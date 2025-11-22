"""
ARQUITECTURA DEL CATÁLOGO DINÁMICO DE EVENTOS
Componente de Cerna Sifuentes
=============================================================================

DIAGRAMA DE CAPAS:

┌────────────────────────────────────────────────────────────────────────┐
│                          API REST LAYER                                │
│  GET /api/catalog/     POST /api/catalog/     GET /api/catalog/sort/  │
│  GET /api/catalog/{id} DELETE /api/catalog/{id} GET /api/catalog/search│
└────────────────────────────────────────────────────────────────────────┘
                               ▲
                               │
┌────────────────────────────────────────────────────────────────────────┐
│                      SERIALIZATION LAYER                               │
│  EventCatalogSerializer  ◄──────────►  JSON/HTTP                       │
└────────────────────────────────────────────────────────────────────────┘
                               ▲
                               │
┌────────────────────────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                                │
│  EventCatalogService                                                   │
│  ├─ CRUD: add_event, get_event, update_event, delete_event            │
│  ├─ Búsqueda: search_by_name, search_by_artist, search_by_price_range │
│  ├─ Ordenamiento: sort_by_date, sort_by_price, sort_by_popularity    │
│  ├─ Análisis: get_statistics, get_trending_events                     │
│  └─ Utilidades: get_all_events, search_upcoming_events                │
└────────────────────────────────────────────────────────────────────────┘
           ▲                                              ▲
           │                                              │
    ┌──────┴──────┐                              ┌────────┴────────┐
    │   BÚSQUEDA  │                              │  ORDENAMIENTO   │
    │             │                              │                 │
    │ • Lineal    │                              │ • MergeSort     │
    │ • Binaria   │                              │ • QuickSort     │
    │ • Filtros   │                              │ • Comparadores  │
    └──────┬──────┘                              └────────┬────────┘
           │                                              │
┌──────────┴──────────────────────────────────────────────┴─────────────┐
│                    DATA STRUCTURES LAYER                              │
│                                                                        │
│  LinkedList[EventCatalog]          dict[int, EventCatalog]            │
│  ├─ Nodos genéricos                 └─ Índice rápido O(1)             │
│  ├─ Insert/Delete                                                      │
│  ├─ Search                                                             │
│  ├─ Filter                                                             │
│  ├─ Merge Sort                                                         │
│  ├─ Quick Sort                                                         │
│  └─ Binary Search                                                      │
└──────────────────────────────────────────────────────────────────────┘
           ▲
           │
┌──────────┴──────────────────────────────────────────────────────────┐
│                      DOMAIN MODEL LAYER                             │
│  EventCatalog                                                        │
│  ├─ id, name, venue, date                                          │
│  ├─ min_price, max_price, total_capacity                           │
│  ├─ sold_tickets, artist_name                                      │
│  ├─ Propiedades calculadas:                                        │
│  │  ├─ popularity_score: (sold/capacity) * 100                     │
│  │  ├─ availability_percentage: (available/capacity) * 100         │
│  │  ├─ is_sold_out(): bool                                         │
│  │  └─ is_upcoming(): bool                                         │
│  └─ Comparadores:                                                  │
│     ├─ compare_by_date                                             │
│     ├─ compare_by_price                                            │
│     └─ compare_by_popularity                                       │
└──────────────────────────────────────────────────────────────────┘

=============================================================================
FLUJO DE DATOS - EJEMPLO: ORDENAR EVENTOS POR FECHA

Usuario
  │
  ▼
GET /api/catalog/sort/by-date/?algorithm=merge&limit=5
  │
  ▼
[EventCatalogViewSet.sort_by_date()]
  │
  ▼
[EventCatalogService.sort_by_date(algorithm="merge")]
  │
  ├─ Obtener todos los eventos de LinkedList
  │
  ▼
[LinkedList.to_list()]  ─────────► O(n) - Recorre lista
  │
  ▼
[LinkedList.merge_sort(compare_by_date)]  ─────────► O(n log n)
  │
  ├─ Particionar recursivamente
  ├─ Comparar con compare_by_date(e1, e2)
  └─ Mergear ordenado
  │
  ▼
[Aplicar limit]  ─────────► O(limit)
  │
  ▼
[EventCatalogSerializer.to_representation()]  ─────────► O(n)
  │
  ▼
Response JSON
  │
  ▼
Usuario

COMPLEJIDAD TOTAL: O(n log n) para ordenamiento

=============================================================================
FLUJO DE DATOS - EJEMPLO: BUSCAR EVENTOS POR RANGO DE PRECIOS

Usuario
  │
  ▼
GET /api/catalog/price_range/?min=50&max=150
  │
  ▼
[EventCatalogViewSet.price_range()]
  │
  ▼
[EventCatalogService.search_by_price_range(50, 150)]
  │
  ▼
[LinkedList.filter(lambda e: e.min_price >= 50 AND e.max_price <= 150)]
  │
  ├─ Recorre cada nodo
  ├─ Evalúa predicado
  └─ Copia a nueva LinkedList si cumple
  │
  ▼
[to_list()]  ─────────► O(n)
  │
  ▼
Resultado
  │
  ▼
Usuario

COMPLEJIDAD TOTAL: O(n) - búsqueda lineal completa

=============================================================================
FLUJO DE DATOS - EJEMPLO: BÚSQUEDA BINARIA POR FECHA

Prerequisito: Datos deben estar ORDENADOS por fecha

Usuario
  │
  ▼
[EventCatalogService.binary_search_by_date(target_date)]
  │
  ├─ sort_by_date()  ─────────► O(n log n)
  │
  ▼
[LinkedList.binary_search(target, compare_by_date)]
  │
  ├─ to_list()  ─────────► O(n)
  │
  ▼
Búsqueda binaria
  │
  ├─ left = 0, right = n-1
  ├─ while left <= right:
  │   ├─ mid = (left + right) / 2
  │   ├─ if arr[mid] < target: left = mid + 1
  │   ├─ if arr[mid] > target: right = mid - 1
  │   └─ else: return mid  ✓ ENCONTRADO
  │
  ▼
Resultado (índice o -1)  ─────────► O(log n)
  │
  ▼
Usuario

COMPLEJIDAD TOTAL: O(n log n) si no está ordenado, O(log n) si ya está ordenado

=============================================================================
OPERACIONES Y COMPLEJIDAD

LECTURA (sin cambiar orden):
├─ get_all_events(): O(n)
├─ get_event(id): O(1)  [índice dict]
├─ search_by_name(q): O(n)
├─ search_by_artist(q): O(n)
├─ search_by_venue(q): O(n)
├─ search_by_price_range(): O(n)
├─ search_by_date_range(): O(n)
├─ search_upcoming_events(): O(n)
├─ search_available_events(): O(n)
└─ get_statistics(): O(n)

ORDENAMIENTO:
├─ sort_by_date(algorithm="merge"): O(n log n)
├─ sort_by_date(algorithm="quick"): O(n log n) avg, O(n²) worst
├─ sort_by_price(algorithm="merge"): O(n log n)
├─ sort_by_price(algorithm="quick"): O(n log n) avg, O(n²) worst
├─ sort_by_popularity(algorithm="merge"): O(n log n)
├─ sort_by_popularity(algorithm="quick"): O(n log n) avg, O(n²) worst
└─ sort_by_availability(): O(n log n) [Python sort]

BÚSQUEDA BINARIA (requiere estar ordenado):
├─ binary_search_by_date(): O(n log n) [sort] + O(log n) [search]
└─ binary_search_by_price(): O(n log n) [sort] + O(log n) [search]

ESCRITURA:
├─ add_event(): O(n)  [inserta al final]
├─ update_event(): O(1) [actualización in-place]
└─ delete_event(): O(n)  [busca y elimina]

ANÁLISIS:
├─ get_trending_events(): O(n log n) [sort] + O(limit)
└─ get_featured_events(): O(n) [filtro] + O(n log n) [sort]

=============================================================================
ESPACIOS EN MEMORIA

LinkedList[EventCatalog]:        O(n)
dict[int, EventCatalog]:          O(n)
MergeSort temporal:               O(n)
QuickSort (recursión):            O(log n)

TOTAL: O(n) para estructura base, O(n) adicional durante operaciones

=============================================================================
VENTAJAS DE ESTA ARQUITECTURA

1. EFICIENCIA
   ✓ Índice O(1) para acceso por ID
   ✓ MergeSort O(n log n) garantizado para grandes datasets
   ✓ Búsqueda binaria O(log n) cuando están ordenados

2. FLEXIBILIDAD
   ✓ LinkedList genérica aplicable a otros tipos
   ✓ Comparadores intercambiables
   ✓ Filtros con predicados personalizados

3. PEDAGOGÍA
   ✓ Implementación explícita de estructuras de datos
   ✓ Algoritmos visibles y comprensibles
   ✓ Análisis de complejidad clara

4. ESCALABILIDAD
   ✓ Fácil añadir nuevos criterios de búsqueda
   ✓ Nuevos comparadores sin cambiar código existente
   ✓ Índices adicionales si es necesario

5. TESTABILIDAD
   ✓ Componentes desacoplados
   ✓ Fácil crear mocks
   ✓ Tests unitarios y de integración completos

=============================================================================
LIMITACIONES Y MEJORAS FUTURAS

LIMITACIONES ACTUALES:
- LinkedList no es thread-safe (no hay sincronización)
- Datos en memoria no persisten automáticamente
- No hay caché de resultados frecuentes
- Índices secundarios limitados (solo por ID)

MEJORAS POSIBLES:
1. Caché de búsquedas frecuentes
2. Índices secundarios (árbol por artista, por lugar)
3. Sincronización con Django ORM
4. Thread-safety con locks/semáforos
5. Búsqueda full-text mejorada
6. Replicación de datos
7. API de webhooks para cambios
8. Compresión de datos históricos

=============================================================================
AUTOR: Cerna Sifuentes, Augusto Nicolas
CURSO: Estructura de Datos
GRUPO: 02
UNIVERSIDAD: Universidad Nacional Mayor de San Marcos
FECHA: Noviembre 2024
"""
