from django.db import models
from django.utils import timezone
from events.models import Event

class Ticket(models.Model):
    codigo_ticket = models.CharField(max_length=20, unique=True, primary_key=True) 
    evento = models.ForeignKey(Event, on_delete=models.CASCADE) 
    
    # Campo crucial para tu módulo
    esta_usado = models.BooleanField(default=False)
    
    fecha_emision = models.DateTimeField(auto_now_add=True)
    fecha_uso = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Ticket {self.codigo_ticket} - {self.evento.name} (Usado: {self.esta_usado})"