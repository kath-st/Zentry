from collections import deque

# 1. COLA (QUEUE) - Para la fila de compra
class ColaDeCompras:
    def __init__(self):
        self.fila = deque() # Deque es optimizado para queues en Python

    def encolar(self, user_id):
        if user_id not in self.fila:
            self.fila.append(user_id)

    def atender(self):
        if self.fila:
            return self.fila.popleft() # Saca el primero (FIFO)
        return None

    def es_turno(self, user_id):
        # En un caso real, verificaríamos si es el primero.
        # Para facilitar la demo, retornamos True si está en la fila.
        return user_id in self.fila

# 2. PILA (STACK) - Para deshacer acciones del carrito
class PilaCarrito:
    def __init__(self):
        # Diccionario de Pilas: user_id -> [lista de acciones]
        self.pilas_usuarios = {}

    def push_accion(self, user_id, seat_id):
        if user_id not in self.pilas_usuarios:
            self.pilas_usuarios[user_id] = []
        self.pilas_usuarios[user_id].append(seat_id) # LIFO

    def pop_accion(self, user_id):
        if user_id in self.pilas_usuarios and self.pilas_usuarios[user_id]:
            return self.pilas_usuarios[user_id].pop() # Saca el último
        return None
    
    def get_all(self, user_id):
        """Obtiene todos los asientos del carrito de un usuario"""
        return self.pilas_usuarios.get(user_id, [])
    
    def clear(self, user_id):
        """Limpia el carrito de un usuario"""
        if user_id in self.pilas_usuarios:
            self.pilas_usuarios[user_id] = []

# Instancias Globales
cola_virtual = ColaDeCompras()
historial_carrito = PilaCarrito()