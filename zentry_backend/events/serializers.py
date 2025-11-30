from rest_framework import serializers
from .models import Event, Zone, Seat

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ['id', 'name', 'price']

class EventSerializer(serializers.ModelSerializer):
    # Incluimos las zonas anidadas para que el frontend sepa los precios disponibles
    zones = ZoneSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 
            'tm_id',       # ID de Ticketmaster
            'title', 
            'image_url',   # La URL de la foto que viene de la API
            'date', 
            'venue', 
            'category', 
            'price_min', 
            'zones'        # Lista de precios/zonas
        ]

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'row_label', 'number', 'status']

# ... (Tus serializers anteriores) ...

class ZoneInputSerializer(serializers.Serializer):
    """ Serializer auxiliar para recibir zonas al crear un evento """
    name = serializers.CharField(max_length=50)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

class EventAdminSerializer(serializers.ModelSerializer):
    """ Serializer para CREAR y EDITAR eventos manualmente """
    # write_only=True significa que sirve para recibir datos, no para mostrarlos
    zones_input = ZoneInputSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'date', 'venue', 'image_url', 
            'category', 'price_min', 'zones_input'
        ]