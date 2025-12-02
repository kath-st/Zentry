from django.db import transaction, IntegrityError
from django.utils import timezone
from datetime import timedelta
from events.models import Seat
from .estructuras import gestor_expiraciones

# Tiempo de reserva (10 minutos)
TIEMPO_RESERVA = 10 

def bloquear_asiento_atomic(seat_id, user):
    """
    Algoritmo de Concurrencia:
    Usa 'Row-Level Locking' para garantizar atomicidad.
    """
    try:
        # 1. INICIO DE LA TRANSACCIÓN (El "Candado")
        with transaction.atomic():
            # select_for_update(): Bloquea esta fila en la BD.
            # Nadie más puede escribir en este asiento hasta que termine este bloque.
            asiento = Seat.objects.select_for_update().get(id=seat_id)

            # 2. VALIDACIÓN DE ESTADO
            # Si ya está vendido o reservado por otro (y no vencido), error.
            if asiento.status != 'AVAILABLE':
                # Podrías agregar lógica aquí para "robar" si ya venció, 
                # pero para simplificar, lanzamos error si no está libre.
                if asiento.status == 'SOLD':
                     raise IntegrityError("El asiento ya fue vendido.")
                if asiento.status == 'RESERVED' and not asiento.is_reservation_expired():
                     raise IntegrityError("El asiento está reservado por otra persona.")

            # 3. ACTUALIZACIÓN (RESERVA)
            asiento.status = 'RESERVED'
            asiento.reserved_by = user
            
            ahora = timezone.now()
            expiracion = ahora + timedelta(minutes=TIEMPO_RESERVA)
            
            asiento.reserved_at = ahora
            asiento.reservation_expires_at = expiracion
            
            asiento.save()

            # 4. AGREGAR A ESTRUCTURA DE DATOS (HEAP)
            # Esto nos permite monitorear expiraciones en RAM sin consultar la BD a cada rato
            gestor_expiraciones.agregar_reserva(asiento.id, expiracion)

            return asiento

    except Seat.DoesNotExist:
        raise ValueError("El asiento no existe.")