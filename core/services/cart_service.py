from typing import Dict
from django.contrib.auth.models import User
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from core.datastructures.stack import Stack, StackUnderflow
from core.domain.models import Cart, CartItem, StockError
from core.services.django_event_service import DjangoEventService
from core.services.django_reservation_service import DjangoReservationService
from cart.models import CartItemModel


class CartService:
    """
    Servicio del carrito de compras con funcionalidad de Undo usando Stack.
    
    Este servicio mantiene el estado del carrito en Django ORM y utiliza
    una pila (Stack) en memoria para implementar la funcionalidad de deshacer.
    """

    def __init__(self, event_service: DjangoEventService | None = None, reservation_service: DjangoReservationService | None = None):
        self.event_service = event_service or DjangoEventService()
        self.reservation_service = reservation_service or DjangoReservationService()
        # Diccionario de pilas de undo por usuario
        self._undo_stacks: Dict[int, Stack] = {}

    def _get_user_stack(self, user: User) -> Stack:
        """Obtiene o crea la pila de undo para un usuario."""
        if user.pk not in self._undo_stacks:
            self._undo_stacks[user.pk] = Stack(maxlen=10)  # Límite de 10 undos
        return self._undo_stacks[user.pk]

    def _capture_state(self, user: User) -> Cart:
        """Captura el estado actual del carrito del usuario."""
        cart_items_models = CartItemModel.objects.filter(user=user).select_related('event', 'zone')
        
        items = []
        for item_model in cart_items_models:
            cart_item = CartItem(
                event_id=item_model.event.pk,
                zone_id=item_model.zone.code,
                qty=item_model.qty,
                unit_price=float(item_model.unit_price),
                reservation_id=str(item_model.reservation.pk) if item_model.reservation else None
            )
            items.append(cart_item)
        
        return Cart(user_id=str(user.pk), items=items)

    def _restore_state(self, user: User, cart: Cart) -> None:
        """Restaura el carrito a un estado específico."""
        with transaction.atomic():
            # Liberar reservas actuales
            current_items = CartItemModel.objects.filter(user=user).select_related('reservation')
            for item in current_items:
                if item.reservation:
                    self.reservation_service.release(str(item.reservation.pk))
            
            # Eliminar todos los items actuales del carrito
            CartItemModel.objects.filter(user=user).delete()
            
            # Recrear los items del estado guardado
            for cart_item in cart.items:
                try:
                    event = self.event_service.get_event(cart_item.event_id)
                    zone = self.event_service.get_zone(cart_item.event_id, cart_item.zone_id)
                    
                    # Crear reserva si es necesario
                    reservation = None
                    if cart_item.reservation_id:
                        try:
                            reservation = self.reservation_service.get_reservation(cart_item.reservation_id)
                            # Si la reserva ha expirado, crear una nueva
                            if self.reservation_service.is_expired(cart_item.reservation_id):
                                reservation_id = self.reservation_service.hold(
                                    str(user.pk), 
                                    cart_item.event_id, 
                                    cart_item.zone_id, 
                                    cart_item.qty
                                )
                                reservation = self.reservation_service.get_reservation(reservation_id)
                        except ValueError:
                            # Si la reserva no existe, crear una nueva
                            reservation_id = self.reservation_service.hold(
                                str(user.pk), 
                                cart_item.event_id, 
                                cart_item.zone_id, 
                                cart_item.qty
                            )
                            reservation = self.reservation_service.get_reservation(reservation_id)
                    
                    # Crear el item del carrito
                    CartItemModel.objects.create(
                        user=user,
                        event=event,
                        zone=zone,
                        qty=cart_item.qty,
                        unit_price=cart_item.unit_price,
                        reservation=reservation
                    )
                    
                except Exception as e:
                    # Si hay error al restaurar un item, continuar con los demás
                    print(f"Error restaurando item {cart_item}: {e}")

    def get_cart(self, user: User) -> Cart:
        """Obtiene el carrito actual del usuario."""
        return self._capture_state(user)

    def add_item(self, user: User, event_id: int, zone_code: str, qty: int) -> Cart:
        """
        Añade un item al carrito.
        
        Args:
            user: Usuario propietario del carrito
            event_id: ID del evento
            zone_code: Código de la zona (ej: "VIP", "GENERAL")
            qty: Cantidad de entradas a añadir
            
        Returns:
            Cart actualizado
            
        Raises:
            StockError: Si no hay suficiente stock
            LimitExceeded: Si se supera el límite de entradas por usuario
        """
        if qty <= 0:
            raise ValueError("La cantidad debe ser mayor que cero")

        # Capturar estado anterior para undo
        previous_state = self._capture_state(user)
        self._get_user_stack(user).push(previous_state)

        with transaction.atomic():
            # Verificar stock disponible
            stock = self.event_service.get_zone_stock(event_id, zone_code)
            if stock < qty:
                raise StockError(f"Stock insuficiente. Disponible: {stock}, solicitado: {qty}")

        # Verificar límite de compra
        self.event_service.ensure_purchase_limit(str(user.pk), event_id, zone_code, qty)

        # Buscar si ya existe un item para este evento y zona
        try:
            existing_item = CartItemModel.objects.get(
                user=user,
                event_id=event_id,
                zone__code=zone_code
            )
            
            # Verificar que la nueva cantidad total no supere el stock
            new_total_qty = existing_item.qty + qty
            if stock < new_total_qty - existing_item.qty:  # stock actual menos lo que ya tenía reservado
                raise StockError(f"Stock insuficiente para la cantidad total solicitada")
            
            # Actualizar cantidad
            existing_item.qty = new_total_qty
            existing_item.save()
            
            # Actualizar reserva
            if existing_item.reservation:
                self.reservation_service.update_qty(str(existing_item.reservation.pk), new_total_qty)
            
        except CartItemModel.DoesNotExist:
                # Crear nuevo item
                event = self.event_service.get_event(event_id)
                zone = self.event_service.get_zone(event_id, zone_code)
                unit_price = self.event_service.get_zone_price(event_id, zone_code)
                
                # Crear reserva
                reservation_id = self.reservation_service.hold(str(user.pk), event_id, zone_code, qty)
                reservation = self.reservation_service.get_reservation(reservation_id)
                
                # Crear item del carrito
                CartItemModel.objects.create(
                    user=user,
                    event=event,
                    zone=zone,
                    qty=qty,
                    unit_price=unit_price,
                    reservation=reservation
                )

        return self.get_cart(user)

    def update_qty(self, user: User, event_id: int, zone_code: str, new_qty: int) -> Cart:
        """
        Actualiza la cantidad de un item del carrito.
        
        Args:
            user: Usuario propietario del carrito
            event_id: ID del evento
            zone_code: Código de la zona
            new_qty: Nueva cantidad
            
        Returns:
            Cart actualizado
        """
        if new_qty == 0:
            return self.remove_item(user, event_id, zone_code)
        
        if new_qty < 0:
            raise ValueError("La cantidad no puede ser negativa")

        # Capturar estado anterior para undo
        previous_state = self._capture_state(user)
        self._get_user_stack(user).push(previous_state)

        with transaction.atomic():
            try:
                item = CartItemModel.objects.get(
                    user=user,
                    event_id=event_id,
                    zone__code=zone_code
                )
                
                # Verificar stock para la nueva cantidad
                stock = self.event_service.get_zone_stock(event_id, zone_code)
                # Sumar el stock que se liberaría si disminuye la cantidad
                available_stock = stock + max(0, item.qty - new_qty)
                
                if new_qty > available_stock:
                    raise StockError(f"Stock insuficiente. Disponible: {available_stock}")

                # Verificar límite de compra
                qty_diff = new_qty - item.qty
                if qty_diff > 0:
                    self.event_service.ensure_purchase_limit(str(user.pk), event_id, zone_code, qty_diff)

                # Actualizar cantidad
                item.qty = new_qty
                item.save()
                
                # Actualizar reserva
                if item.reservation:
                    self.reservation_service.update_qty(str(item.reservation.pk), new_qty)
                
            except CartItemModel.DoesNotExist:
                raise ValueError(f"Item no encontrado en el carrito para evento {event_id} y zona {zone_code}")

        return self.get_cart(user)

    def remove_item(self, user: User, event_id: int, zone_code: str) -> Cart:
        """
        Elimina un item del carrito.
        
        Args:
            user: Usuario propietario del carrito
            event_id: ID del evento
            zone_code: Código de la zona
            
        Returns:
            Cart actualizado
        """
        # Capturar estado anterior para undo
        previous_state = self._capture_state(user)
        self._get_user_stack(user).push(previous_state)

        with transaction.atomic():
            try:
                item = CartItemModel.objects.get(
                    user=user,
                    event_id=event_id,
                    zone__code=zone_code
                )
                
                # Liberar reserva
                if item.reservation:
                    self.reservation_service.release(str(item.reservation.pk))
                
                # Eliminar item
                item.delete()
                
            except CartItemModel.DoesNotExist:
                # Si el item no existe, no hay nada que hacer
                pass

        return self.get_cart(user)

    def clear_cart(self, user: User) -> None:
        """Vacía completamente el carrito del usuario."""
        # Capturar estado anterior para undo
        previous_state = self._capture_state(user)
        self._get_user_stack(user).push(previous_state)

        with transaction.atomic():
            items = CartItemModel.objects.filter(user=user).select_related('reservation')
            
            # Liberar todas las reservas
            for item in items:
                if item.reservation:
                    self.reservation_service.release(str(item.reservation.pk))
            
            # Eliminar todos los items
            items.delete()

    def undo(self, user: User) -> Cart:
        """
        Deshace la última operación del carrito.
        
        Args:
            user: Usuario propietario del carrito
            
        Returns:
            Cart restaurado al estado anterior
            
        Raises:
            StackUnderflow: Si no hay operaciones para deshacer
        """
        user_stack = self._get_user_stack(user)
        
        if user_stack.is_empty():
            raise StackUnderflow("No hay operaciones para deshacer")
        
        # Obtener estado anterior
        previous_state = user_stack.pop()
        
        # Restaurar estado
        self._restore_state(user, previous_state)
        
        return self.get_cart(user)

    def can_undo(self, user: User) -> bool:
        """Verifica si el usuario puede deshacer alguna operación."""
        user_stack = self._get_user_stack(user)
        return not user_stack.is_empty()

    def get_undo_count(self, user: User) -> int:
        """Obtiene el número de operaciones que se pueden deshacer."""
        user_stack = self._get_user_stack(user)
        return len(user_stack)