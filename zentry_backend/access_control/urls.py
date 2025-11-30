from django.urls import path
from .views import ValidateTicketView, StatsView

urlpatterns = [
    path('validate/', ValidateTicketView.as_view(), name='validate-ticket'),
    path('stats/', StatsView.as_view(), name='scan-stats'),
]