from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.get_cart, name='get_cart'),
    path('cart/add/', views.add_item, name='add_cart_item'),
    path('cart/update/', views.update_qty, name='update_cart_item'),
    path('cart/remove/', views.remove_item, name='remove_cart_item'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('cart/undo/', views.undo, name='undo_cart'),
]