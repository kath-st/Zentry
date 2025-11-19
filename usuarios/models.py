from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    TIPOS_USUARIO = (
        ('ORGANIZADOR', 'Organizador'),
        ('COMPRADOR', 'Comprador'),
        ('VALIDADOR', 'Validador'),
    )
    tipo = models.CharField(max_length=20, choices=TIPOS_USUARIO, default='COMPRADOR')
    telefono = models.CharField(max_length=15, blank=True)
    dni = models.CharField(max_length=8, unique=True, blank=False)
    fecha_nacimiento = models.DateField("Fecha de nacimiento", blank=False, help_text="Formato: AAAA-MM-DD", null=True)

    @property
    def edad(self):
        hoy = date.today()
        edad = hoy.year - self.fecha_nacimiento.year
        if hoy.month < self.fecha_nacimiento.month or (hoy.month == self.fecha_nacimiento.month and hoy.day < self.fecha_nacimiento.day):
            edad -= 1
        return edad
    
    def es_organizador(self):
        return self.tipo == 'ORGANIZADOR'
    
    def es_comprador(self):
        return self.tipo == 'COMPRADOR'
    
    def es_validador(self):
        return self.tipo == 'VALIDADOR'


class Compra(models.Model):
    """Modelo persistente para compras realizadas por los usuarios.

    Se usa para poblar la `Pila` en memoria al iniciar la app y para
    mantener un historial persistente en la base de datos.
    """
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='compras')
    producto = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.producto} ({self.monto})"