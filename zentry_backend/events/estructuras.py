class MatrizAsientos:
    """
    Representación en memoria de la sala.
    Aumentamos filas a 20 para que quepan varias zonas.
    """
    def __init__(self, filas=20, columnas=10): # <--- AUMENTADO A 20 FILAS
        self.filas = filas
        self.columnas = columnas
        self.matriz = [[None for _ in range(columnas)] for _ in range(filas)]

    def cargar_desde_db(self, lista_asientos_queryset):
        for asiento in lista_asientos_queryset:
            # Parseamos "F1" -> índice 0
            # Si el backend genera filas altas (F15), esto funcionará bien
            fila_idx = int(asiento.row_label.replace("F", "")) - 1
            col_idx = asiento.number - 1
            
            if 0 <= fila_idx < self.filas and 0 <= col_idx < self.columnas:
                self.matriz[fila_idx][col_idx] = {
                    "id": asiento.id,
                    "nombre": f"{asiento.row_label}-{asiento.number}",
                    "status": asiento.status,
                    # --- NUEVOS DATOS IMPORTANTES ---
                    "price": asiento.zone.price,       # Precio Real
                    "zone_name": asiento.zone.name,    # Nombre Zona (VIP/General)
                    "event_title": asiento.zone.event.title # Título del evento
                }

    def obtener_json(self):
        return self.matriz
    
    def buscar_consecutivos(self, cantidad):
        """ 
        Algoritmo para encontrar N asientos juntos.
        Retorna: (fila, columna_inicio) o None 
        """
        for i in range(self.filas):
            consecutivos = 0
            inicio = -1
            for j in range(self.columnas):
                if self.matriz[i][j] and self.matriz[i][j]['status'] == 'AVAILABLE':
                    if consecutivos == 0: inicio = j
                    consecutivos += 1
                    if consecutivos == cantidad:
                        return {"fila": f"F{i+1}", "asientos": [x+1 for x in range(inicio, j+1)]}
                else:
                    consecutivos = 0
        return None

# --- IMPLEMENTACIÓN DE LISTA ENLAZADA Y MERGE SORT (REQUERIMIENTO ED) ---

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def to_list(self):
        """Convierte la lista enlazada a una lista de Python estándar"""
        result = []
class MatrizAsientos:
    """
    Representación en memoria de la sala.
    Aumentamos filas a 20 para que quepan varias zonas.
    """
    def __init__(self, filas=20, columnas=10): # <--- AUMENTADO A 20 FILAS
        self.filas = filas
        self.columnas = columnas
        self.matriz = [[None for _ in range(columnas)] for _ in range(filas)]

    def cargar_desde_db(self, lista_asientos_queryset):
        for asiento in lista_asientos_queryset:
            # Parseamos "F1" -> índice 0
            # Si el backend genera filas altas (F15), esto funcionará bien
            fila_idx = int(asiento.row_label.replace("F", "")) - 1
            col_idx = asiento.number - 1
            
            if 0 <= fila_idx < self.filas and 0 <= col_idx < self.columnas:
                self.matriz[fila_idx][col_idx] = {
                    "id": asiento.id,
                    "nombre": f"{asiento.row_label}-{asiento.number}",
                    "status": asiento.status,
                    # --- NUEVOS DATOS IMPORTANTES ---
                    "price": asiento.zone.price,       # Precio Real
                    "zone_name": asiento.zone.name,    # Nombre Zona (VIP/General)
                    "event_title": asiento.zone.event.title # Título del evento
                }

    def obtener_json(self):
        return self.matriz
    
    def buscar_consecutivos(self, cantidad):
        """ 
        Algoritmo para encontrar N asientos juntos.
        Retorna: (fila, columna_inicio) o None 
        """
        for i in range(self.filas):
            consecutivos = 0
            inicio = -1
            for j in range(self.columnas):
                if self.matriz[i][j] and self.matriz[i][j]['status'] == 'AVAILABLE':
                    if consecutivos == 0: inicio = j
                    consecutivos += 1
                    if consecutivos == cantidad:
                        return {"fila": f"F{i+1}", "asientos": [x+1 for x in range(inicio, j+1)]}
                else:
                    consecutivos = 0
        return None

# --- IMPLEMENTACIÓN DE LISTA ENLAZADA Y MERGE SORT (REQUERIMIENTO ED) ---

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def to_list(self):
        """Convierte la lista enlazada a una lista de Python estándar"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def merge_sort(self, head, ascending=True):
        if not head or not head.next:
            return head

        # Encontrar el medio
        middle = self.get_middle(head)
        next_to_middle = middle.next
        middle.next = None

        # Recursión
        left = self.merge_sort(head, ascending)
        right = self.merge_sort(next_to_middle, ascending)

        # Merge
        sorted_list = self.sorted_merge(left, right, ascending)
        return sorted_list

    def get_middle(self, head):
        if not head:
            return head
        slow = head
        fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    def sorted_merge(self, a, b, ascending=True):
        result = None
        if not a:
            return b
        if not b:
            return a

        # Ordenar por FECHA (date)
        # Si ascending es True: a <= b
        # Si ascending es False: a >= b
        should_pick_a = (a.data.date <= b.data.date) if ascending else (a.data.date >= b.data.date)

        if should_pick_a:
            result = a
            result.next = self.sorted_merge(a.next, b, ascending)
        else:
            result = b
            result.next = self.sorted_merge(a, b.next, ascending)
        return result

    def sort(self, ascending=True):
        """Método público para ordenar la lista actual"""
        self.head = self.merge_sort(self.head, ascending)