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

class JoinQueueView(APIView):
    """ Paso 1: Entrar a la Cola (Queue) """
    def post(self, request):
        cola_virtual.encolar(request.user.id)
        return Response({"message": "Estás en la fila virtual. Procede al pago."})

class UndoCartView(APIView):
    """ Paso Opcional: Deshacer última selección (Stack) """
    def post(self, request):
        ultimo_asiento = historial_carrito.pop_accion(request.user.id)
        if ultimo_asiento:
            # Aquí liberaríamos el asiento en BD si estuviera reservado
            return Response({"message": f"Asiento {ultimo_asiento} eliminado del historial (Stack LIFO)."})
        return Response({"error": "Nada que deshacer"}, status=400)

class CheckoutView(APIView):
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
                    # Calcular total
                    seats = Seat.objects.filter(id__in=seat_ids, status='AVAILABLE')
                    if len(seats) != len(seat_ids):
                         return Response({"error": "Uno o más asientos ya no están disponibles"}, status=409)
                    
                    total = sum([s.zone.price for s in seats])
                    
                    # Crear Orden
                    order = Order.objects.create(user=request.user, total_amount=total)
                    
                    tickets_creados = []
                    for seat in seats:
                        # Marcar asiento ocupado
                        seat.status = 'SOLD'
                        seat.save()
                        
                        # Generar Ticket
                        code = f"ZEN-{uuid.uuid4().hex[:6].upper()}"
                        Ticket.objects.create(order=order, seat=seat, ticket_code=code)
                        validador_acceso.cargar_ticket(code)
                        tickets_creados.append(code)

                        # Guardar acción en PILA por si quiere reembolsar luego (opcional)
                        historial_carrito.push_accion(request.user.id, seat.id)
                    
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