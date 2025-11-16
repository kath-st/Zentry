from core.services.event_service import EventService
from events.models import Event, Zone
from reservations.models import Reservation
from core.domain.models import LimitExceeded
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist


class DjangoEventService(EventService):
    """Implementación concreta de EventService usando Django ORM."""

    def get_zone_stock(self, event_id: int, zone_id: str) -> int:
        """Obtiene el stock disponible de una zona en un evento."""
        try:
            zone = Zone.objects.get(event_id=event_id, code=zone_id)
            # Calcular reservas sold/held no expiradas
            reserved = Reservation.objects.filter(
                event_id=event_id,
                zone=zone,
                status__in=["held", "sold"],
            ).aggregate(total=Sum("qty"))["total"] or 0
            
            return max(zone.capacity - reserved, 0)
        except ObjectDoesNotExist:
            return 0

    def get_zone_price(self, event_id: int, zone_id: str, stage: str | None = None) -> float:
        """Obtiene el precio de una zona en un evento."""
        try:
            zone = Zone.objects.get(event_id=event_id, code=zone_id)
            # TODO: Implementar lógica de stages si es necesario (preventa, regular, etc.)
            return float(zone.price)
        except ObjectDoesNotExist:
            raise ValueError(f"Zona {zone_id} no encontrada para el evento {event_id}")

    def ensure_purchase_limit(self, user_id: str, event_id: int, zone_id: str, requested_qty: int) -> None:
        """Verifica que el usuario no supere el límite de entradas."""
        # Límite total de 6 entradas por usuario
        active_reservations = Reservation.objects.filter(
            user_id=user_id,
            status__in=["held", "sold"],
        ).aggregate(total=Sum("qty"))["total"] or 0
        
        if active_reservations + requested_qty > 6:
            raise LimitExceeded(f"Se supera el límite de entradas por usuario (máximo 6). Actualmente tiene {active_reservations}")

    def get_event(self, event_id: int) -> Event:
        """Obtiene un evento por su ID."""
        try:
            return Event.objects.get(id=event_id)
        except ObjectDoesNotExist:
            raise ValueError(f"Evento {event_id} no encontrado")

    def get_zone(self, event_id: int, zone_id: str) -> Zone:
        """Obtiene una zona de un evento."""
        try:
            return Zone.objects.get(event_id=event_id, code=zone_id)
        except ObjectDoesNotExist:
            raise ValueError(f"Zona {zone_id} no encontrada para el evento {event_id}")