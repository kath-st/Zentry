from django.db import models
from django.utils import timezone # Para manejar fechas

# Modelo base requerido para el Foreign Key del Ticket
class Evento(models.Model):
    """
    Modelo simplificado para los Eventos (asumimos que otro compañero lo gestiona).
    Necesario para la relación con Ticket.
    """
    nombre = models.CharField(max_length=150)
    fecha = models.DateField()
    # Otros campos de Evento...

    def __str__(self):
        return self.nombre

class Ticket(models.Model):
    """
    Modelo clave para la validación. Almacena el código único y el estado de uso.
    """
    # El código debe ser la clave principal para búsquedas rápidas en la DB (INDEX)
    codigo_ticket = models.CharField(max_length=20, unique=True, primary_key=True) 
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE) 
    
    # Campo crucial para tu módulo
    esta_usado = models.BooleanField(default=False)
    
    fecha_emision = models.DateTimeField(auto_now_add=True)
    fecha_uso = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Ticket {self.codigo_ticket} - {self.evento.nombre} (Usado: {self.esta_usado})"