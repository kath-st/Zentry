from django.db import models
from django.conf import settings
from events.models import Seat

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    # CVV no se guarda por seguridad, solo se valida en el momento

class Ticket(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tickets')
    seat = models.ForeignKey(Seat, on_delete=models.PROTECT)
    ticket_code = models.CharField(max_length=10, unique=True) # El código final (ej: ZENTRY-88)

    def __str__(self):
        return self.ticket_code