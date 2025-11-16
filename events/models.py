from django.db import models


class Event(models.Model):
    """Modelo para eventos/conciertos."""
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.name} - {self.venue}"


class Zone(models.Model):
    """Modelo para zonas de un evento (VIP, General, etc.)."""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="zones")
    code = models.CharField(max_length=50)  # ej: "VIP", "GENERAL"
    name = models.CharField(max_length=100)  # ej: "Zona VIP", "Zona General"
    capacity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stage = models.CharField(max_length=50, default="regular")  # preventa, regular, etc.

    class Meta:
        unique_together = ['event', 'code']
        ordering = ['event', 'code']

    def __str__(self):
        return f"{self.event.name} - {self.name}"