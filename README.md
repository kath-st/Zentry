# Zentry - Sistema de Tickets para Conciertos

Zentry es un sistema de gestión de tickets para conciertos desarrollado como proyecto de Estructura de Datos. El sistema ha sido migrado de Excel/pandas a Django + SQLite, manteniendo el uso explícito de estructuras de datos en memoria para cumplir con los objetivos académicos.

## 🏗️ Arquitectura

### Migración Excel → Django
- **Antes**: Repositorios basados en pandas + archivos Excel
- **Ahora**: Django ORM + SQLite con estructuras de datos en memoria

### Componentes Principales

#### 📦 Core (`core/`)
- `datastructures/stack.py`: **Stack** para funcionalidad de Undo (Katherine)
- `datastructures/linked_list.py`: **LinkedList** genérica con ordenamiento (Cerna)
- `domain/models.py`: Modelos de dominio (CartItem, Cart, excepciones)
- `domain/event_catalog.py`: Modelos para catálogo dinámico de eventos (Cerna)
- `services/event_catalog_service.py`: Servicio de catálogo con búsqueda/ordenamiento (Cerna)
- `services/`: Interfaces abstractas y servicios concretos con Django

#### 🎪 Apps Django
- **events**: Gestión de eventos y zonas
- **reservations**: Manejo de reservas de tickets  
- **cart**: Carrito de compras con Undo usando Stack

## 🚀 Funcionalidades

### 📂 Catálogo Dinámico de Eventos (Módulo de Cerna)
- ✅ **Lista Enlazada** para almacenar eventos de forma dinámica
- ✅ **Búsqueda avanzada**: por nombre, artista, lugar, rango de precios, fechas
- ✅ **Ordenamiento eficiente**: 
  - **MergeSort** (O(n log n) estable) 
  - **QuickSort** (O(n log n) promedio)
  - Por fecha, precio, popularidad
- ✅ **Búsqueda binaria**: en datos ordenados (O(log n))
- ✅ **Filtrado dinámico**: eventos próximos, disponibles, agotados
- ✅ **Estadísticas en tiempo real**: ocupación, ingresos, trending
- ✅ **Índices rápidos**: acceso O(1) por ID

### Carrito de Compras (Módulo de Katherine)
- ✅ **Añadir items** al carrito con validación de stock
- ✅ **Actualizar cantidades** con límites por usuario
- ✅ **Eliminar items** con liberación automática de reservas
- ✅ **Vaciar carrito** completo
- ✅ **UNDO**: Funcionalidad de deshacer usando Stack
- ✅ **Gestión de reservas** automática (hold/release/expire)
- ✅ **Límites de compra**: Máximo 6 entradas por usuario

### Stack de Undo
```python
# Ejemplo de uso del Stack para Undo
from core.datastructures.stack import Stack

stack = Stack(maxlen=10)  # Límite de 10 undos
stack.push(estado_anterior)
estado_restaurado = stack.pop()  # Undo
```

### API REST
- **Catálogo (Cerna)**:
  - `GET /api/catalog/` - Listar eventos (con ordenamiento)
  - `GET /api/catalog/{id}/` - Obtener evento específico
  - `POST /api/catalog/` - Crear evento
  - `GET /api/catalog/search/?q=término&type=name|artist|venue` - Búsqueda
  - `GET /api/catalog/sort/by-date/` - Ordenar por fecha
  - `GET /api/catalog/sort/by-price/` - Ordenar por precio
  - `GET /api/catalog/sort/by-popularity/` - Ordenar por popularidad
  - `GET /api/catalog/trending/?limit=10` - Eventos en tendencia
  - `GET /api/catalog/featured/?limit=5` - Eventos destacados
  - `GET /api/catalog/statistics/` - Estadísticas generales

- **Carrito (Katherine)**:
  - `GET /api/cart/` - Obtener carrito actual
  - `POST /api/cart/add/` - Añadir item
  - `POST /api/cart/update/` - Actualizar cantidad
  - `POST /api/cart/remove/` - Eliminar item  
  - `POST /api/cart/clear/` - Vaciar carrito
  - `POST /api/cart/undo/` - Deshacer última operación

## 📋 Instalación y Configuración

### Prerrequisitos
- Python 3.10+
- Django 5.0+
- Django REST Framework

### Instalación
```bash
# Clonar repositorio
git clone https://github.com/kath-st/Zentry.git
cd Zentry

# Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install django djangorestframework

# Configurar base de datos
python manage.py makemigrations
python manage.py migrate

# Crear datos de ejemplo
python init_database.py

# Ejecutar servidor
python manage.py runserver
```

### Accesos
- **Admin**: http://localhost:8000/admin/ (admin/admin123)
- **API**: http://localhost:8000/api/cart/
- **Usuario de prueba**: katherine/test123

## 🧪 Pruebas

### Ejecutar Tests
```bash
# Todas las pruebas
python -m pytest tests/ -v

# Tests del Catálogo (Cerna - LinkedList, búsqueda, ordenamiento)
python -m pytest tests/test_event_catalog.py -v

# Tests del Stack (estructura de datos)
python -m pytest tests/test_stack.py -v

# Tests de Undo del carrito (Katherine)
python -m pytest tests/test_cart_undo.py -v

# Tests de integración
python -m pytest tests/test_cart_integration.py -v

# Con cobertura
python -m pytest tests/ --cov=core --cov=api --cov-report=html
```

