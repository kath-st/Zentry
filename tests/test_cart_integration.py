import pytest
from django.test import TestCase, TransactionTestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction, models
from datetime import timedelta

from core.services.cart_service import CartService
from core.domain.models import StockError, LimitExceeded
from events.models import Event, Zone
from reservations.models import Reservation
from cart.models import CartItemModel


class CartIntegrationTestCase(TransactionTestCase):
    """Pruebas de integración para el sistema completo de carrito."""

    def setUp(self):
        """Configuración inicial para las pruebas."""
        # Crear usuarios de prueba
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpass123'
        )
        
        self.user2 = User.objects.create_user(
            username='user2', 
            email='user2@example.com',
            password='testpass123'
        )
        
        # Crear evento de prueba
        self.event = Event.objects.create(
            name='Festival de Rock',
            date=timezone.now() + timedelta(days=30),
            venue='Estadio Nacional'
        )
        
        # Crear zonas con diferentes capacidades y precios
        self.zone_vip = Zone.objects.create(
            event=self.event,
            code='VIP',
            name='Zona VIP Premium',
            capacity=50,
            price=200.00
        )
        
        self.zone_general = Zone.objects.create(
            event=self.event,
            code='GENERAL',
            name='Zona General',
            capacity=1000,
            price=100.00
        )
        
        self.zone_palco = Zone.objects.create(
            event=self.event,
            code='PALCO',
            name='Palco Presidencial',
            capacity=10,  # Capacidad muy limitada
            price=500.00
        )
        
        # Crear instancia del servicio
        self.cart_service = CartService()

    def test_complete_purchase_flow(self):
        """Simula un flujo completo de compra desde carrito vacío hasta confirmación."""
        
        # 1. Verificar carrito inicial vacío
        cart = self.cart_service.get_cart(self.user1)
        self.assertEqual(len(cart.items), 0)
        self.assertEqual(cart.total_amount(), 0)
        
        # 2. Añadir items de diferentes zonas
        cart = self.cart_service.add_item(self.user1, self.event.pk, 'VIP', 2)
        self.assertEqual(len(cart.items), 1)
        self.assertEqual(cart.total_amount(), 400.00)  # 2 * 200
        
        cart = self.cart_service.add_item(self.user1, self.event.pk, 'GENERAL', 3)
        self.assertEqual(len(cart.items), 2)
        self.assertEqual(cart.total_amount(), 700.00)  # 400 + (3 * 100)
        
        # 3. Verificar que se crearon las reservas correctamente
        reservations = Reservation.objects.filter(user=self.user1, status='held')
        self.assertEqual(reservations.count(), 2)
        
        # 4. Actualizar cantidades
        cart = self.cart_service.update_qty(self.user1, self.event.pk, 'VIP', 1)
        self.assertEqual(cart.total_amount(), 500.00)  # 200 + 300
        
        # 5. Simular error y hacer undo
        original_total = cart.total_amount()
        try:
            # Intentar añadir más de la capacidad del palco
            self.cart_service.add_item(self.user1, self.event.pk, 'PALCO', 15)
        except StockError:
            # El carrito debe mantenerse igual
            cart_after_error = self.cart_service.get_cart(self.user1)
            self.assertEqual(cart_after_error.total_amount(), original_total)
        
        # 6. Operación exitosa final
        cart = self.cart_service.add_item(self.user1, self.event.pk, 'PALCO', 2)
        self.assertEqual(len(cart.items), 3)
        final_amount = cart.total_amount()  # 200 + 300 + 1000
        self.assertEqual(final_amount, 1500.00)

    def test_stock_management_between_users(self):
        """Prueba la gestión de stock entre múltiples usuarios."""
        
        # Usuario 1 añade casi toda la capacidad del palco (respetando límite de 6)
        self.cart_service.add_item(self.user1, self.event.pk, 'PALCO', 5)
        
        # Verificar stock restante
        stock_remaining = self.cart_service.event_service.get_zone_stock(self.event.pk, 'PALCO')
        self.assertEqual(stock_remaining, 2)  # 10 - 8 = 2
        
        # Usuario 2 puede tomar el stock restante
        cart2 = self.cart_service.add_item(self.user2, self.event.pk, 'PALCO', 2)
        self.assertEqual(cart2.items[0].qty, 2)
        
        # Verificar que no queda stock
        stock_remaining = self.cart_service.event_service.get_zone_stock(self.event.pk, 'PALCO')
        self.assertEqual(stock_remaining, 0)
        
        # Usuario 2 no puede añadir más
        with self.assertRaises(StockError):
            self.cart_service.add_item(self.user2, self.event.pk, 'PALCO', 1)
        
        # Si Usuario 1 reduce su cantidad, se libera stock
        self.cart_service.update_qty(self.user1, self.event.pk, 'PALCO', 5)
        stock_after_reduction = self.cart_service.event_service.get_zone_stock(self.event.pk, 'PALCO')
        self.assertEqual(stock_after_reduction, 3)  # Se liberaron 3 entradas

    def test_purchase_limits_enforcement(self):
        """Prueba que se respeten los límites de compra por usuario."""
        
        # Usuario intenta comprar exactamente el límite (6 entradas)
        self.cart_service.add_item(self.user1, self.event.pk, 'GENERAL', 6)
        cart = self.cart_service.get_cart(self.user1)
        self.assertEqual(cart.total_qty(), 6)
        
        # Intentar añadir una entrada más debe fallar
        with self.assertRaises(LimitExceeded):
            self.cart_service.add_item(self.user1, self.event.pk, 'VIP', 1)
        
        # Pero puede intercambiar (eliminar una zona y añadir otra)
        self.cart_service.update_qty(self.user1, self.event.pk, 'GENERAL', 4)
        self.cart_service.add_item(self.user1, self.event.pk, 'VIP', 2)
        
        cart_final = self.cart_service.get_cart(self.user1)
        self.assertEqual(cart_final.total_qty(), 6)  # 4 + 2 = 6

    def test_reservation_lifecycle(self):
        """Prueba el ciclo de vida completo de las reservas."""
        
        # Añadir item crea reserva en estado 'held'
        cart = self.cart_service.add_item(self.user1, self.event.pk, 'VIP', 2)
        reservation_id = cart.items[0].reservation_id
        
        reservation = Reservation.objects.get(id=reservation_id)
        self.assertEqual(reservation.status, 'held')
        self.assertEqual(reservation.qty, 2)
        self.assertFalse(reservation.is_expired())
        
        # Actualizar cantidad actualiza la reserva
        self.cart_service.update_qty(self.user1, self.event.pk, 'VIP', 3)
        reservation.refresh_from_db()
        self.assertEqual(reservation.qty, 3)
        
        # Eliminar item libera (cancela) la reserva
        self.cart_service.remove_item(self.user1, self.event.pk, 'VIP')
        reservation.refresh_from_db()
        self.assertEqual(reservation.status, 'cancelled')

    def test_undo_restores_reservations_correctly(self):
        """Prueba que el undo restaura correctamente las reservas."""
        
        # Estado inicial: añadir item
        cart1 = self.cart_service.add_item(self.user1, self.event.pk, 'VIP', 2)
        original_reservation_id = cart1.items[0].reservation_id
        
        # Añadir segundo item
        cart2 = self.cart_service.add_item(self.user1, self.event.pk, 'GENERAL', 3)
        
        # Verificar que hay 2 reservas activas
        active_reservations = Reservation.objects.filter(user=self.user1, status='held')
        self.assertEqual(active_reservations.count(), 2)
        
        # Hacer undo (volver al estado con solo VIP)
        cart_after_undo = self.cart_service.undo(self.user1)
        self.assertEqual(len(cart_after_undo.items), 1)
        self.assertEqual(cart_after_undo.items[0].zone_id, 'VIP')
        
        # Verificar que solo queda 1 reserva activa (la de VIP)
        active_reservations_after_undo = Reservation.objects.filter(user=self.user1, status='held')
        self.assertEqual(active_reservations_after_undo.count(), 1)

    def test_concurrent_modifications_safety(self):
        """Prueba la seguridad ante modificaciones concurrentes."""
        
        # Simular condición de carrera: dos usuarios intentan tomar las últimas entradas
        # Configurar zona con capacidad muy limitada (solo 1 entrada)
        limited_zone = Zone.objects.create(
            event=self.event,
            code='LIMITED',
            name='Zona Limitada',
            capacity=1,
            price=300.00
        )
        
        # En condiciones normales, solo uno debería poder obtener la entrada
        success_count = 0
        error_count = 0
        
        # Usuario 1 intenta comprar
        try:
            self.cart_service.add_item(self.user1, self.event.pk, 'LIMITED', 1)
            success_count += 1
        except StockError:
            error_count += 1
        
        # Usuario 2 intenta comprar la misma entrada
        try:
            self.cart_service.add_item(self.user2, self.event.pk, 'LIMITED', 1)
            success_count += 1
        except StockError:
            error_count += 1
        
        # Solo uno debe haber tenido éxito
        self.assertEqual(success_count, 1)
        self.assertEqual(error_count, 1)
        
        # Verificar que no se sobre-vendió
        total_reserved = Reservation.objects.filter(
            event=self.event,
            zone=limited_zone,
            status='held'
        ).aggregate(total=models.Sum('qty'))['total'] or 0
        
        self.assertEqual(total_reserved, 1)

    def test_data_consistency_after_operations(self):
        """Prueba la consistencia de datos después de múltiples operaciones."""
        
        # Realizar secuencia compleja de operaciones
        self.cart_service.add_item(self.user1, self.event.pk, 'VIP', 2)
        self.cart_service.add_item(self.user1, self.event.pk, 'GENERAL', 3)
        self.cart_service.update_qty(self.user1, self.event.pk, 'VIP', 1)
        self.cart_service.add_item(self.user1, self.event.pk, 'PALCO', 1)
        
        # Verificar consistencia entre carrito y reservas
        cart = self.cart_service.get_cart(self.user1)
        
        total_cart_qty = cart.total_qty()
        total_reservations_qty = Reservation.objects.filter(
            user=self.user1,
            status='held'
        ).aggregate(total=models.Sum('qty'))['total'] or 0
        
        self.assertEqual(total_cart_qty, total_reservations_qty)
        
        # Verificar que cada item del carrito tiene su reserva correspondiente
        for item in cart.items:
            self.assertIsNotNone(item.reservation_id)
            reservation = Reservation.objects.get(id=item.reservation_id)
            self.assertEqual(reservation.status, 'held')
            self.assertEqual(reservation.qty, item.qty)
            self.assertEqual(reservation.zone.code, item.zone_id)

    def test_error_recovery_with_undo(self):
        """Prueba la recuperación de errores usando undo."""
        
        # Estado inicial estable
        cart1 = self.cart_service.add_item(self.user1, self.event.pk, 'GENERAL', 2)
        initial_total = cart1.total_amount()
        
        # Realizar operación que va a fallar
        try:
            # Intentar añadir más entradas de las permitidas
            self.cart_service.add_item(self.user1, self.event.pk, 'GENERAL', 5)  # Total sería 7 > 6
            self.fail("Debería haber lanzado LimitExceeded")
        except LimitExceeded:
            # El carrito debe mantenerse intacto
            cart_after_error = self.cart_service.get_cart(self.user1)
            self.assertEqual(cart_after_error.total_amount(), initial_total)
            self.assertTrue(self.cart_service.can_undo(self.user1))
        
        # Añadir operación exitosa
        cart2 = self.cart_service.add_item(self.user1, self.event.pk, 'VIP', 1)
        
        # Si necesita recuperarse, puede usar undo
        if cart2.total_amount() != initial_total + 200:
            cart_recovered = self.cart_service.undo(self.user1)
            self.assertEqual(cart_recovered.total_amount(), initial_total)

    def test_multiple_users_independent_operations(self):
        """Prueba que las operaciones de usuarios múltiples son independientes."""
        
        # Ambos usuarios crean carritos independientes
        cart1 = self.cart_service.add_item(self.user1, self.event.pk, 'VIP', 1)
        cart2 = self.cart_service.add_item(self.user2, self.event.pk, 'GENERAL', 2)
        
        # Verificar independencia
        self.assertEqual(len(cart1.items), 1)
        self.assertEqual(len(cart2.items), 1)
        self.assertEqual(cart1.items[0].zone_id, 'VIP')
        self.assertEqual(cart2.items[0].zone_id, 'GENERAL')
        
        # Undo de usuario 1 no afecta usuario 2
        self.cart_service.undo(self.user1)
        
        cart1_after_undo = self.cart_service.get_cart(self.user1)
        cart2_after_undo = self.cart_service.get_cart(self.user2)
        
        self.assertEqual(len(cart1_after_undo.items), 0)
        self.assertEqual(len(cart2_after_undo.items), 1)  # Usuario 2 no afectado
        
        # Stacks de undo independientes
        self.assertFalse(self.cart_service.can_undo(self.user1))
        self.assertTrue(self.cart_service.can_undo(self.user2))