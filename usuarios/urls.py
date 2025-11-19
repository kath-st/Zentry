from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro_comprador, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('comprar/', views.agregar_compra, name='comprar'),
    path('admin-usuarios/', views.admin_usuarios, name='admin_usuarios'),
    path('modificar-usuario/<int:usuario_id>/', views.modificar_usuario, name='modificar_usuario'),
    path('validador/', views.validador_dashboard, name='validador_dashboard'),
]