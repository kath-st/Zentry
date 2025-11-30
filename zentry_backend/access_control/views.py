from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ScanLog
from orders.models import Ticket
from .estructuras import validador_acceso
from django.utils import timezone

class ValidateTicketView(APIView):
    def post(self, request):
        code = request.data.get('ticket_code')
        employee = request.user # Asumimos que es un empleado logueado
        
        # 1. VALIDACIÓN ESTRUCTURAL (SET - O(1))
        # Si no está en el Set, ni siquiera molestamos a la base de datos
        if not validador_acceso.es_autentico(code):
            ScanLog.objects.create(employee=employee, scanned_code=code, outcome='INVALID')
            return Response({
                "status": "error",
                "message": "Ticket NO EXISTE (Rechazado por Set)",
                "color": "red"
            }, status=404)

        # 2. VALIDACIÓN DE ESTADO (Base de Datos)
        try:
            ticket = Ticket.objects.get(ticket_code=code)
            
            if ticket.seat.status == 'USED': # O usaremos un campo is_used si lo agregaste
                 ScanLog.objects.create(employee=employee, scanned_code=code, outcome='DUPLICATE')
                 return Response({
                    "status": "warning",
                    "message": "Ticket YA FUE USADO",
                    "color": "yellow",
                    "data": {
                        "event": ticket.seat.zone.event.title,
                        "time": ticket.order.created_at # Simulado
                    }
                }, status=409)

            # 3. ÉXITO (Marcar como usado)
            # Usamos el estado del asiento o agregamos un campo 'is_used' al ticket
            # Para este ejemplo, cambiamos el status del asiento a 'USED' (o similar)
            ticket.seat.status = 'USED' 
            ticket.seat.save()
            
            ScanLog.objects.create(employee=employee, scanned_code=code, outcome='SUCCESS')
            
            return Response({
                "status": "success",
                "message": "Bienvenido",
                "color": "green",
                "data": {
                    "user": f"{ticket.order.user.first_name} {ticket.order.user.last_name}",
                    "seat": f"{ticket.seat.zone.name} - {ticket.seat.row_label}{ticket.seat.number}",
                    "event": ticket.seat.zone.event.title
                }
            }, status=200)

        except Ticket.DoesNotExist:
            # Esto no debería pasar si el Set está sincronizado, pero por seguridad:
            return Response({"error": "Error de sincronización"}, status=500)

class StatsView(APIView):
    def get(self, request):
        # 1. Obtenemos la hora actual en la zona horaria configurada
        now = timezone.localtime(timezone.now())
        
        # 2. Definimos el inicio del día (00:00:00)
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # 3. Filtramos desde el inicio del día en adelante
        logs = ScanLog.objects.filter(timestamp__gte=start_of_day)
        
        return Response({
            "validos_hoy": logs.filter(outcome='SUCCESS').count(),
            "duplicados_hoy": logs.filter(outcome='DUPLICATE').count(),
            "invalidos_hoy": logs.filter(outcome='INVALID').count()
        })