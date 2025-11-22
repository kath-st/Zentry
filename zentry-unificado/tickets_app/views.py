from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .services.control_acceeso_service import ControlAccesoService

# Variable global para el servicio (se inicializa cuando sea necesario)
control_service = None

def get_control_service():
    """Obtiene o crea la instancia del servicio de control de acceso."""
    global control_service
    if control_service is None:
        control_service = ControlAccesoService()
    return control_service

@method_decorator(csrf_exempt, name='dispatch')
def validar_acceso(request):
    """
    Endpoint para validar el acceso con el código numérico.
    Método de verificación: POST
    """
    
    if request.method == 'POST':
        try:
            # 1. Leer el código del cuerpo de la petición POST
            data = json.loads(request.body)
            codigo_ticket = data.get('codigo', None)
            
            if not codigo_ticket:
                return JsonResponse({"status": "ERROR", "mensaje": "Código de ticket requerido."}, status=400)

            # 2. Llamar a tu lógica de Estructuras de Datos (O(1))
            resultado = get_control_service().validar_ticket(codigo_ticket)
            
            return JsonResponse(resultado)
        
        except json.JSONDecodeError:
            return JsonResponse({"status": "ERROR", "mensaje": "Formato de petición inválido."}, status=400)
    
    return JsonResponse({"status": "ERROR", "mensaje": "Método no permitido. Use POST."}, status=405)


def ver_fila_ingreso(request):
    """
    Endpoint para ver el estado actual de la fila de ingreso (Cola/Deque).
    """
    # Se extrae la cola de la instancia de servicio
    fila_actual = list(get_control_service().fila_ingreso) 
    
    return JsonResponse({
        "status": "OK",
        "total_en_fila": len(fila_actual),
        "orden_de_ingreso": fila_actual
    })