from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from events.models import Event, Zone


class Reservation(models.Model):
    """Modelo para reservas de entradas."""
    
    STATUS_CHOICES = [
        ("held", "Held"),
        ("sold", "Sold"),
        ("cancelled", "Cancelled"),
        ("expired", "Expired"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="held")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.event.name} - {self.zone.code} ({self.qty})"

    def is_expired(self):
        """Verifica si la reserva ha expirado."""
        return timezone.now() > self.expires_at

    def save(self, *args, **kwargs):
        # Si no se especifica expires_at, establecer 15 minutos por defecto
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=15)
        super().save(*args, **kwargs)