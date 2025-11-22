# Estado de Integración

## Modelos Unificados

**Event**: Unificado en `events.Event` - Todos los módulos (EventoM2, EventoTicket) ahora usan este modelo.
**Asiento**: Movido a `events.Asiento` con FK a `events.Zone`.
**Zone**: Extendido con `filas` y `columnas` para soportar grillas de asientos.
**Migraciones**: Base de datos recreada con modelos unificados.

## Tests

**test_stack.py**: Imports corregidos.
**test_cart_undo.py**: Usa `get_user_model()` con campo `dni`.
**test_cart_integration.py**: Usa `get_user_model()` con campo `dni`.
**3 tests fallando**: Lógica de negocio, no imports.

## Sistema Django

Django 5.0.7 con Python 3.13
Servidor funcional en puerto 8000
AUTH_USER_MODEL: usuarios.Usuario
