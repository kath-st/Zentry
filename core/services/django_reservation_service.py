from core.services.reservation_service import ReservationService
from reservations.models import Reservation
from events.models import Event, Zone
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta


class DjangoReservationService(ReservationService):
    """Implementación concreta de ReservationService usando Django ORM."""

    def hold(self, user_id: str, event_id: int, zone_id: str, qty: int, ttl_minutes: int = 15) -> str:
        """Crea una reserva en estado 'held'."""
        try:
            event = Event.objects.get(id=event_id)
            zone = Zone.objects.get(event_id=event_id, code=zone_id)
            
            expires_at = timezone.now() + timedelta(minutes=ttl_minutes)
            
            reservation = Reservation.objects.create(
                user_id=user_id,
                event=event,
                zone=zone,
                qty=qty,
                status="held",
                expires_at=expires_at
            )
            
            return str(reservation.pk)
        except ObjectDoesNotExist as e:
            raise ValueError(f"Error al crear reserva: {str(e)}")

    def release(self, reservation_id: str) -> None:
        """Libera una reserva (marca como cancelled)."""
        try:
            reservation = Reservation.objects.get(id=int(reservation_id))
            reservation.status = "cancelled"
            reservation.save()
        except (ObjectDoesNotExist, ValueError):
            # Si la reserva no existe, no hay nada que hacer
            pass

    def confirm(self, reservation_id: str) -> None:
        """Confirma una reserva (marca como sold)."""
        try:
            reservation = Reservation.objects.get(id=int(reservation_id))
            reservation.status = "sold"
            reservation.save()
        except (ObjectDoesNotExist, ValueError):
            raise ValueError(f"Reserva {reservation_id} no encontrada")

    def is_expired(self, reservation_id: str) -> bool:
        """Verifica si una reserva ha expirado."""
        try:
            reservation = Reservation.objects.get(id=int(reservation_id))
            is_expired = reservation.is_expired()
            
            # Si ha expirado y aún está en held, marcar como expired
            if is_expired and reservation.status == "held":
                reservation.status = "expired"
                reservation.save()
                
            return is_expired
        except (ObjectDoesNotExist, ValueError):
            return True  # Si no se encuentra, se considera expirada

    def get_reservation(self, reservation_id: str) -> Reservation:
        """Obtiene una reserva por su ID."""
        try:
            return Reservation.objects.get(id=int(reservation_id))
        except (ObjectDoesNotExist, ValueError):
            raise ValueError(f"Reserva {reservation_id} no encontrada")

    def update_qty(self, reservation_id: str, new_qty: int) -> None:
        """Actualiza la cantidad de una reserva."""
        try:
            reservation = Reservation.objects.get(id=int(reservation_id))
            reservation.qty = new_qty
            reservation.save()
        except (ObjectDoesNotExist, ValueError):
            raise ValueError(f"Reserva {reservation_id} no encontrada")