### Cobertura de Pruebas
- ✅ **LinkedList** (Cerna): Insert, delete, search, filter, merge sort, quick sort, binary search
- ✅ **Catálogo de Eventos** (Cerna): CRUD, búsqueda avanzada, ordenamiento, estadísticas
- ✅ **Stack**: Pruebas unitarias de push/pop/peek/overflow/underflow
- ✅ **Cart Undo** (Katherine): Todas las operaciones + undo + múltiples usuarios
- ✅ **Integración**: Flujos completos, concurrencia, consistencia de datos

## 📊 Modelo de Datos

### Modelos Django
```python
# Events
Event: nombre, fecha, venue, descripción
Zone: evento, código, capacidad, precio

# Reservations  
Reservation: usuario, evento, zona, cantidad, estado, expira_en

# Cart
CartItemModel: usuario, evento, zona, cantidad, precio, reserva
```

### Modelos de Dominio (En Memoria)
```python
# Catálogo (Cerna)
@dataclass
class EventCatalog:
    id: int
    name: str
    venue: str
    date: datetime
    min_price: float
    max_price: float
    total_capacity: int
    sold_tickets: int = 0
    artist_name: str = ""

# Carrito (Katherine)
@dataclass
class CartItem:
    event_id: int
    zone_id: str  
    qty: int
    unit_price: float
    reservation_id: str | None = None

@dataclass  
class Cart:
    user_id: str
    items: list[CartItem]
```

### Estructuras de Datos Utilizadas
```python
# Cerna - Catálogo Dinámico
LinkedList[EventCatalog]           # Almacenamiento principal
dict[int, EventCatalog]            # Índice rápido por ID

# Katherine - Carrito con Undo
Stack[Cart]                        # Historial de operaciones
list[CartItem]                     # Items del carrito actual

# Xiomara - Gestión de Asientos (Pendiente)
list[list[Seat]]                   # Matriz de asientos
CircularQueue[Reservation]         # Cola de reservas

# Diana - Registro de Usuarios (Pendiente)
dict[str, User]                    # Índice de usuarios
list[Purchase]                     # Historial de compras

# Rony - Validación de Tickets (Pendiente)
Queue[Visitor]                     # Fila de ingreso
HashSet[str]                       # Tickets validados
BinarySearchTree[Ticket]           # Búsqueda de tickets
```

## 🔄 Flujo de Operaciones

### Añadir Item al Carrito
1. **Validar** stock disponible
2. **Verificar** límite de usuario (6 entradas)
3. **Capturar** estado anterior → Stack
4. **Crear/Actualizar** item en BD
5. **Gestionar** reserva (hold)
6. **Retornar** carrito actualizado

### Operación Undo
1. **Verificar** que stack no esté vacío
2. **Obtener** estado anterior del Stack (pop)
3. **Sincronizar** BD con estado anterior:
   - Liberar reservas actuales
   - Recrear items del estado anterior
   - Gestionar reservas según disponibilidad
4. **Retornar** carrito restaurado

## 🏛️ Patrones de Diseño

- **Repository Pattern**: Abstracciones de persistencia
- **Service Layer**: Lógica de negocio separada
- **Domain Model**: Objetos de dominio independientes de la persistencia
- **Command Pattern**: Stack de operaciones para Undo
- **Iterator Pattern**: Recorrido de LinkedList
- **Strategy Pattern**: Comparadores intercambiables para ordenamiento

## 🎯 Objetivos Académicos Cumplidos

### Cerna - Catálogo Dinámico de Eventos
1. ✅ **Lista Enlazada**: Estructura genérica implementada con nodos
2. ✅ **Algoritmos de Ordenamiento**: MergeSort y QuickSort
3. ✅ **Búsqueda Binaria**: En datos ordenados O(log n)
4. ✅ **Búsqueda Lineal**: Con filtros flexibles
5. ✅ **Complejidad**: Análisis O(n log n) para ordenamiento
6. ✅ **Testing**: Pruebas completas de estructura y algoritmos

### Katherine - Carrito con Undo
1. ✅ **Estructura de Datos**: Stack implementado y usado explícitamente
2. ✅ **Operaciones**: Push/Pop para gestión de estados
3. ✅ **Manejo de Excepciones**: StackUnderflow/StackOverflow
4. ✅ **Casos de Uso Reales**: Sistema de Undo en aplicación práctica
5. ✅ **Testing Completo**: Cobertura de todos los escenarios

### Equipo - Futuras Integraciones
- ⏳ Xiomara: Matriz y Cola Circular para asientos/reservas
- ⏳ Diana: Hash y Estructura de Usuario para registro
- ⏳ Rony: Colas y ABB para validación de tickets

## 📖 Documentación Completa

- [Catálogo Dinámico de Eventos (Cerna)](./CATALOGO_EVENTOS_CERNA.md)
  - Arquitectura de LinkedList
  - Algoritmos de búsqueda y ordenamiento
  - Complejidad computacional detallada
  - Ejemplos de uso completos
  - Integración con otros módulos

## 👥 Equipo

- **Katherine**: Módulo de Carrito + Undo (Stack)
- **Equipo**: Eventos, Reservas, Integración

## 📝 Notas de Migración

### Mantenido (NO modificar)
- `datastructures/stack.py`
- `tests/test_stack.py`  
- `domain/models.py` (dataclasses)
- Interfaces abstractas de servicios

### Migrado/Reemplazado
- ❌ Repositorios Excel → ✅ Django ORM
- ❌ pandas/openpyxl → ✅ SQLite
- ❌ `app.py` vacío → ✅ Django project
- ❌ Tests Excel → ✅ Django TestCase

### Nuevo
- ✅ `CartService` completo con Django + Stack
- ✅ API REST para carrito
- ✅ Tests de integración Django
- ✅ Gestión automática de reservas

---

**Zentry v2.0** - Migrado a Django manteniendo estructuras de datos académicas 🎓
