"""
Serializadores para el Catálogo de Eventos.
Convierte modelos de dominio a/desde JSON.
"""

from rest_framework import serializers
from core.domain.event_catalog import EventCatalog, SortCriteria


class EventCatalogSerializer(serializers.Serializer):
    """Serializador para EventCatalog."""
    
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    venue = serializers.CharField(max_length=200)
    date = serializers.DateTimeField()
    min_price = serializers.FloatField(min_value=0)
    max_price = serializers.FloatField(min_value=0)
    total_capacity = serializers.IntegerField(min_value=1)
    sold_tickets = serializers.IntegerField(default=0, min_value=0)
    description = serializers.CharField(required=False, allow_blank=True)
    artist_name = serializers.CharField(required=False, allow_blank=True)
    is_active = serializers.BooleanField(default=True)
    popularity_score = serializers.SerializerMethodField(read_only=True)
    availability_percentage = serializers.SerializerMethodField(read_only=True)
    is_sold_out = serializers.SerializerMethodField(read_only=True)
    is_upcoming = serializers.SerializerMethodField(read_only=True)

    def get_popularity_score(self, obj) -> float:
        """Retorna score de popularidad."""
        return obj.popularity_score

    def get_availability_percentage(self, obj) -> float:
        """Retorna porcentaje de disponibilidad."""
        return obj.availability_percentage

    def get_is_sold_out(self, obj) -> bool:
        """Retorna si está agotado."""
        return obj.is_sold_out()

    def get_is_upcoming(self, obj) -> bool:
        """Retorna si es futuro."""
        return obj.is_upcoming()

    def create(self, validated_data):
        """Crea una instancia de EventCatalog desde datos validados."""
        return EventCatalog(**validated_data)

    def update(self, instance, validated_data):
        """Actualiza una instancia de EventCatalog."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        return instance


class EventCatalogListSerializer(serializers.Serializer):
    """Serializador para lista de eventos con opciones de ordenamiento."""
    
    events = EventCatalogSerializer(many=True, read_only=True)
    sort_by = serializers.ChoiceField(
        choices=[c.value for c in SortCriteria],
        required=False,
        help_text="Ordenar por: date, price, o popularity"
    )
    total_count = serializers.SerializerMethodField(read_only=True)

    def get_total_count(self, obj):
        """Retorna el total de eventos."""
        return len(obj.get('events', []))
