import heapq
from events.estructuras import MatrizAsientos  # Reutilizamos la Matriz (Array 2D)

class MinHeapExpiraciones:
    """
    Estructura de Datos: Montículo Binario (Min-Heap).
    Objetivo: Obtener siempre la reserva próxima a vencer en O(1).
    """
    def __init__(self):
        # Lista de tuplas (timestamp_expiracion, seat_id)
        self.heap = []
    
    def agregar_reserva(self, seat_id, expiration_time):
        # O(log n)
        timestamp = expiration_time.timestamp()
        heapq.heappush(self.heap, (timestamp, seat_id))

    def obtener_proxima_a_vencer(self):
        # O(1) - Solo mira el tope
        if not self.heap:
            return None
        return self.heap[0] # (timestamp, seat_id)

    def eliminar_minimo(self):
        # O(log n)
        if self.heap:
            return heapq.heappop(self.heap)
        return None

# Instancia global del Heap (en memoria)
gestor_expiraciones = MinHeapExpiraciones()