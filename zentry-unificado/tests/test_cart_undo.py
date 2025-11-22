import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from core.services.cart_service import CartService
from core.datastructures.stack import StackUnderflow
from core.domain.models import StockError, LimitExceeded
from events.models import Event, Zone
from reservations.models import Reservation
from cart.models import CartItemModel

User = get_user_model()


class CartUndoTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            dni='12345678'
        )
        
        # Crear evento de prueba
        self.event = Event.objects.create(
            name='Concierto Test',
            date=timezone.now() + timedelta(days=30),
            venue='Estadio Test'
        )
        
        # Crear zonas de prueba
        self.zone_vip = Zone.objects.create(
            event=self.event,
            code='VIP',
            name='Zona VIP',
            capacity=100,
            price=150.00
        )
        
        self.zone_general = Zone.objects.create(
            event=self.event,
            code='GENERAL',
            name='Zona General',
            capacity=500,
            price=75.00
        )
        
        # Crear instancia del servicio
        self.cart_service = CartService()

    def test_add_item_and_undo(self):
        """Prueba añadir un item y luego deshacerlo."""
        # Estado inicial: carrito vacío
        initial_cart = self.cart_service.get_cart(self.user)
        self.assertEqual(len(initial_cart.items), 0)
        self.assertFalse(self.cart_service.can_undo(self.user))
        
        # Añadir item
        cart_after_add = self.cart_service.add_item(self.user, self.event.pk, 'VIP', 2)
        self.assertEqual(len(cart_after_add.items), 1)
        self.assertEqual(cart_after_add.items[0].qty, 2)
        self.assertTrue(self.cart_service.can_undo(self.user))
        
        # Deshacer
        cart_after_undo = self.cart_service.undo(self.user)
        self.assertEqual(len(cart_after_undo.items), 0)
        self.assertFalse(self.cart_service.can_undo(self.user))

    def test_update_qty_and_undo(self):
        """Prueba actualizar cantidad y luego deshacerlo."""
        # Añadir item inicial
        self.cart_service.add_item(self.user, self.event.pk, 'VIP', 2)
        
        # Actualizar cantidad
        cart_after_update = self.cart_service.update_qty(self.user, self.event.pk, 'VIP', 5)
        self.assertEqual(cart_after_update.items[0].qty, 5)
        self.assertEqual(self.cart_service.get_undo_count(self.user), 2)  # add + update
        
        # Deshacer la actualización
        cart_after_undo = self.cart_service.undo(self.user)
        self.assertEqual(cart_after_undo.items[0].qty, 2)  # Vuelve al estado anterior
        
    def test_remove_item_and_undo(self):
        """Prueba eliminar un item y luego deshacerlo."""
        # Añadir item inicial
        self.cart_service.add_item(self.user, self.event.pk, 'VIP', 3)
        
        # Eliminar item
        cart_after_remove = self.cart_service.remove_item(self.user, self.event.pk, 'VIP')
        self.assertEqual(len(cart_after_remove.items), 0)
        
        # Deshacer eliminación
        cart_after_undo = self.cart_service.undo(self.user)
        self.assertEqual(len(cart_after_undo.items), 1)
        self.assertEqual(cart_after_undo.items[0].qty, 3)

    def test_clear_cart_and_undo(self):
        """Prueba vaciar carrito y luego deshacerlo."""
        # Añadir varios items
        self.cart_service.add_item(self.user, self.event.pk, 'VIP', 2)
        self.cart_service.add_item(self.user, self.event.pk, 'GENERAL', 4)
        
        cart_before_clear = self.cart_service.get_cart(self.user)
        self.assertEqual(len(cart_before_clear.items), 2)
        
        # Vaciar carrito
        self.cart_service.clear_cart(self.user)
        cart_after_clear = self.cart_service.get_cart(self.user)
        self.assertEqual(len(cart_after_clear.items), 0)
        
        # Deshacer vaciado
        cart_after_undo = self.cart_service.undo(self.user)
        self.assertEqual(len(cart_after_undo.items), 2)

    def test_multiple_undos(self):
        """Prueba varios undos consecutivos."""
        # Estado inicial
        self.assertFalse(self.cart_service.can_undo(self.user))
        
        # Operación 1: Añadir VIP
        self.cart_service.add_item(self.user, self.event.pk, 'VIP', 1)
        self.assertEqual(self.cart_service.get_undo_count(self.user), 1)
        
        # Operación 2: Añadir GENERAL
        self.cart_service.add_item(self.user, self.event.pk, 'GENERAL', 2)
        self.assertEqual(self.cart_service.get_undo_count(self.user), 2)
        
        # Operación 3: Actualizar VIP
        self.cart_service.update_qty(self.user, self.event.pk, 'VIP', 3)
        self.assertEqual(self.cart_service.get_undo_count(self.user), 3)
        
        # Undo 1: Volver al estado antes de actualizar VIP
        cart1 = self.cart_service.undo(self.user)
        self.assertEqual(len(cart1.items), 2)
        vip_item = next(item for item in cart1.items if item.zone_id == 'VIP')
        self.assertEqual(vip_item.qty, 1)  # Cantidad original
        
        # Undo 2: Volver al estado antes de añadir GENERAL
        cart2 = self.cart_service.undo(self.user)
        self.assertEqual(len(cart2.items), 1)
        self.assertEqual(cart2.items[0].zone_id, 'VIP')
        
        # Undo 3: Volver al estado inicial (vacío)
        cart3 = self.cart_service.undo(self.user)
        self.assertEqual(len(cart3.items), 0)
        self.assertFalse(self.cart_service.can_undo(self.user))

    def test_undo_empty_stack(self):
        """Prueba hacer undo cuando la pila está vacía."""
        # Verificar que no se puede hacer undo en carrito nuevo
        self.assertFalse(self.cart_service.can_undo(self.user))
        
        # Intentar undo debe lanzar StackUnderflow
        with self.assertRaises(StackUnderflow):
            self.cart_service.undo(self.user)

    def test_undo_after_multiple_operations(self):
        """Prueba undo después de operaciones complejas."""
        # Secuencia de operaciones complejas
        self.cart_service.add_item(self.user, self.event.pk, 'VIP', 2)      # Estado A
        self.cart_service.add_item(self.user, self.event.pk, 'GENERAL', 3)  # Estado B
        self.cart_service.update_qty(self.user, self.event.pk, 'VIP', 1)     # Estado C
        self.cart_service.remove_item(self.user, self.event.pk, 'GENERAL')   # Estado D
        
        final_cart = self.cart_service.get_cart(self.user)
        self.assertEqual(len(final_cart.items), 1)
        self.assertEqual(final_cart.items[0].zone_id, 'VIP')
        self.assertEqual(final_cart.items[0].qty, 1)
        
        # Undo para volver al estado C (antes de eliminar GENERAL)
        cart_c = self.cart_service.undo(self.user)
        self.assertEqual(len(cart_c.items), 2)
        
        # Undo para volver al estado B (antes de actualizar VIP)
        cart_b = self.cart_service.undo(self.user)
        vip_item = next(item for item in cart_b.items if item.zone_id == 'VIP')
        self.assertEqual(vip_item.qty, 2)  # Cantidad original

    def test_undo_preserves_reservations(self):
        """Prueba que el undo maneja correctamente las reservas."""
        # Añadir item (esto crea una reserva)
        cart = self.cart_service.add_item(self.user, self.event.pk, 'VIP', 2)
        
        # Verificar que se creó la reserva
        self.assertIsNotNone(cart.items[0].reservation_id)
        reservation_id = cart.items[0].reservation_id
        
        # Eliminar item
        self.cart_service.remove_item(self.user, self.event.pk, 'VIP')
        
        # Undo: debe restaurar el item con su reserva
        restored_cart = self.cart_service.undo(self.user)
        self.assertEqual(len(restored_cart.items), 1)
        # La reserva puede ser la misma o una nueva (dependiendo de si expiró)
        self.assertIsNotNone(restored_cart.items[0].reservation_id)

    def test_concurrent_users_independent_undo_stacks(self):
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123',
            dni='87654321'
        )
        
        # Usuario 1 añade item
        self.cart_service.add_item(self.user, self.event.pk, 'VIP', 1)
        self.assertTrue(self.cart_service.can_undo(self.user))
        self.assertFalse(self.cart_service.can_undo(user2))
        
        # Usuario 2 añade item diferente
        self.cart_service.add_item(user2, self.event.pk, 'GENERAL', 2)
        self.assertTrue(self.cart_service.can_undo(user2))
        
        # Los undos son independientes
        self.assertEqual(self.cart_service.get_undo_count(self.user), 1)
        self.assertEqual(self.cart_service.get_undo_count(user2), 1)
        
        # Undo usuario 1 no afecta usuario 2
        self.cart_service.undo(self.user)
        self.assertFalse(self.cart_service.can_undo(self.user))
        self.assertTrue(self.cart_service.can_undo(user2))  # Usuario 2 sigue pudiendo hacer undo

    def test_undo_stack_capacity_limit(self):
        """Prueba que la pila de undo respeta el límite de capacidad."""
        # Hacer más de 10 operaciones (límite del stack)
        for i in range(12):
            if i % 2 == 0 and i < 6:  # Respetar límite de usuario
                self.cart_service.add_item(self.user, self.event.pk, 'VIP', 1)
            elif i % 2 != 0:
                # Solo actualizar cantidad si ya tenemos items
                try:
                    self.cart_service.update_qty(self.user, self.event.pk, 'VIP', min(i + 1, 6))
                except:
                    pass  # Ignorar errores de límite
        
        # Solo debe poder deshacer las últimas 10 operaciones
        self.assertEqual(self.cart_service.get_undo_count(self.user), 10)
        
        # Hacer 10 undos
        for _ in range(10):
            self.cart_service.undo(self.user)
        
        # Ya no debe poder hacer más undos
        self.assertFalse(self.cart_service.can_undo(self.user))
        
        with self.assertRaises(StackUnderflow):
            self.cart_service.undo(self.user)