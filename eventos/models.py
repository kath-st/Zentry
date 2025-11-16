from django.conf import settings
from django.db import models
from django.utils import timezone

class Ubicacion(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Zona(models.Model):
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)  # VIP, Preferencial, General
    filas = models.PositiveIntegerField(default=1)    # número de filas (convertidas a letras)
    columnas = models.PositiveIntegerField(default=1) # número de columnas por fila

    def capacidad(self):
        return self.filas * self.columnas

    def __str__(self):
        return f"{self.ubicacion.nombre} - {self.nombre} (capacidad={self.capacidad()})"

class Evento(models.Model):
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    fecha = models.DateTimeField()
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} ({self.fecha})"

class Asiento(models.Model):
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE)
    fila = models.CharField(max_length=10)   # p.ej. "A", "B", "AA"
    columna = models.PositiveIntegerField()  # p.ej. 1,2,3...

    class Meta:
        unique_together = ('zona', 'fila', 'columna')

    def __str__(self):
        return f"{self.zona.nombre} - {self.fila}-{self.columna} (id:{self.id})"

class PrecioPorZona(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('evento', 'zona')

    def __str__(self):
        return f"{self.evento.titulo} - {self.zona.nombre} : {self.precio}"

class PurchaseSession(models.Model):
    """
    Sesión de compra global para un usuario y un evento.
    Todas las reservas creadas durante esta sesión heredarán expiracion=session.expiracion.
    """
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)
    expiracion = models.DateTimeField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Session {self.id} - Usuario {self.usuario} - Evento {self.evento.id} - Activo {self.activo}"

class Reserva(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    asiento = models.ForeignKey(Asiento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                null=True, blank=True)  # nullable para integración futura
    session = models.ForeignKey(PurchaseSession, on_delete=models.CASCADE, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    expiracion = models.DateTimeField()
    activo = models.BooleanField(default=True)

    class Meta:
        # evita dos reservas simultáneas de mismo asiento para el mismo evento
        unique_together = ('evento', 'asiento')

    def __str__(self):
        return f"Reserva {self.id} - Evento {self.evento.id} - Asiento {self.asiento.id} - Usuario {self.usuario}"

class Compra(models.Model):
    """
    Compra agrupada que asocia varias reservas.
    """
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL,
                                null=True, blank=True)
    reservas = models.ManyToManyField(Reserva, related_name='compras')
    creado_en = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=100, blank=True, null=True)
    monto_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Compra {self.id} - Usuario {self.usuario} - Monto {self.monto_total}"
