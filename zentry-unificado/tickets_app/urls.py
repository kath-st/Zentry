from django.urls import path
from . import views

urlpatterns = [
    # 1. Endpoint principal para el personal de control
    path('validar-acceso/', views.validar_acceso, name='validar_acceso_api'),
    
    # 2. Endpoint opcional para monitorear la fila (uso de la Cola)
    path('fila-ingreso/', views.ver_fila_ingreso, name='ver_fila_api'),
]