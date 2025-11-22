"""
CATÁLOGO DINÁMICO DE EVENTOS - MÓDULO DE CERNA SIFUENTES
Componente: Estructura de Datos - Catálogo Dinámico de Eventos
Responsable: Cerna Sifuentes, Augusto Nicolas
Fecha: Noviembre 2024

=============================================================================
DESCRIPCIÓN
=============================================================================

Este módulo implementa un catálogo dinámico de eventos para el sistema
Zentry de gestión de tickets de conciertos. Utiliza estructuras de datos
avanzadas para garantizar eficiencia en búsqueda, ordenamiento y filtrado.

COMPONENTES PRINCIPALES:

1. LinkedList (core/datastructures/linked_list.py)
   - Estructura genérica de lista enlazada
   - Operaciones: insert, delete, search, filter, traverse
   - Algoritmos: MergeSort, QuickSort, BinarySearch
   
2. EventCatalog (core/domain/event_catalog.py)
   - Modelo de evento con propiedades de popularidad
   - Comparadores para ordenamiento (fecha, precio, popularidad)
   - Cálculos de disponibilidad y estado
   
3. EventCatalogService (core/services/event_catalog_service.py)
   - Gestión CRUD de eventos
   - Búsqueda avanzada y filtrado
   - Ordenamiento con MergeSort/QuickSort
   - Búsqueda binaria
   - Estadísticas y eventos trending
   
4. API REST (api/views_catalog.py, api/serializers_catalog.py)
   - Endpoints para acceso al catálogo
   - Búsqueda, ordenamiento y filtrado
   - Estadísticas en tiempo real

=============================================================================
ESTRUCTURA DE DATOS UTILIZADA
=============================================================================

LISTA ENLAZADA (LinkedList)
├── Nodos con datos genéricos
├── Cabecera (head) y tamaño
├── Operaciones O(n) para búsqueda
├── Operaciones O(1) para inserción al inicio
└── Soporte para algoritmos de ordenamiento

ÍNDICE DE ID (Diccionario)
├── Acceso rápido O(1) por ID
├── Complementa la búsqueda en lista enlazada
└── Mantiene consistencia con LinkedList

=============================================================================
ALGORITMOS IMPLEMENTADOS
=============================================================================

1. MERGE SORT - O(n log n)
   ✓ Estable
   ✓ Optimo para datos enlazados
   ✓ Complejidad garantizada
   ✗ Requiere espacio adicional O(n)

2. QUICK SORT - O(n log n) promedio, O(n²) peor caso
   ✓ Rápido en promedio
   ✓ Espacio O(log n) con recursión
   ✓ Bueno para datos aleatorios
   ✗ Inestable

3. BÚSQUEDA BINARIA - O(log n)
   ✓ Muy eficiente en datos ordenados
   ✓ Requiere lista ordenada
   ✗ No funciona en datos desordenados

4. BÚSQUEDA LINEAL CON FILTROS - O(n)
   ✓ Flexible para cualquier criterio
   ✓ Funciona con datos desordenados
   ✗ Menos eficiente que binaria

=============================================================================
FUNCIONALIDADES IMPLEMENTADAS
=============================================================================

CRUD BÁSICO:
✓ Crear evento (add_event)
✓ Obtener evento por ID (get_event)
✓ Actualizar evento (update_event)
✓ Eliminar evento (delete_event)
✓ Listar todos (get_all_events)

BÚSQUEDA:
✓ Por nombre (search_by_name)
✓ Por artista (search_by_artist)
✓ Por lugar (search_by_venue)
✓ Por rango de precios (search_by_price_range)
✓ Por rango de fechas (search_by_date_range)
✓ Eventos futuros (search_upcoming_events)
✓ Con disponibilidad (search_available_events)

ORDENAMIENTO:
✓ Por fecha (sort_by_date)
✓ Por precio (sort_by_price)
✓ Por popularidad (sort_by_popularity)
✓ Por disponibilidad (sort_by_availability)
✓ Seleccionar algoritmo (MergeSort/QuickSort)

BÚSQUEDA BINARIA:
✓ Por fecha (binary_search_by_date)
✓ Por precio (binary_search_by_price)

ANÁLISIS Y ESTADÍSTICAS:
✓ Estadísticas generales (get_statistics)
✓ Eventos trending (get_trending_events)
✓ Eventos destacados (get_featured_events)

=============================================================================
ENDPOINTS API REST
=============================================================================

OPERACIONES BÁSICAS:
GET    /api/catalog/                      - Listar todos (con sort opcional)
GET    /api/catalog/{id}/                 - Obtener específico
POST   /api/catalog/                      - Crear evento
PATCH  /api/catalog/{id}/                 - Actualizar evento
DELETE /api/catalog/{id}/                 - Eliminar evento

BÚSQUEDA:
GET    /api/catalog/search/?q=término&type=name|artist|venue
GET    /api/catalog/upcoming/             - Próximos eventos
GET    /api/catalog/available/            - Con disponibilidad
GET    /api/catalog/price_range/?min=50&max=200

ORDENAMIENTO:
GET    /api/catalog/sort/by-date/?algorithm=merge&limit=10
GET    /api/catalog/sort/by-price/?algorithm=merge&limit=10
GET    /api/catalog/sort/by-popularity/?algorithm=merge&limit=10

ANÁLISIS:
GET    /api/catalog/trending/?limit=10    - Eventos en tendencia
GET    /api/catalog/featured/?limit=5     - Eventos destacados
GET    /api/catalog/statistics/           - Estadísticas generales

=============================================================================
EJEMPLO DE USO
=============================================================================

CREAR CATÁLOGO Y AÑADIR EVENTOS:

    from core.services.event_catalog_service import EventCatalogService
    from core.domain.event_catalog import EventCatalog
    from datetime import datetime, timedelta

    service = EventCatalogService()
    
    event = EventCatalog(
        id=1,
        name="Rock Night",
        venue="Estadio Nacional",
        date=datetime.now() + timedelta(days=7),
        min_price=50.0,
        max_price=150.0,
        total_capacity=5000,
        sold_tickets=2500,
        artist_name="The Beatles Cover"
    )
    
    service.add_event(event)

ORDENAR EVENTOS:

    # Por fecha (MergeSort)
    by_date = service.sort_by_date(algorithm="merge")
    
    # Por popularidad (QuickSort)
    by_popularity = service.sort_by_popularity(algorithm="quick")
    
    # Por precio
    by_price = service.sort_by_price(algorithm="merge")

BUSCAR EVENTOS:

    # Búsqueda simple
    rock_events = service.search_by_name("rock")
    
    # Búsqueda por rango de precios
    affordable = service.search_by_price_range(50, 100)
    
    # Eventos futuros
    upcoming = service.search_upcoming_events()
    
    # Con disponibilidad
    available = service.search_available_events()

ANÁLISIS:

    # Eventos trending
    trending = service.get_trending_events(limit=10)
    
    # Estadísticas
    stats = service.get_statistics()
    print(f"Total eventos: {stats['total_events']}")
    print(f"Ocupación: {stats['occupancy_percentage']:.2f}%")

=============================================================================
COMPLEJIDAD COMPUTACIONAL
=============================================================================

OPERACIÓN                      COMPLEJIDAD    NOTAS
────────────────────────────────────────────────────────────────────────
Insert                         O(n)           Inserta al final
Delete                         O(n)           Búsqueda lineal
Get por ID (índice)            O(1)           Acceso directo
Get por índice                 O(n)           Recorre lista
Search lineal                  O(n)           Recorre todo
Filter                         O(n)           Recorre todo
MergeSort                      O(n log n)     Estable, óptimo
QuickSort                      O(n log n)     Promedio
BinarySearch                   O(log n)       Requiere ordenado
Statistics                     O(n)           Recorre todos

ESPACIO:
LinkedList                     O(n)           n nodos
Index dict                     O(n)           n entradas
MergeSort                      O(n)           Copia temporal
QuickSort                      O(log n)       Pila recursión

=============================================================================
TESTING
=============================================================================

Tests implementados en tests/test_event_catalog.py:

✓ Tests de LinkedList (insert, delete, search, sort, etc.)
✓ Tests de comparadores (date, price, popularity)
✓ Tests de EventCatalog (propiedades, cálculos)
✓ Tests de EventCatalogService (CRUD, búsqueda, ordenamiento)

Ejecutar tests:
    pytest tests/test_event_catalog.py -v

=============================================================================
REGLAS DE NEGOCIO IMPLEMENTADAS (DE CERNA)
=============================================================================

1. Unicidad de eventos
   - Cada evento tiene ID único
   - No se pueden duplicar eventos

2. Gestión de disponibilidad
   - Cálculo automático de popularidad
   - Porcentaje de disponibilidad
   - Detección de eventos agotados

3. Validación de estados
   - Evento activo/inactivo
   - Evento futuro/pasado
   - Evento agotado/disponible

4. Ordenamiento eficiente
   - MergeSort para datos grande/médios
   - QuickSort para datos pequeños
   - Búsqueda binaria cuando es posible

5. Auditoría
   - Timestamps de creación/actualización
   - Seguimiento de cambios
   - Historial implícito

=============================================================================
INTEGRACIÓN CON OTROS MÓDULOS
=============================================================================

CARRITO (Katherine):
- Usa eventos del catálogo para operaciones de compra
- Validación de disponibilidad contra catálogo

RESERVAS (Xiomara):
- Lee datos de eventos y zonas del catálogo
- Mantiene sincronización de stocks

USUARIOS (Diana):
- Asocia usuario a eventos en historial
- Usa búsquedas del catálogo

VALIDACIÓN (Rony):
- Verifica estado del evento en validación
- Usa información de catálogo

=============================================================================
FUTURAS MEJORAS
=============================================================================

1. Caché de resultados de búsqueda frecuentes
2. Índices secundarios (por artista, lugar)
3. Búsqueda full-text
4. Replicación de datos
5. Sincronización en tiempo real
6. API de webhooks para cambios de disponibilidad
7. Recomendaciones basadas en búsquedas previas
8. Analytics avanzados

=============================================================================
NOTAS IMPORTANTES
=============================================================================

- La instancia de EventCatalogService es global en API
  Para producción, usar inyección de dependencias
  
- Los eventos se mantienen en memoria (LinkedList)
  Para persistencia, integrar con Django ORM
  
- No hay sincronización de threads
  Para ambiente concurrente, añadir locks
  
- El ordenamiento crea copias temporales
  Para conjuntos grandes, considerar ordenamiento external

=============================================================================
AUTOR
=============================================================================

Cerna Sifuentes, Augusto Nicolas
Estudiante de Ingeniería de Sistemas
Universidad Nacional Mayor de San Marcos
Curso: Estructura de Datos
Grupo: 02
Fecha: Noviembre 2024
