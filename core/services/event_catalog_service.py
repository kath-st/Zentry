"""
Servicio de Catálogo Dinámico de Eventos.
Gestiona la lista enlazada, búsqueda y ordenamiento de eventos.
Componente de Cerna Sifuentes - Estructura de Datos
"""

from typing import List, Optional, Callable
from datetime import datetime
from core.datastructures.linked_list import LinkedList
from core.domain.event_catalog import (
    EventCatalog, SortCriteria, COMPARATORS,
    compare_by_date, compare_by_price, compare_by_popularity
)


class EventCatalogService:
    """
    Servicio que gestiona el catálogo dinámico de eventos
    usando lista enlazada y algoritmos de búsqueda/ordenamiento.
    """

    def __init__(self):
        """Inicializa el servicio con una lista enlazada vacía."""
        self.events_list: LinkedList[EventCatalog] = LinkedList()
        self._id_index: dict[int, EventCatalog] = {}  # Índice rápido por ID

    # ==================== CRUD ====================

    def add_event(self, event: EventCatalog) -> EventCatalog:
        """
        Añade un nuevo evento al catálogo.
        
        Args:
            event: Evento a añadir
            
        Returns:
            El evento añadido
            
        Raises:
            ValueError: Si el evento con ese ID ya existe
        """
        if event.id in self._id_index:
            raise ValueError(f"Evento con ID {event.id} ya existe")
        
        self.events_list.insert(event)
        self._id_index[event.id] = event
        return event

    def get_event(self, event_id: int) -> Optional[EventCatalog]:
        """
        Obtiene un evento por ID.
        
        Args:
            event_id: ID del evento
            
        Returns:
            Evento si existe, None en caso contrario
        """
        return self._id_index.get(event_id)

    def update_event(self, event_id: int, **kwargs) -> Optional[EventCatalog]:
        """
        Actualiza un evento existente.
        
        Args:
            event_id: ID del evento
            **kwargs: Campos a actualizar
            
        Returns:
            Evento actualizado o None si no existe
        """
        event = self.get_event(event_id)
        if not event:
            return None

        # Actualizar campos permitidos
        allowed_fields = {
            'name', 'venue', 'date', 'description', 'artist_name',
            'min_price', 'max_price', 'total_capacity', 'sold_tickets',
            'is_active'
        }
        
        for key, value in kwargs.items():
            if key in allowed_fields:
                setattr(event, key, value)
        
        event.updated_at = datetime.now()
        return event

    def delete_event(self, event_id: int) -> bool:
        """
        Elimina un evento del catálogo.
        
        Args:
            event_id: ID del evento
            
        Returns:
            True si se eliminó, False si no existía
        """
        event = self.get_event(event_id)
        if not event:
            return False
        
        self.events_list.delete(event)
        del self._id_index[event_id]
        return True

    # ==================== BÚSQUEDA ====================

    def get_all_events(self) -> List[EventCatalog]:
        """Obtiene todos los eventos en el catálogo."""
        return self.events_list.to_list()

    def search_by_id(self, event_id: int) -> Optional[EventCatalog]:
        """Búsqueda rápida por ID (O(1))."""
        return self._id_index.get(event_id)

    def search_by_name(self, name: str) -> List[EventCatalog]:
        """
        Busca eventos por nombre (búsqueda parcial case-insensitive).
        
        Args:
            name: Nombre o parte del nombre a buscar
            
        Returns:
            Lista de eventos que coinciden
        """
        name_lower = name.lower()
        predicate = lambda e: name_lower in e.name.lower()
        return self.events_list.filter(predicate).to_list()

    def search_by_artist(self, artist_name: str) -> List[EventCatalog]:
        """
        Busca eventos por artista.
        
        Args:
            artist_name: Nombre del artista
            
        Returns:
            Lista de eventos del artista
        """
        artist_lower = artist_name.lower()
        predicate = lambda e: artist_lower in e.artist_name.lower()
        return self.events_list.filter(predicate).to_list()

    def search_by_venue(self, venue: str) -> List[EventCatalog]:
        """Busca eventos por lugar."""
        venue_lower = venue.lower()
        predicate = lambda e: venue_lower in e.venue.lower()
        return self.events_list.filter(predicate).to_list()

    def search_upcoming_events(self) -> List[EventCatalog]:
        """Obtiene todos los eventos futuros."""
        now = datetime.now()
        predicate = lambda e: e.date > now and e.is_active
        return self.events_list.filter(predicate).to_list()

    def search_available_events(self) -> List[EventCatalog]:
        """Obtiene eventos con tickets disponibles."""
        predicate = lambda e: not e.is_sold_out() and e.is_active
        return self.events_list.filter(predicate).to_list()

    def search_by_price_range(self, min_price: float, max_price: float) -> List[EventCatalog]:
        """
        Busca eventos dentro de un rango de precios.
        
        Args:
            min_price: Precio mínimo
            max_price: Precio máximo
            
        Returns:
            Lista de eventos en ese rango
        """
        predicate = lambda e: e.min_price >= min_price and e.max_price <= max_price
        return self.events_list.filter(predicate).to_list()

    def search_by_date_range(self, start_date: datetime, end_date: datetime) -> List[EventCatalog]:
        """
        Busca eventos en un rango de fechas.
        
        Args:
            start_date: Fecha inicial
            end_date: Fecha final
            
        Returns:
            Lista de eventos en ese rango
        """
        predicate = lambda e: start_date <= e.date <= end_date
        return self.events_list.filter(predicate).to_list()

    # ==================== ORDENAMIENTO ====================

    def sort_by_date(self, algorithm: str = "merge") -> List[EventCatalog]:
        """
        Ordena eventos por fecha (más próximos primero).
        
        Args:
            algorithm: "merge" para MergeSort o "quick" para QuickSort
            
        Returns:
            Lista ordenada de eventos
        """
        temp_list = LinkedList[EventCatalog]()
        temp_list.from_list(self.events_list.to_list())
        
        if algorithm == "quick":
            temp_list.quick_sort(compare_by_date)
        else:
            temp_list.merge_sort(compare_by_date)
        
        return temp_list.to_list()

    def sort_by_price(self, algorithm: str = "merge") -> List[EventCatalog]:
        """
        Ordena eventos por precio mínimo (menor precio primero).
        
        Args:
            algorithm: "merge" para MergeSort o "quick" para QuickSort
            
        Returns:
            Lista ordenada de eventos
        """
        temp_list = LinkedList[EventCatalog]()
        temp_list.from_list(self.events_list.to_list())
        
        if algorithm == "quick":
            temp_list.quick_sort(compare_by_price)
        else:
            temp_list.merge_sort(compare_by_price)
        
        return temp_list.to_list()

    def sort_by_popularity(self, algorithm: str = "merge") -> List[EventCatalog]:
        """
        Ordena eventos por popularidad (más vendidos primero).
        
        Args:
            algorithm: "merge" para MergeSort o "quick" para QuickSort
            
        Returns:
            Lista ordenada de eventos
        """
        temp_list = LinkedList[EventCatalog]()
        temp_list.from_list(self.events_list.to_list())
        
        if algorithm == "quick":
            temp_list.quick_sort(compare_by_popularity)
        else:
            temp_list.merge_sort(compare_by_popularity)
        
        return temp_list.to_list()

    def sort_by_availability(self) -> List[EventCatalog]:
        """Ordena eventos por disponibilidad (más entradas disponibles primero)."""
        return sorted(
            self.events_list.to_list(),
            key=lambda e: e.availability_percentage,
            reverse=True
        )

    # ==================== BÚSQUEDA BINARIA ====================

    def binary_search_by_date(self, target_date: datetime) -> Optional[EventCatalog]:
        """
        Búsqueda binaria por fecha (lista debe estar ordenada por fecha).
        
        Args:
            target_date: Fecha a buscar
            
        Returns:
            Evento con esa fecha o None
        """
        sorted_events = self.sort_by_date()
        temp_list = LinkedList[EventCatalog]()
        temp_list.from_list(sorted_events)
        
        target_event = EventCatalog(
            id=-1,
            name="",
            venue="",
            date=target_date,
            min_price=0,
            max_price=0,
            total_capacity=0
        )
        
        index = temp_list.binary_search(target_event, compare_by_date)
        return sorted_events[index] if index >= 0 else None

    def binary_search_by_price(self, target_price: float) -> Optional[EventCatalog]:
        """
        Búsqueda binaria por precio.
        
        Args:
            target_price: Precio a buscar
            
        Returns:
            Evento cercano a ese precio o None
        """
        sorted_events = self.sort_by_price()
        temp_list = LinkedList[EventCatalog]()
        temp_list.from_list(sorted_events)
        
        target_event = EventCatalog(
            id=-1,
            name="",
            venue="",
            date=datetime.now(),
            min_price=target_price,
            max_price=target_price,
            total_capacity=0
        )
        
        index = temp_list.binary_search(target_event, compare_by_price)
        return sorted_events[index] if index >= 0 else None

    # ==================== UTILIDADES ====================

    def get_statistics(self) -> dict:
        """Obtiene estadísticas generales del catálogo."""
        events = self.get_all_events()
        if not events:
            return {
                "total_events": 0,
                "upcoming_events": 0,
                "sold_out_events": 0,
                "total_capacity": 0,
                "total_sold": 0,
                "avg_ticket_price": 0,
            }

        upcoming = sum(1 for e in events if e.is_upcoming())
        sold_out = sum(1 for e in events if e.is_sold_out())
        total_capacity = sum(e.total_capacity for e in events)
        total_sold = sum(e.sold_tickets for e in events)
        total_price = sum(e.min_price * e.total_capacity for e in events)

        return {
            "total_events": len(events),
            "upcoming_events": upcoming,
            "sold_out_events": sold_out,
            "total_capacity": total_capacity,
            "total_sold": total_sold,
            "avg_ticket_price": total_price / total_capacity if total_capacity > 0 else 0,
            "occupancy_percentage": (total_sold / total_capacity * 100) if total_capacity > 0 else 0,
        }

    def get_trending_events(self, limit: int = 10) -> List[EventCatalog]:
        """
        Obtiene los eventos más vendidos (trending).
        
        Args:
            limit: Número de eventos a retornar
            
        Returns:
            Lista de eventos más populares
        """
        sorted_by_pop = self.sort_by_popularity()
        return sorted_by_pop[:limit]

    def get_featured_events(self, limit: int = 5) -> List[EventCatalog]:
        """
        Obtiene eventos destacados (próximos y con disponibilidad).
        
        Args:
            limit: Número de eventos a retornar
            
        Returns:
            Lista de eventos destacados
        """
        upcoming = self.search_upcoming_events()
        available = [e for e in upcoming if not e.is_sold_out()]
        sorted_by_date = sorted(available, key=lambda e: e.date)
        return sorted_by_date[:limit]

    def __len__(self) -> int:
        """Retorna el número total de eventos en el catálogo."""
        return len(self.events_list)

    def __repr__(self) -> str:
        return f"EventCatalogService(total_events={len(self)})"
