"""
GUÍA RÁPIDA DE INSTALACIÓN Y USO
Módulo: Catálogo Dinámico de Eventos (Cerna)
========================================================================

PASO 1: INSTALAR DEPENDENCIAS
========================================================================

pip install -r requirements.txt

O específicamente para este módulo:
pip install django djangorestframework pytest pytest-cov

PASO 2: CONFIGURAR DJANGO
========================================================================

1. Actualizar INSTALLED_APPS en zentry_django/settings.py:

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'core',
    'events',
    'reservations',
    'cart',
]

2. Actualizar urls.py:

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.routes_catalog')),
    path('api/', include('api.routes_cart')),
    # ... otras rutas
]

3. Ejecutar migraciones (si es necesario):

python manage.py makemigrations
python manage.py migrate

PASO 3: USAR EL MÓDULO
========================================================================

OPCIÓN A: Mediante API REST

1. Iniciar servidor Django:
   python manage.py runserver

2. Acceder a endpoints:
   - GET http://localhost:8000/api/catalog/
   - POST http://localhost:8000/api/catalog/
   - GET http://localhost:8000/api/catalog/search/?q=rock
   - GET http://localhost:8000/api/catalog/sort/by-date/
   - GET http://localhost:8000/api/catalog/statistics/

OPCIÓN B: Usar la demo interactiva

1. Ejecutar demo:
   python demo_catalog.py

   Muestra:
   ✓ Creación de eventos
   ✓ Búsqueda básica y avanzada
   ✓ Ordenamiento por múltiples criterios
   ✓ Estadísticas
   ✓ Eventos trending
   ✓ Comparación de algoritmos

OPCIÓN C: Código Python directo

from core.services.event_catalog_service import EventCatalogService
from core.domain.event_catalog import EventCatalog
from datetime import datetime, timedelta

# Crear servicio
service = EventCatalogService()

# Crear evento
event = EventCatalog(
    id=1,
    name="Rock Night",
    venue="Estadio Nacional",
    date=datetime.now() + timedelta(days=7),
    min_price=50.0,
    max_price=150.0,
    total_capacity=5000,
    sold_tickets=2500,
    artist_name="The Beatles"
)

# Operaciones
service.add_event(event)
results = service.search_by_name("rock")
sorted_events = service.sort_by_date()
stats = service.get_statistics()

PASO 4: EJECUTAR TESTS
========================================================================

Todos los tests:
python -m pytest tests/test_event_catalog.py -v

Específicos:
python -m pytest tests/test_event_catalog.py::TestLinkedList -v
python -m pytest tests/test_event_catalog.py::TestEventCatalogService -v

Con cobertura:
python -m pytest tests/test_event_catalog.py --cov=core --cov-report=html

PASO 5: EXPLORAR DOCUMENTACIÓN
========================================================================

Documentación técnica:
- CATALOGO_EVENTOS_CERNA.md

Arquitectura y diagramas:
- ARQUITECTURA_CATALOGO.md

Resumen ejecutivo:
- RESUMEN_CERNA.txt

Ejemplos de código:
- demo_catalog.py

========================================================================
EJEMPLOS DE USO POR CASO
========================================================================

CASO 1: BUSCAR EVENTOS POR NOMBRE
───────────────────────────────────

# API REST:
GET http://localhost:8000/api/catalog/search/?q=rock&type=name

# Python:
service = EventCatalogService()
results = service.search_by_name("rock")
for event in results:
    print(f"{event.name} - {event.popularity_score}%")

CASO 2: ORDENAR EVENTOS POR PRECIO
─────────────────────────────────────

# API REST:
GET http://localhost:8000/api/catalog/sort/by-price/?algorithm=merge&limit=5

# Python:
sorted_events = service.sort_by_price(algorithm="merge")
for event in sorted_events[:5]:
    print(f"{event.name}: S/{event.min_price}-{event.max_price}")

CASO 3: OBTENER EVENTOS TRENDING
──────────────────────────────────

# API REST:
GET http://localhost:8000/api/catalog/trending/?limit=10

# Python:
trending = service.get_trending_events(limit=10)
for i, event in enumerate(trending, 1):
    print(f"{i}. {event.name} - {event.popularity_score:.1f}%")

CASO 4: BÚSQUEDA AVANZADA CON RANGO DE PRECIOS
────────────────────────────────────────────────

# API REST:
GET http://localhost:8000/api/catalog/price_range/?min=50&max=150

# Python:
affordable = service.search_by_price_range(50, 150)
for event in affordable:
    print(f"{event.name}: S/{event.min_price}-S/{event.max_price}")

CASO 5: ESTADÍSTICAS GENERALES
────────────────────────────────

# API REST:
GET http://localhost:8000/api/catalog/statistics/

# Python:
stats = service.get_statistics()
print(f"Total eventos: {stats['total_events']}")
print(f"Ocupación: {stats['occupancy_percentage']:.1f}%")
print(f"Ingresos totales: S/{stats['total_capacity'] * stats['avg_ticket_price']:,.2f}")

========================================================================
ESTRUCTURA DE CARPETAS
========================================================================

zentry/
├── api/
│   ├── serializers_catalog.py      ← Serializadores
│   ├── views_catalog.py            ← Endpoints
│   └── routes_catalog.py           ← Rutas
│
├── core/
│   ├── datastructures/
│   │   ├── __init__.py
│   │   ├── linked_list.py          ← LinkedList implementación
│   │   └── stack.py
│   │
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── event_catalog.py        ← Modelo de dominio
│   │   └── models.py
│   │
│   └── services/
│       ├── __init__.py
│       └── event_catalog_service.py ← Lógica de negocio
│
├── tests/
│   ├── test_event_catalog.py       ← Tests
│   └── conftest.py
│
├── CATALOGO_EVENTOS_CERNA.md       ← Documentación técnica
├── ARQUITECTURA_CATALOGO.md        ← Diagramas y flujos
├── RESUMEN_CERNA.txt               ← Resumen ejecutivo
└── demo_catalog.py                 ← Demo interactiva

========================================================================
COMANDOS ÚTILES
========================================================================

# Ejecutar servidor Django
python manage.py runserver

# Ejecutar shell Python (con contexto Django)
python manage.py shell

# Crear superusuario admin
python manage.py createsuperuser

# Ejecutar tests
python -m pytest tests/test_event_catalog.py -v

# Tests con cobertura
python -m pytest tests/ --cov=core --cov-report=html

# Ejecutar demo
python demo_catalog.py

# Linter (verificar errores)
pylint core/services/event_catalog_service.py

# Formateador (mejorar estilo)
black core/services/event_catalog_service.py

========================================================================
SOLUCIÓN DE PROBLEMAS
========================================================================

PROBLEMA 1: "ModuleNotFoundError: No module named 'core'"
SOLUCIÓN: Asegúrate de estar en la carpeta raíz del proyecto
          cd c:\Users\Nicolas\Documents\Coding\ProyectoED_Zentry\Zentry
          python manage.py runserver

PROBLEMA 2: "ImportError: cannot import name 'LinkedList'"
SOLUCIÓN: Revisa que el archivo core/datastructures/linked_list.py exista
          y tenga el contenido correcto

PROBLEMA 3: Tests fallan
SOLUCIÓN: python -m pytest tests/test_event_catalog.py -v
          Revisa los errores específicos y reporta

PROBLEMA 4: API devuelve error 404
SOLUCIÓN: Verifica que:
          1. Server Django está corriendo (python manage.py runserver)
          2. URL es correcta
          3. routes_catalog.py está incluido en urls.py principal

========================================================================
CONTACTO Y SOPORTE
========================================================================

Responsable del módulo: Cerna Sifuentes, Augusto Nicolas
Email: a.cerna@estudiante.unmsm.edu.pe
Grupo: 02
Curso: Estructura de Datos
Universidad: Universidad Nacional Mayor de San Marcos

========================================================================
"""
