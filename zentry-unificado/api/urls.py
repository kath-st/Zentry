from django.urls import path, include

urlpatterns = [
    # Catálogo de eventos (Cerna)
    path('catalog/', include('api.routes_catalog')),
    
    # Carrito de compras (Cerna/Katherine)
    path('', include('cart.urls')),
]