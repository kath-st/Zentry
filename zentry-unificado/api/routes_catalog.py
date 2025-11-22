"""
Rutas API para el Catálogo Dinámico de Eventos.
Componente de Cerna Sifuentes - Estructura de Datos
"""

from django.urls import path, include
from rest_framework.routers import SimpleRouter
from api.views_catalog import EventCatalogViewSet

# Crear router y registrar ViewSet
router = SimpleRouter()
router.register(r'events', EventCatalogViewSet, basename='event_catalog')

urlpatterns = [
    path('', include(router.urls)),
]
