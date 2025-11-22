"""
Modelos de dominio para el Catálogo Dinámico de Eventos.
Componente de Cerna Sifuentes - Estructura de Datos
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


class SortCriteria(Enum):
    """Criterios de ordenamiento para eventos."""
    BY_DATE = "date"
    BY_PRICE = "price"
    BY_POPULARITY = "popularity"


@dataclass
class EventCatalog:
    """
    Modelo de dominio para un evento en el catálogo.
    Contiene toda la información necesaria para ordenamiento y búsqueda.
    """
    id: int
    name: str
    venue: str
    date: datetime
    min_price: float  # Precio mínimo entre zonas
    max_price: float  # Precio máximo entre zonas
    total_capacity: int
    sold_tickets: int = 0  # Para calcular popularidad
    description: str = ""
    artist_name: str = ""
    
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True

    @property
    def popularity_score(self) -> float:
        """
        Calcula score de popularidad basado en tickets vendidos.
        Rango: 0.0 a 100.0
        """
        if self.total_capacity == 0:
            return 0.0
        return (self.sold_tickets / self.total_capacity) * 100

    @property
    def availability_percentage(self) -> float:
        """Porcentaje de tickets disponibles."""
        if self.total_capacity == 0:
            return 0.0
        return ((self.total_capacity - self.sold_tickets) / self.total_capacity) * 100

    def is_sold_out(self) -> bool:
        """Verifica si el evento está agotado."""
        return self.sold_tickets >= self.total_capacity

    def is_upcoming(self) -> bool:
        """Verifica si el evento es futuro."""
        return self.date > datetime.now()

    def days_until(self) -> int:
        """Días hasta el evento."""
        if not self.is_upcoming():
            return 0
        delta = self.date - datetime.now()
        return delta.days

    def __eq__(self, other):
        """Comparación por ID."""
        if isinstance(other, EventCatalog):
            return self.id == other.id
        return False

    def __hash__(self):
        """Hash basado en ID."""
        return hash(self.id)

    def __repr__(self) -> str:
        return (f"EventCatalog(id={self.id}, name='{self.name}', "
                f"date={self.date.strftime('%Y-%m-%d')}, "
                f"popularity={self.popularity_score:.1f}%)")


# Funciones comparadoras para ordenamiento
def compare_by_date(event1: EventCatalog, event2: EventCatalog) -> int:
    """Comparador para ordenar por fecha (ascendente)."""
    if event1.date < event2.date:
        return -1
    elif event1.date > event2.date:
        return 1
    return 0


def compare_by_price(event1: EventCatalog, event2: EventCatalog) -> int:
    """Comparador para ordenar por precio mínimo (ascendente)."""
    if event1.min_price < event2.min_price:
        return -1
    elif event1.min_price > event2.min_price:
        return 1
    return 0


def compare_by_popularity(event1: EventCatalog, event2: EventCatalog) -> int:
    """Comparador para ordenar por popularidad (descendente)."""
    pop1 = event1.popularity_score
    pop2 = event2.popularity_score
    if pop1 > pop2:  # Descendente
        return -1
    elif pop1 < pop2:
        return 1
    return 0


def compare_by_availability(event1: EventCatalog, event2: EventCatalog) -> int:
    """Comparador para ordenar por disponibilidad (descendente)."""
    avail1 = event1.availability_percentage
    avail2 = event2.availability_percentage
    if avail1 > avail2:
        return -1
    elif avail1 < avail2:
        return 1
    return 0


# Mapeo de criterios a funciones comparadoras
COMPARATORS = {
    SortCriteria.BY_DATE: compare_by_date,
    SortCriteria.BY_PRICE: compare_by_price,
    SortCriteria.BY_POPULARITY: compare_by_popularity,
}
