from django.urls import path
from .views import CheckoutView, JoinQueueView, UndoCartView, MyTicketsView

urlpatterns = [
    path('queue/join/', JoinQueueView.as_view(), name='join-queue'),
    path('cart/undo/', UndoCartView.as_view(), name='undo-cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('my-tickets/', MyTicketsView.as_view(), name='my-tickets'),
]