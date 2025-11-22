from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    direccion = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.name} - {self.venue}"


class Zone(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="zones")
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stage = models.CharField(max_length=50, default="regular")
    filas = models.PositiveIntegerField(default=1)
    columnas = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ['event', 'code']
        ordering = ['event', 'code']

    def __str__(self):
        return f"{self.event.name} - {self.name}"


class Asiento(models.Model):
    zona = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name="asientos")
    fila = models.CharField(max_length=10)
    columna = models.PositiveIntegerField()

    class Meta:
        unique_together = ('zona', 'fila', 'columna')

    def __str__(self):
        return f"{self.zona.name} - {self.fila}-{self.columna} (id:{self.id})"