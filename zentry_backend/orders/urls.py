from django.urls import path
from .views import (
    CheckoutView, JoinQueueView, UndoCartView, MyTicketsView,
    AddToCartView, ReleaseReservationView, CleanExpiredReservationsView,
    DownloadTicketPDFView
)

urlpatterns = [
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/release/', ReleaseReservationView.as_view(), name='release-reservation'),
    path('cart/undo/', UndoCartView.as_view(), name='undo-cart'),
    path('cart/clean-expired/', CleanExpiredReservationsView.as_view(), name='clean-expired'),
    path('queue/join/', JoinQueueView.as_view(), name='join-queue'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('my-tickets/', MyTicketsView.as_view(), name='my-tickets'),
    path('tickets/<int:ticket_id>/download/', DownloadTicketPDFView.as_view(), name='download-ticket-pdf'),
]