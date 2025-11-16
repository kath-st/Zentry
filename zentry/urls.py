from django.contrib import admin
from django.urls import path, include  # <-- ¡ESTO ES CRUCIAL! Asegúrate de importar 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    # Incluye las rutas de tu aplicación tickets_app
    path('api/v1/tickets/', include('tickets_app.urls')), 
]