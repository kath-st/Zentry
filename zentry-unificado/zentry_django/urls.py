"""
URL Configuration for zentry_django project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/auth/login/', permanent=False)),
    path('admin/', admin.site.urls),
    path('eventos/', include('usuarios.urls')),
    # API principal (catálogo y carrito)
    path('api/', include('api.urls')),
    # Módulo de usuarios (Diana)
    path('auth/', include('usuarios.urls')),
    # Módulo de reservas y asientos (Módulo2)
    path('reservas/', include('reservas_modulo2.urls')),
    # Módulo de control de acceso (Rony)
    path('control-acceso/', include('tickets_app.urls')),
]