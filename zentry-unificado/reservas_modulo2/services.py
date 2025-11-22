import heapq
from datetime import timedelta
from django.utils import timezone
from django.db import transaction, IntegrityError
from decimal import Decimal

from .models import ReservaM2 as Reserva, CompraM2 as Compra, PurchaseSession
from events.models import Asiento, Event as Evento, Zone
from .estructuras import ordenamiento_rapido

TIEMPO_EXPIRACION_MINUTOS = 5
LIMITE_ASIENTOS_POR_USUARIO = 5

class GestorDeReservas:
    """
    Clase principal del módulo 2.
    Maneja:
    - Sesiones de compra
    - Reservas
    - Expiraciones (con heap mínimo)
    - Confirmación de compra
    - "Deshacer" (eliminar una reserva)
    """

    def __init__(self):
        # Heap mínimo para expiraciones → (epoch_expiracion, id_reserva)
        self.heap = []
        self.heap_inicializado = False


    def construir_heap(self):
        if self.heap_inicializado:
            return
        
        reservas_activas = Reserva.objects.filter(activo=True)

        for r in reservas_activas:
            epoch = r.expiracion.timestamp()
            heapq.heappush(self.heap, (epoch, r.id))

        self.heap_inicializado = True


    def liberar_expiradas(self):
        """
        Marca como inactivas las reservas cuyo tiempo ya venció.
        También desactiva sesiones si ya expiraron.
        """
        self.construir_heap()
        ahora_epoch = timezone.now().timestamp()
        liberadas = []

        while self.heap and self.heap[0][0] <= ahora_epoch:
            _, reserva_id = heapq.heappop(self.heap)

            try:
                reserva = Reserva.objects.get(id=reserva_id)
            except Reserva.DoesNotExist:
                continue

            if reserva.activo and reserva.expiracion <= timezone.now():
                reserva.activo = False
                reserva.save()
                liberadas.append(reserva)

                # También validar expiración de la sesión
                if reserva.session:
                    ses = reserva.session
                    if ses.activo and ses.expiracion <= timezone.now():
                        ses.activo = False
                        ses.save()

        return liberadas


    def iniciar_sesion_compra(self, usuario, evento, minutos=TIEMPO_EXPIRACION_MINUTOS):
        """
        Crea una sesión de compra global para el usuario.
        Todas sus reservas heredarán su fecha de expiración.
        """
        expiracion = timezone.now() + timedelta(minutes=minutos)
        sesion = PurchaseSession.objects.create(
            usuario=usuario,
            evento=evento,
            expiracion=expiracion,
            activo=True
        )
        return sesion


    def reservar_asiento(self, evento: Evento, asiento_id: int, usuario, sesion: PurchaseSession):
        """
        Reserva un asiento para un usuario dentro de la sesión de compra.
        - Verifica límite de 5
        - Lock de BD (select_for_update)
        - Hereda expiración de la sesión global
        """
        if usuario is None:
            raise ValueError("Se requiere un usuario para reservar.")

        # Actualizar expiraciones antes de reservar
        self.liberar_expiradas()

        # Verificar límite por evento
        activas_usuario = Reserva.objects.filter(
            evento=evento, usuario=usuario, activo=True
        ).count()

        if activas_usuario + 1 > LIMITE_ASIENTOS_POR_USUARIO:
            raise IntegrityError(
                f"Límite de {LIMITE_ASIENTOS_POR_USUARIO} asientos por evento excedido. "
                f"Ya tienes {activas_usuario} activos."
            )

        try:
            with transaction.atomic():
                asiento = Asiento.objects.select_for_update().get(id=asiento_id)

                # Verificar si ya está reservado o vendido
                conflicto = Reserva.objects.filter(
                    evento=evento, asiento=asiento, activo=True
                ).exists()

                if conflicto:
                    raise IntegrityError(f"El asiento {asiento.id} ya está reservado.")

                # Crear reserva con expiración heredada
                reserva = Reserva.objects.create(
                    evento=evento,
                    asiento=asiento,
                    usuario=usuario,
                    session=sesion,
                    expiracion=sesion.expiracion,
                    activo=True
                )

                heapq.heappush(self.heap, (reserva.expiracion.timestamp(), reserva.id))

        except Exception as e:
            raise e

        return reserva


    def eliminar_reserva(self, reserva_id: int, usuario):
        """
        Marca como inactiva una reserva.
        Este método se usa cuando el usuario elimina un asiento del resumen.
        """
        try:
            with transaction.atomic():
                r = Reserva.objects.select_for_update().get(id=reserva_id)

                if r.usuario != usuario:
                    raise IntegrityError("No puedes eliminar una reserva que no te pertenece.")

                if not r.activo:
                    raise IntegrityError("La reserva ya no está activa.")

                r.activo = False
                r.save()
                return r

        except Reserva.DoesNotExist:
            raise IntegrityError("Reserva no encontrada.")


    def obtener_precio_reserva(self, reserva: Reserva) -> Decimal:
        zona = reserva.asiento.zona
        return zona.price


    def confirmar_compra(self, lista_ids_reserva: list, usuario=None, metodo_pago=None):
        """
        Confirma varias reservas como una sola compra.
        Marca cada reserva como inactiva y genera una Compra.
        """
        if not lista_ids_reserva:
            raise ValueError("No hay reservas para confirmar.")

        with transaction.atomic():

            reservas = []
            total = Decimal('0.00')

            for rid in lista_ids_reserva:
                r = Reserva.objects.select_for_update().get(id=rid)

                if not r.activo:
                    raise IntegrityError(f"La reserva {rid} ya expiró o fue cancelada.")

                precio = self.obtener_precio_reserva(r)
                total += Decimal(precio)

                reservas.append(r)

            compra = Compra.objects.create(
                usuario=usuario,
                metodo_pago=metodo_pago,
                monto_total=total
            )

            for r in reservas:
                r.activo = False
                r.save()
                compra.reservas.add(r)

            return compra


    def obtener_asientos_disponibles(self, evento: Evento, zona_id=None):
        """
        Devuelve una lista ORDENADA de asientos disponibles para un evento.
        """
        self.liberar_expiradas()

        asientos = Asiento.objects.all()
        if zona_id:
            asientos = asientos.filter(zona_id=zona_id)

        reservados_ids = Reserva.objects.filter(
            evento=evento, activo=True
        ).values_list('asiento_id', flat=True)

        asientos = asientos.exclude(id__in=list(reservados_ids))

        arreglo = [(a.fila, a.columna, a.id) for a in asientos]

        return ordenamiento_rapido(arreglo)