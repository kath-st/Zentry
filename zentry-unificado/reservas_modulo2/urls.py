from django.urls import path
from . import views

urlpatterns = [
    path('iniciar-sesion-compra/', views.iniciar_sesion_compra, name='iniciar_sesion_compra'),
    path('asientos/<int:evento_id>/', views.listar_asientos_disponibles, name='listar_asientos_disponibles'),
    path('asientos/<int:evento_id>/<int:zona_id>/', views.listar_asientos_disponibles, name='listar_asientos_disponibles_zona'),
    path('seleccionar-asiento/', views.seleccionar_asiento, name='seleccionar_asiento'),
    path('eliminar-reserva/', views.eliminar_reserva, name='eliminar_reserva'),
    path('confirmar-compra/', views.confirmar_compra, name='confirmar_compra'),
]