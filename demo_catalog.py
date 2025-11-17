"""
EJEMPLO DE USO - Catálogo Dinámico de Eventos (Cerna)
Demostración completa de funcionalidades
"""

from datetime import datetime, timedelta
from core.services.event_catalog_service import EventCatalogService
from core.domain.event_catalog import EventCatalog


def main():
    """Ejemplo completo de uso del catálogo de eventos."""
    
    # ==================== INICIALIZACIÓN ====================
    print("=" * 70)
    print("CATÁLOGO DINÁMICO DE EVENTOS - DEMO")
    print("Componente de Cerna Sifuentes")
    print("=" * 70)
    
    service = EventCatalogService()
    now = datetime.now()
    
    # ==================== CREAR EVENTOS ====================
    print("\n1. CREANDO EVENTOS...")
    print("-" * 70)
    
    events_data = [
        {
            "id": 1,
            "name": "Rock Night 2024",
            "venue": "Estadio Nacional",
            "date": now + timedelta(days=7),
            "min_price": 50.0,
            "max_price": 150.0,
            "total_capacity": 5000,
            "sold_tickets": 2500,
            "artist_name": "The Beatles Cover Band"
        },
        {
            "id": 2,
            "name": "Jazz Evening",
            "venue": "Teatro Principal",
            "date": now + timedelta(days=14),
            "min_price": 80.0,
            "max_price": 200.0,
            "total_capacity": 1000,
            "sold_tickets": 800,
            "artist_name": "Miles Davis Tribute"
        },
        {
            "id": 3,
            "name": "Pop Fest 2024",
            "venue": "Anfiteatro Metropolitano",
            "date": now + timedelta(days=21),
            "min_price": 30.0,
            "max_price": 100.0,
            "total_capacity": 8000,
            "sold_tickets": 500,
            "artist_name": "Taylor Swift Cover"
        },
        {
            "id": 4,
            "name": "Classical Symphony",
            "venue": "Opera House",
            "date": now + timedelta(days=3),
            "min_price": 120.0,
            "max_price": 250.0,
            "total_capacity": 1500,
            "sold_tickets": 1500,
            "artist_name": "Philharmonic Orchestra"
        },
        {
            "id": 5,
            "name": "Electronic Beats",
            "venue": "Club Underground",
            "date": now + timedelta(days=28),
            "min_price": 25.0,
            "max_price": 60.0,
            "total_capacity": 500,
            "sold_tickets": 150,
            "artist_name": "DJ Tiësto"
        }
    ]
    
    for data in events_data:
        event = EventCatalog(**data)
        service.add_event(event)
        print(f"✓ {event.name} - {event.popularity_score:.1f}% popularidad")
    
    print(f"\nTotal de eventos en catálogo: {len(service)}")
    
    # ==================== BÚSQUEDA BÁSICA ====================
    print("\n2. BÚSQUEDA BÁSICA...")
    print("-" * 70)
    
    # Por nombre
    rock_events = service.search_by_name("rock")
    print(f"\nEventos con 'rock': {len(rock_events)}")
    for e in rock_events:
        print(f"  - {e.name} ({e.artist_name})")
    
    # Por artista
    jazz_events = service.search_by_artist("miles")
    print(f"\nEventos con artista 'miles': {len(jazz_events)}")
    for e in jazz_events:
        print(f"  - {e.name}")
    
    # ==================== FILTRADO ====================
    print("\n3. FILTRADO...")
    print("-" * 70)
    
    # Eventos próximos
    upcoming = service.search_upcoming_events()
    print(f"\nEventos próximos: {len(upcoming)}")
    for e in upcoming:
        print(f"  - {e.name} - {e.date.strftime('%Y-%m-%d')}")
    
    # Con disponibilidad
    available = service.search_available_events()
    print(f"\nEventos disponibles: {len(available)}")
    for e in available:
        print(f"  - {e.name} ({e.availability_percentage:.1f}% disponible)")
    
    # ==================== ORDENAMIENTO ====================
    print("\n4. ORDENAMIENTO...")
    print("-" * 70)
    
    # Por fecha (MergeSort)
    print("\nPor FECHA (MergeSort):")
    by_date = service.sort_by_date(algorithm="merge")
    for e in by_date:
        print(f"  - {e.date.strftime('%Y-%m-%d')}: {e.name}")
    
    # Por precio (QuickSort)
    print("\nPor PRECIO (QuickSort):")
    by_price = service.sort_by_price(algorithm="quick")
    for e in by_price:
        print(f"  - S/ {e.min_price:.2f}-{e.max_price:.2f}: {e.name}")
    
    # Por popularidad (MergeSort)
    print("\nPor POPULARIDAD (MergeSort - Descendente):")
    by_pop = service.sort_by_popularity(algorithm="merge")
    for e in by_pop:
        print(f"  - {e.popularity_score:.1f}%: {e.name}")
    
    # ==================== BÚSQUEDA AVANZADA ====================
    print("\n5. BÚSQUEDA AVANZADA...")
    print("-" * 70)
    
    # Por rango de precios
    affordable = service.search_by_price_range(30, 100)
    print(f"\nEventos entre S/30 y S/100: {len(affordable)}")
    for e in affordable:
        print(f"  - {e.name}: S/{e.min_price:.2f}-S/{e.max_price:.2f}")
    
    # ==================== ANÁLISIS Y ESTADÍSTICAS ====================
    print("\n6. ESTADÍSTICAS...")
    print("-" * 70)
    
    stats = service.get_statistics()
    print(f"""
    Total de eventos: {stats['total_events']}
    Eventos próximos: {stats['upcoming_events']}
    Eventos agotados: {stats['sold_out_events']}
    Capacidad total: {stats['total_capacity']} tickets
    Tickets vendidos: {stats['total_sold']}
    Ocupación: {stats['occupancy_percentage']:.1f}%
    Precio promedio: S/{stats['avg_ticket_price']:.2f}
    """)
    
    # ==================== EVENTOS DESTACADOS ====================
    print("\n7. EVENTOS ESPECIALES...")
    print("-" * 70)
    
    # Trending
    trending = service.get_trending_events(limit=3)
    print(f"\nEventos en Tendencia:")
    for i, e in enumerate(trending, 1):
        print(f"  {i}. {e.name} - {e.popularity_score:.1f}% vendido")
    
    # Featured
    featured = service.get_featured_events(limit=3)
    print(f"\nEventos Destacados:")
    for i, e in enumerate(featured, 1):
        print(f"  {i}. {e.name} - {e.date.strftime('%Y-%m-%d')}")
    
    # ==================== OPERACIONES CRUD ====================
    print("\n8. OPERACIONES CRUD...")
    print("-" * 70)
    
    # Obtener un evento
    event_1 = service.get_event(1)
    print(f"\nEvento ID 1: {event_1.name}")
    
    # Actualizar
    updated = service.update_event(1, sold_tickets=3000)
    print(f"✓ Actualizado - Nuevas ventas: {updated.sold_tickets}")
    
    # Estadística después de update
    print(f"  Nueva popularidad: {updated.popularity_score:.1f}%")
    
    # ==================== DEMOSTRACIÓN DE ALGORITMOS ====================
    print("\n9. COMPARACIÓN DE ALGORITMOS...")
    print("-" * 70)
    
    import time
    
    # MergeSort vs QuickSort
    print("\nOrdenamiento por fecha:")
    
    start = time.time()
    merge_result = service.sort_by_date(algorithm="merge")
    merge_time = time.time() - start
    print(f"  MergeSort: {merge_time*1000:.3f}ms")
    
    start = time.time()
    quick_result = service.sort_by_date(algorithm="quick")
    quick_time = time.time() - start
    print(f"  QuickSort: {quick_time*1000:.3f}ms")
    
    # Verificar que ambos dan el mismo resultado
    assert [e.id for e in merge_result] == [e.id for e in quick_result]
    print("  ✓ Ambos resultados son idénticos")
    
    # ==================== RESUMEN ====================
    print("\n" + "=" * 70)
    print("RESUMEN DE FUNCIONALIDADES")
    print("=" * 70)
    print("""
    ✓ Lista Enlazada para almacenamiento dinámico
    ✓ Búsqueda por nombre, artista, lugar
    ✓ Filtrado por disponibilidad, fecha, precio
    ✓ MergeSort para ordenamiento estable O(n log n)
    ✓ QuickSort para ordenamiento rápido O(n log n)
    ✓ Búsqueda binaria en datos ordenados O(log n)
    ✓ Índices rápidos por ID O(1)
    ✓ Estadísticas en tiempo real
    ✓ Eventos trending y destacados
    ✓ CRUD completo
    
    Componente: Catálogo Dinámico de Eventos
    Responsable: Cerna Sifuentes, Augusto Nicolas
    Estado: ✅ COMPLETO Y FUNCIONAL
    """)
    print("=" * 70)


if __name__ == "__main__":
    main()
