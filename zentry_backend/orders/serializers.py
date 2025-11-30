from rest_framework import serializers
from events.serializers import EventSerializer
from .models import Ticket, Order

class PurchaseSerializer(serializers.Serializer):
    seat_ids = serializers.ListField(child=serializers.IntegerField())
    cvv = serializers.CharField(max_length=4)

class TicketDetailSerializer(serializers.ModelSerializer):
    # Campos calculados para no enviar todo el objeto anidado complejo
    event_title = serializers.CharField(source='seat.zone.event.title')
    event_date = serializers.DateTimeField(source='seat.zone.event.date')
    event_image = serializers.CharField(source='seat.zone.event.image_url')
    venue = serializers.CharField(source='seat.zone.event.venue')
    seat_label = serializers.SerializerMethodField()
    price = serializers.DecimalField(source='seat.zone.price', max_digits=10, decimal_places=2)

    class Meta:
        model = Ticket
        fields = ['id', 'ticket_code', 'event_title', 'event_date', 'event_image', 'venue', 'seat_label', 'price']

    def get_seat_label(self, obj):
        return f"{obj.seat.zone.name} - {obj.seat.row_label}{obj.seat.number}"