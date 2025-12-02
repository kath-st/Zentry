from django.urls import path
from .views import MapaVisualView, ReservarAsientoView

urlpatterns = [
    path('mapa/<int:event_id>/', MapaVisualView.as_view(), name='mapa'),
    path('bloquear/', ReservarAsientoView.as_view(), name='bloquear'),
]