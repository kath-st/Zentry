from django.urls import path
from .views import (
    EventListView, ImportEventsView, SeatMapView, 
    EventCreateView, EventAdminDetailView, EventDetailView
)

urlpatterns = [
    # Rutas Públicas
    path('', EventListView.as_view(), name='list-events'),
    path('<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('<int:event_id>/seats/', SeatMapView.as_view(), name='seat-map'),
    
    # Rutas Admin
    path('import/tm/', ImportEventsView.as_view(), name='import-tm'),
    path('create/', EventCreateView.as_view(), name='create-event'),       # Crear
    path('<int:pk>/manage/', EventAdminDetailView.as_view(), name='manage-event'), # Editar/Borrar
]