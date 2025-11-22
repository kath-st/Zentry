from django.conf import settings
from django.db import models
from django.utils import timezone
from events.models import Event, Zone, Asiento

class PurchaseSession(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    evento = models.ForeignKey(Event, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)
    expiracion = models.DateTimeField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Session {self.id} - Usuario {self.usuario} - Evento {self.evento.id} - Activo {self.activo}"

class ReservaM2(models.Model):
    evento = models.ForeignKey(Event, on_delete=models.CASCADE)
    asiento = models.ForeignKey(Asiento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                null=True, blank=True)
    session = models.ForeignKey(PurchaseSession, on_delete=models.CASCADE, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    expiracion = models.DateTimeField()
    activo = models.BooleanField(default=True)

    class Meta:
        unique_together = ('evento', 'asiento')

    def __str__(self):
        return f"Reserva {self.id} - Evento {self.evento.id} - Asiento {self.asiento.id} - Usuario {self.usuario}"

class CompraM2(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL,
                                null=True, blank=True)
    reservas = models.ManyToManyField(ReservaM2, related_name='compras')
    creado_en = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=100, blank=True, null=True)
    monto_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Compra {self.id} - Usuario {self.usuario} - Monto {self.monto_total}"