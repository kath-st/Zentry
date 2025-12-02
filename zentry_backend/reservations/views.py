from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.db import transaction, IntegrityError
from django.utils import timezone
from datetime import timedelta
from events.models import Seat # Importamos el modelo de tu compañero
from orders.estructuras import historial_carrito # Conectamos con el carrito de ella

# Importaciones de TUS módulos
from .services import bloquear_asiento_atomic
from .estructuras import gestor_expiraciones
from events.estructuras import MatrizAsientos # Usamos la clase de visualización

# Importaciones de OTROS módulos
from events.models import Seat
from orders.estructuras import historial_carrito # Para conectar con la compañera

class MapaVisualView(APIView):
    """
    GET /api/reservations/mapa/<event_id>/
    Muestra la MATRIZ de asientos (Estructura de Datos 1).
    """
    permission_classes = [AllowAny]

    def get(self, request, event_id):
        # 1. Obtener datos crudos
        asientos = Seat.objects.filter(zone__event_id=event_id)
        
        # 2. Procesar con Estructura (Matriz)
        # Asumimos 20 filas x 10 columnas como definiste antes
        sala = MatrizAsientos(filas=20, columnas=10) 
        sala.cargar_desde_db(asientos)
        
        return Response({
            "mapa": sala.obtener_json(),
            # Algoritmo de búsqueda de consecutivos (Opcional, pero suma puntos)
            "sugerencia": sala.buscar_consecutivos(2) 
        })

class ReservarAsientoView(APIView):
    """
    TU LÓGICA MAESTRA: Bloqueo transaccional de asientos.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        seat_id = request.data.get('seat_id')
        
        try:
            with transaction.atomic():
                # 1. BLOQUEO (Row-Level Locking)
                # Esto congela el asiento para que nadie más lo toque
                seat = Seat.objects.select_for_update().get(id=seat_id)

                # 2. VALIDACIÓN
                if seat.status != 'AVAILABLE':
                    return Response({"error": "Asiento ganado por otro usuario"}, status=409)

                # 3. RESERVA TEMPORAL
                seat.status = 'RESERVED'
                seat.reserved_by = request.user
                seat.reserved_at = timezone.now()
                # 10 minutos para pagar
                seat.reservation_expires_at = timezone.now() + timedelta(minutes=10)
                seat.save()

                # 4. ACTUALIZAR ESTRUCTURA DE LA COMPAÑERA (Stack)
                historial_carrito.push_accion(request.user.id, seat.id)

                return Response({
                    "message": "Asiento bloqueado",
                    "expires_at": seat.reservation_expires_at
                }, status=200)

        except Seat.DoesNotExist:
            return Response({"error": "Asiento no encontrado"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)