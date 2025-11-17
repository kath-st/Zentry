"""
Tests para el Catálogo Dinámico de Eventos.
Cerna Sifuentes - Estructura de Datos
"""

import pytest
from datetime import datetime, timedelta
from core.datastructures.linked_list import LinkedList
from core.domain.event_catalog import EventCatalog, compare_by_date, compare_by_price
from core.services.event_catalog_service import EventCatalogService


@pytest.fixture
def sample_events():
    """Crea eventos de ejemplo para las pruebas."""
    now = datetime.now()
    return [
        EventCatalog(
            id=1, name="Rock Night 2024", venue="Estadio Nacional",
            date=now + timedelta(days=7), min_price=50.0, max_price=150.0,
            total_capacity=5000, sold_tickets=2500, artist_name="The Beatles"
        ),
        EventCatalog(
            id=2, name="Jazz Evening", venue="Teatro Principal",
            date=now + timedelta(days=14), min_price=80.0, max_price=200.0,
            total_capacity=1000, sold_tickets=800, artist_name="Miles Davis"
        ),
        EventCatalog(
            id=3, name="Pop Fest", venue="Anfiteatro Metropolitano",
            date=now + timedelta(days=21), min_price=30.0, max_price=100.0,
            total_capacity=8000, sold_tickets=500, artist_name="Taylor Swift"
        ),
        EventCatalog(
            id=4, name="Classical Symphony", venue="Opera House",
            date=now + timedelta(days=3), min_price=120.0, max_price=250.0,
            total_capacity=1500, sold_tickets=1500, artist_name="Philharmonic"
        ),
    ]


@pytest.fixture
def catalog_service():
    """Crea una instancia del servicio de catálogo."""
    return EventCatalogService()


class TestLinkedList:
    """Tests para LinkedList."""

    def test_insert_and_retrieve(self):
        ll = LinkedList()
        ll.insert(1)
        ll.insert(2)
        ll.insert(3)
        assert len(ll) == 3
        assert ll.get(0) == 1
        assert ll.get(2) == 3

    def test_delete(self):
        ll = LinkedList()
        ll.insert(1)
        ll.insert(2)
        ll.insert(3)
        assert ll.delete(2) is True
        assert len(ll) == 2

    def test_filter(self):
        ll = LinkedList()
        for i in range(1, 11):
            ll.insert(i)
        even_ll = ll.filter(lambda x: x % 2 == 0)
        assert len(even_ll) == 5

    def test_merge_sort(self):
        ll = LinkedList()
        for val in [5, 2, 8, 1, 9, 3]:
            ll.insert(val)
        def compare(a, b): return -1 if a < b else (1 if a > b else 0)
        ll.merge_sort(compare)
        assert ll.to_list() == [1, 2, 3, 5, 8, 9]

    def test_quick_sort(self):
        ll = LinkedList()
        for val in [5, 2, 8, 1, 9, 3]:
            ll.insert(val)
        def compare(a, b): return -1 if a < b else (1 if a > b else 0)
        ll.quick_sort(compare)
        assert ll.to_list() == [1, 2, 3, 5, 8, 9]


class TestEventCatalogService:
    """Tests para EventCatalogService."""

    def test_add_event(self, catalog_service, sample_events):
        event = sample_events[0]
        added = catalog_service.add_event(event)
        assert added.id == 1
        assert len(catalog_service) == 1

    def test_add_duplicate_raises_error(self, catalog_service, sample_events):
        event = sample_events[0]
        catalog_service.add_event(event)
        with pytest.raises(ValueError):
            catalog_service.add_event(event)

    def test_get_event(self, catalog_service, sample_events):
        event = sample_events[0]
        catalog_service.add_event(event)
        retrieved = catalog_service.get_event(1)
        assert retrieved is not None
        assert retrieved.id == 1

    def test_delete_event(self, catalog_service, sample_events):
        event = sample_events[0]
        catalog_service.add_event(event)
        success = catalog_service.delete_event(1)
        assert success is True
        assert len(catalog_service) == 0

    def test_search_by_name(self, catalog_service, sample_events):
        for event in sample_events:
            catalog_service.add_event(event)
        results = catalog_service.search_by_name("rock")
        assert len(results) == 1
        assert results[0].id == 1

    def test_search_upcoming(self, catalog_service, sample_events):
        for event in sample_events:
            catalog_service.add_event(event)
        results = catalog_service.search_upcoming_events()
        assert len(results) == 4

    def test_sort_by_date(self, catalog_service, sample_events):
        for event in sample_events:
            catalog_service.add_event(event)
        sorted_events = catalog_service.sort_by_date()
        for i in range(len(sorted_events) - 1):
            assert sorted_events[i].date <= sorted_events[i + 1].date

    def test_sort_by_price(self, catalog_service, sample_events):
        for event in sample_events:
            catalog_service.add_event(event)
        sorted_events = catalog_service.sort_by_price()
        for i in range(len(sorted_events) - 1):
            assert sorted_events[i].min_price <= sorted_events[i + 1].min_price

    def test_sort_by_popularity(self, catalog_service, sample_events):
        for event in sample_events:
            catalog_service.add_event(event)
        sorted_events = catalog_service.sort_by_popularity()
        for i in range(len(sorted_events) - 1):
            assert sorted_events[i].popularity_score >= sorted_events[i + 1].popularity_score

    def test_get_statistics(self, catalog_service, sample_events):
        for event in sample_events:
            catalog_service.add_event(event)
        stats = catalog_service.get_statistics()
        assert stats['total_events'] == 4
        assert stats['total_capacity'] == 15500

    def test_trending_events(self, catalog_service, sample_events):
        for event in sample_events:
            catalog_service.add_event(event)
        trending = catalog_service.get_trending_events(limit=2)
        assert len(trending) == 2
