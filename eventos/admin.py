from django.contrib import admin
from .models import (
    Ubicacion,
    Zona,
    Evento,
    Asiento,
    PrecioPorZona,
    Reserva,
    Compra,
    PurchaseSession
)

from .modulo.reservas.utils import generar_asientos_para_zona


# ADMIN DE ZONA (auto-generación de asientos al crear zona)
@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        """
        Genera los asientos automáticamente solo cuando la zona
        se crea por primera vez (no en modificaciones).
        """
        super().save_model(request, obj, form, change)

        if not change:  # Si es creación
            generar_asientos_para_zona(obj)


# REGISTROS BÁSICOS
admin.site.register(Ubicacion)
admin.site.register(Asiento)
admin.site.register(Reserva)
admin.site.register(PrecioPorZona)
admin.site.register(PurchaseSession)
admin.site.register(Compra)


# ADMIN DE EVENTO
@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "fecha", "ubicacion")
    list_filter = ("ubicacion", "fecha")
    search_fields = ("titulo",)
