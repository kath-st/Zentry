from collections import deque

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.anterior = None
        self.siguiente = None


class ListaDoblementeEnlazada:
    """
    Implementación de lista doblemente enlazada.
    Usada para representar la selección de asientos (resumen local).
    Puede tener un límite de elementos (máx 5 tickets).
    """

    def __init__(self, max_longitud=None):
        self.cabeza = None
        self.cola = None
        self.longitud = 0
        self.max_longitud = max_longitud

    def agregar(self, valor):
        """Agrega un valor al final de la lista."""
        if self.max_longitud is not None and self.longitud >= self.max_longitud:
            raise Exception("Se alcanzó el límite de elementos.")
        
        nuevo = Nodo(valor)

        if self.cabeza is None:
            self.cabeza = self.cola = nuevo
        else:
            self.cola.siguiente = nuevo
            nuevo.anterior = self.cola
            self.cola = nuevo

        self.longitud += 1
        return nuevo

    def eliminar_ultimo(self):
        """Elimina el último elemento (ideal para 'Deshacer')."""
        if self.cola is None:
            return None
        
        nodo = self.cola

        if nodo.anterior:
            self.cola = nodo.anterior
            self.cola.siguiente = None
        else:
            self.cabeza = self.cola = None
        
        nodo.anterior = nodo.siguiente = None
        self.longitud -= 1

        return nodo.valor

    def eliminar(self, nodo):
        """Elimina un nodo específico."""
        if nodo is None:
            return
        
        if nodo.anterior:
            nodo.anterior.siguiente = nodo.siguiente
        else:
            self.cabeza = nodo.siguiente
        
        if nodo.siguiente:
            nodo.siguiente.anterior = nodo.anterior
        else:
            self.cola = nodo.anterior

        nodo.anterior = nodo.siguiente = None
        self.longitud -= 1

    def a_lista(self):
        """Convierte la lista enlazada a una lista Python normal."""
        resultado = []
        actual = self.cabeza

        while actual:
            resultado.append(actual.valor)
            actual = actual.siguiente

        return resultado

# QUICKSORT
def ordenamiento_rapido(arreglo):
    """
    Recibe un arreglo de tuplas comparables (p.ej. (fila, columna, id)).
    """
    if len(arreglo) <= 1:
        return arreglo
    
    pivote = arreglo[len(arreglo) // 2]

    menores = [x for x in arreglo if x < pivote]
    iguales  = [x for x in arreglo if x == pivote]
    mayores = [x for x in arreglo if x > pivote]

    return ordenamiento_rapido(menores) + iguales + ordenamiento_rapido(mayores)

def busqueda_binaria(arreglo, objetivo):
    """
    Búsqueda binaria sobre arreglo ordenado.
    """
    izquierda, derecha = 0, len(arreglo) - 1

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2

        if arreglo[medio] == objetivo:
            return medio
        elif arreglo[medio] < objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1

    return -1  # no encontrado

class Pila:    
    def __init__(self):
        self.datos = []

    def apilar(self, valor):
        self.datos.append(valor)

    def desapilar(self):
        return self.datos.pop() if self.datos else None

    def vacia(self):
        return len(self.datos) == 0

class Cola:
    def __init__(self):
        self.datos = deque()

    def encolar(self, valor):
        self.datos.append(valor)

    def desencolar(self):
        return self.datos.popleft() if self.datos else None

    def vacia(self):
        return len(self.datos) == 0
