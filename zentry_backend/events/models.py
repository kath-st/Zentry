from django.db import models

class Event(models.Model):
    # ID original de Ticketmaster
    tm_id = models.CharField(max_length=50, unique=True)
    
    title = models.CharField(max_length=200)
    image_url = models.URLField() # Ticketmaster nos da una URL, no el archivo
    date = models.DateTimeField()
    venue = models.CharField(max_length=200) # Lugar del evento
    category = models.CharField(max_length=100)
    
    # Precios simulados (TM no siempre da el precio exacto fácil)
    price_min = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)

    def __str__(self):
        return self.title

class Zone(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='zones')
    name = models.CharField(max_length=50) # Ej: "General", "VIP"
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Seat(models.Model):
    STATUS_CHOICES = (('AVAILABLE', 'Disponible'), ('SOLD', 'Ocupado'))
    
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='seats')
    row_label = models.CharField(max_length=5) # F1, F2
    number = models.IntegerField() # 1, 2, 3
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='AVAILABLE')

    class Meta:
        ordering = ['row_label', 'number']