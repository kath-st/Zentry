from django.db import models
from django.conf import settings
from events.models import Event, Zone
from reservations.models import Reservation


class CartItemModel(models.Model):
    """Modelo Django para items del carrito de compras."""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart_items")
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    reservation = models.ForeignKey(Reservation, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "event", "zone"], name="unique_cart_line_per_user")
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.event.name} - {self.zone.code} ({self.qty})"

    @property
    def total_price(self):
        """Calcula el precio total de este item del carrito."""
        return self.qty * self.unit_price