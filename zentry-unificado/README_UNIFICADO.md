# Zentry - Sistema Unificado de Gestión de Eventos

Sistema backend Django unificado que integra todos los módulos del equipo de desarrollo:

## Módulos Integrados

### Catálogo de Eventos (Cerna)
- **Ubicación**: `core/`, `events/`, `api/`
- **Funcionalidad**: Gestión y visualización de catálogo dinámico de eventos
- **Endpoints**: `/api/catalog/`
- **Estructuras de datos**: Implementaciones personalizadas para optimización

### Gestión de Usuarios (Diana)
- **Ubicación**: `usuarios/`
- **Funcionalidad**: Autenticación, perfiles de usuario (Organizador, Comprador, Validador)
- **Endpoints**: `/auth/`
- **Modelo**: Usuario personalizado que extiende AbstractUser

### Carrito de Compras con Undo (Katherine/Cerna)
- **Ubicación**: `cart/`, `core/services/cart_service.py`
- **Funcionalidad**: Carrito con funcionalidad de deshacer usando Stack
- **Endpoints**: `/api/cart/`
- **Estructuras de datos**: Pila (Stack) para undo operations

### Sistema de Reservas y Asientos (Módulo2)
- **Ubicación**: `reservas_modulo2/`
- **Funcionalidad**: Gestión de reservas con sesiones de compra y expiración automática
- **Endpoints**: `/reservas/`
- **Estructuras de datos**: Lista doblemente enlazada, colas, heap mínimo, quicksort, búsqueda binaria

### Control de Acceso (Rony)
- **Ubicación**: `tickets_app/`
- **Funcionalidad**: Validación de tickets con códigos numéricos (sin QR)
- **Endpoints**: `/control-acceso/`
- **Estructuras de datos**: Hash Set (O(1)), Cola (deque) para fila de ingreso

## Estructura de URLs

```
/admin/                 # Administración Django
/api/catalog/          # Catálogo de eventos
/api/cart/             # Carrito de compras
/auth/                 # Autenticación y usuarios
/reservas/             # Sistema de reservas y asientos  
/control-acceso/       # Validación de tickets
```

## Configuración

### Requisitos
- Python 3.13+
- Django 5.x
- Django REST Framework

### Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Aplicar migraciones:
```bash
python manage.py migrate
```

3. Crear superusuario:
```bash
python manage.py createsuperuser
```

4. Ejecutar servidor:
```bash
python manage.py runserver
```

## Apps del Proyecto

- `core`: Servicios centrales y estructuras de datos compartidas
- `events`: Modelos de eventos del sistema principal
- `reservations`: Sistema de reservas base
- `cart`: Carrito de compras con undo
- `usuarios`: Gestión de usuarios con roles
- `reservas_modulo2`: Sistema avanzado de reservas con sesiones
- `tickets_app`: Control de acceso y validación de tickets

## Arquitectura

El proyecto mantiene la lógica de negocio original de cada módulo intacta, únicamente reorganizando la estructura de archivos e integrando las configuraciones necesarias.

### Características Preservadas:
- Estructuras de datos originales de cada módulo
- Algoritmos y lógica de negocio sin modificaciones  
- Funcionalidades específicas de cada equipo
- Optimizaciones de rendimiento (O(1), heap, etc.)

### Integración Realizada:
- Unificación de proyecto Django
- Configuración centralizada de URLs y settings
- Modelo de usuario unificado (AUTH_USER_MODEL)
- Estructura de API coherente

## Testing

Ejecutar tests:
```bash
python -m pytest
```

## Contribuidores

- **Cerna**: Catálogo de eventos y carrito base
- **Diana**: Sistema de usuarios y autenticación  
- **Módulo2**: Sistema avanzado de reservas
- **Katherine**: Funcionalidad de undo para carrito
- **Rony**: Control de acceso con códigos numéricos

## Notas de Integración

Ver `INTEGRACION_PENDIENTES.md` para detalles sobre diferencias de modelos y posibles mejoras futuras de integración entre módulos.