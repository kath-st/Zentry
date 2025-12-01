import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from .models import Order, Ticket
from .serializers import PurchaseSerializer, TicketDetailSerializer
from events.models import Seat
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .estructuras import cola_virtual, historial_carrito
from access_control.estructuras import validador_acceso
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string

class AddToCartView(APIView):
    """Agregar asientos al carrito y reservarlos temporalmente"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        seat_ids = request.data.get('seat_ids', [])
        
        if not seat_ids:
            return Response({"error": "No se proporcionaron asientos"}, status=400)
        
        try:
            with transaction.atomic():
                # Verificar disponibilidad
                seats = Seat.objects.select_for_update().filter(
                    id__in=seat_ids,
                    status='AVAILABLE'
                )
                
                if len(seats) != len(seat_ids):
                    return Response({"error": "Uno o más asientos ya no están disponibles"}, status=409)
                
                # Reservar temporalmente (10 minutos)
                expiration_time = timezone.now() + timedelta(minutes=10)
                
                reserved_seats = []
                for seat in seats:
                    seat.status = 'RESERVED'
                    seat.reserved_by = request.user
                    seat.reserved_at = timezone.now()
                    seat.reservation_expires_at = expiration_time
                    seat.save()
                    
                    # Agregar a la pila (Stack)
                    historial_carrito.push_accion(request.user.id, seat.id)
                    
                    reserved_seats.append({
                        'id': seat.id,
                        'seat': f"{seat.row_label}{seat.number}",
                        'zone': seat.zone.name,
                        'price': float(seat.zone.price),
                        'expires_at': expiration_time.isoformat()
                    })
                
                return Response({
                    "message": "Asientos reservados temporalmente",
                    "seats": reserved_seats,
                    "expires_in_minutes": 10
                }, status=200)
                
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class ReleaseReservationView(APIView):
    """Liberar una reserva temporal específica"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        seat_id = request.data.get('seat_id')
        
        if not seat_id:
            return Response({"error": "seat_id requerido"}, status=400)
        
        try:
            seat = Seat.objects.get(id=seat_id, reserved_by=request.user, status='RESERVED')
            
            # Liberar asiento
            seat.status = 'AVAILABLE'
            seat.reserved_by = None
            seat.reserved_at = None
            seat.reservation_expires_at = None
            seat.save()
            
            return Response({"message": "Reserva liberada exitosamente"}, status=200)
            
        except Seat.DoesNotExist:
            return Response({"error": "Asiento no encontrado o no reservado por ti"}, status=404)

class CleanExpiredReservationsView(APIView):
    """Limpiar todas las reservas expiradas (puede ser llamado periódicamente)"""
    
    def post(self, request):
        now = timezone.now()
        expired_seats = Seat.objects.filter(
            status='RESERVED',
            reservation_expires_at__lt=now
        )
        
        count = expired_seats.count()
        expired_seats.update(
            status='AVAILABLE',
            reserved_by=None,
            reserved_at=None,
            reservation_expires_at=None
        )
        
        return Response({
            "message": f"{count} reservas expiradas limpiadas",
            "count": count
        }, status=200)

class JoinQueueView(APIView):
    """ Paso 1: Entrar a la Cola (Queue) """
    def post(self, request):
        cola_virtual.encolar(request.user.id)
        return Response({"message": "Estás en la fila virtual. Procede al pago."})

class UndoCartView(APIView):
    """ Paso Opcional: Deshacer última selección (Stack) """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        ultimo_asiento_id = historial_carrito.pop_accion(request.user.id)
        if ultimo_asiento_id:
            try:
                # Liberar el asiento que estaba reservado
                seat = Seat.objects.get(id=ultimo_asiento_id, reserved_by=request.user)
                seat.status = 'AVAILABLE'
                seat.reserved_by = None
                seat.reserved_at = None
                seat.reservation_expires_at = None
                seat.save()
                
                return Response({
                    "message": f"Asiento {seat.row_label}{seat.number} eliminado del carrito (Stack LIFO).",
                    "seat_id": ultimo_asiento_id
                })
            except Seat.DoesNotExist:
                return Response({"error": "Asiento no encontrado"}, status=404)
        return Response({"error": "Nada que deshacer"}, status=400)

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # 1. VERIFICAR COLA (Estructura de Datos)
        if not cola_virtual.es_turno(request.user.id):
             return Response({"error": "Debes unirte a la fila primero."}, status=403)

        serializer = PurchaseSerializer(data=request.data)
        if serializer.is_valid():
            cvv = serializer.validated_data['cvv']
            seat_ids = serializer.validated_data['seat_ids']

            # 2. VALIDAR CVV (Requisito Seguridad) GENERICOOOOOO SIEMPRE VA A SER 123 OJOOOOO
            if cvv != "123":
                return Response({"error": "CVV Inválido"}, status=400)

            # 3. PROCESAR COMPRA (Atomicidad)
            try:
                with transaction.atomic():
                    # Verificar que los asientos estén reservados por este usuario
                    seats = Seat.objects.filter(
                        id__in=seat_ids, 
                        reserved_by=request.user,
                        status='RESERVED'
                    )
                    
                    if len(seats) != len(seat_ids):
                         return Response({
                             "error": "Uno o más asientos no están reservados por ti o ya expiraron"
                         }, status=409)
                    
                    total = sum([s.zone.price for s in seats])
                    
                    # Crear Orden
                    order = Order.objects.create(user=request.user, total_amount=total)
                    
                    tickets_creados = []
                    for seat in seats:
                        # Marcar asiento como VENDIDO (no solo reservado)
                        seat.status = 'SOLD'
                        seat.reserved_by = None
                        seat.reserved_at = None
                        seat.reservation_expires_at = None
                        seat.save()
                        
                        # Generar Ticket
                        code = f"ZEN-{uuid.uuid4().hex[:6].upper()}"
                        Ticket.objects.create(order=order, seat=seat, ticket_code=code)
                        validador_acceso.cargar_ticket(code)
                        tickets_creados.append(code)
                    
                    # Limpiar el carrito del usuario (Stack)
                    historial_carrito.clear(request.user.id)
                    
                    # Sacar de la cola
                    cola_virtual.atender()

                    return Response({
                        "status": "Compra exitosa",
                        "tickets": tickets_creados,
                        "total": total
                    }, status=201)
            except Exception as e:
                return Response({"error": str(e)}, status=500)
        
        return Response(serializer.errors, status=400)

class MyTicketsView(generics.ListAPIView):
    serializer_class = TicketDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retorna solo los tickets del usuario actual
        return Ticket.objects.filter(order__user=self.request.user).order_by('-id')

class DownloadTicketPDFView(APIView):
    """Generar y descargar PDF de un ticket"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, ticket_id):
        try:
            # Obtener ticket del usuario actual
            ticket = Ticket.objects.select_related(
                'seat__zone__event',
                'order__user'
            ).get(id=ticket_id, order__user=request.user)
            
            # Datos del template
            context = {
                'ticket': ticket,
                'event': ticket.seat.zone.event,
                'seat': ticket.seat,
                'user': request.user,
                'zone': ticket.seat.zone,
            }
            
            # Renderizar HTML
            html_string = render_to_string('ticket_pdf.html', context)
            
            # Generar PDF
            pdf_file = HTML(string=html_string).write_pdf()
            
            # Respuesta HTTP
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="ticket_{ticket.ticket_code}.pdf"'
            
            return response
            
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket no encontrado"}, status=404)