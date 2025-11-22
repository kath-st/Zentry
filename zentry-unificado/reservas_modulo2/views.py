# views.py (versión en español)
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

from events.models import Event as Evento, Asiento
from .models import ReservaM2 as Reserva, PurchaseSession
from .services import GestorDeReservas

gestor = GestorDeReservas()

# Iniciar sesión de compra (temporizador global)
@csrf_exempt
def iniciar_sesion_compra(request):
    """
    POST JSON:
    { "usuario_id": <int>, "evento_id": <int> }

    Retorna:
    {
        "sesion_id": <id>,
        "expiracion": "<ISO>"
    }
    """
    if request.method != 'POST':
        return HttpResponseBadRequest("Método no permitido.")

    try:
        datos = json.loads(request.body)
        usuario_id = datos.get("usuario_id")
        evento_id = datos.get("evento_id")
    except:
        return HttpResponseBadRequest("JSON inválido.")

    if not usuario_id or not evento_id:
        return HttpResponseBadRequest("Faltan campos.")

    Usuario = get_user_model()
    usuario = get_object_or_404(Usuario, id=usuario_id)
    evento = get_object_or_404(Evento, id=evento_id)

    sesion = gestor.iniciar_sesion_compra(usuario, evento)

    return JsonResponse({
        "sesion_id": sesion.id,
        "expiracion": sesion.expiracion.isoformat()
    })


@csrf_exempt
def listar_asientos_disponibles(request, evento_id, zona_id=None):
    """
    GET
    Retorna lista de asientos disponibles y ordenados.
    """
    evento = get_object_or_404(Evento, id=evento_id)
    disponibles = gestor.obtener_asientos_disponibles(evento, zona_id)

    resultado = [
        {"fila": f, "columna": c, "asiento_id": a_id}
        for (f, c, a_id) in disponibles
    ]

    return JsonResponse({"asientos": resultado})


# (crear reserva)
@csrf_exempt
def seleccionar_asiento(request):
    """
    POST JSON:
    {
        "usuario_id": X,
        "evento_id": Y,
        "sesion_id": Z,
        "asiento_id": A
    }
    """
    if request.method != 'POST':
        return HttpResponseBadRequest("Método no permitido.")

    try:
        datos = json.loads(request.body)
        usuario_id = datos.get("usuario_id")
        evento_id = datos.get("evento_id")
        sesion_id = datos.get("sesion_id")
        asiento_id = datos.get("asiento_id")
    except:
        return HttpResponseBadRequest("JSON inválido.")

    if not (usuario_id and evento_id and sesion_id and asiento_id):
        return HttpResponseBadRequest("Faltan campos.")

    Usuario = get_user_model()
    usuario = get_object_or_404(Usuario, id=usuario_id)
    evento = get_object_or_404(Evento, id=evento_id)
    sesion = get_object_or_404(PurchaseSession, id=sesion_id)

    # Validaciones de sesión
    if not sesion.activo or sesion.evento.id != evento.id or sesion.usuario != usuario:
        return JsonResponse({"error": "Sesión inválida o expirada."}, status=400)

    try:
        reserva = gestor.reservar_asiento(evento, asiento_id, usuario, sesion)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({
        "reserva_id": reserva.id,
        "asiento": {
            "fila": reserva.asiento.fila,
            "columna": reserva.asiento.columna
        },
        "expiracion": reserva.expiracion.isoformat()
    })


# Eliminar asiento / reserva (Deshacer)
@csrf_exempt
def eliminar_reserva(request):
    """
    POST JSON:
    {
        "usuario_id": X,
        "reserva_id": Y
    }
    """
    if request.method != 'POST':
        return HttpResponseBadRequest("Método no permitido.")

    try:
        datos = json.loads(request.body)
        usuario_id = datos.get("usuario_id")
        reserva_id = datos.get("reserva_id")
    except:
        return HttpResponseBadRequest("JSON inválido.")

    if not (usuario_id and reserva_id):
        return HttpResponseBadRequest("Faltan campos.")

    Usuario = get_user_model()
    usuario = get_object_or_404(Usuario, id=usuario_id)

    try:
        reserva = gestor.eliminar_reserva(reserva_id, usuario)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({
        "reserva_cancelada_id": reserva.id,
        "mensaje": "Reserva eliminada."
    })


# Confirmar compra (agrupada)
@csrf_exempt
def confirmar_compra(request):
    """
    POST JSON:
    {
        "usuario_id": X,
        "reservas": [1,2,3],
        "metodo_pago": "Tarjeta"
    }
    """
    if request.method != 'POST':
        return HttpResponseBadRequest("Método no permitido.")

    try:
        datos = json.loads(request.body)
        usuario_id = datos.get("usuario_id")
        lista_ids = datos.get("reservas", [])
        metodo_pago = datos.get("metodo_pago")
    except:
        return HttpResponseBadRequest("JSON inválido.")

    if not (usuario_id and lista_ids):
        return HttpResponseBadRequest("Faltan campos.")

    Usuario = get_user_model()
    usuario = get_object_or_404(Usuario, id=usuario_id)

    try:
        compra = gestor.confirmar_compra(lista_ids, usuario, metodo_pago)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({
        "compra_id": compra.id,
        "total": str(compra.monto_total),
        "reservas": [r.id for r in compra.reservas.all()],
        "mensaje": "Compra realizada correctamente."
    })
