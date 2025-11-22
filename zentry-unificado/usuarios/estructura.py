class Nodo:
    def __init__(self, datos):
        self.datos = datos
        self.siguiente = None

class Pila:
    def __init__(self):
        self.tope = None
        self.tamaño = 0
    
    def esta_vacia(self):
        return self.tope is None
    
    def apilar(self, compra):
        nuevo_nodo = Nodo(compra)
        nuevo_nodo.siguiente = self.tope
        self.tope = nuevo_nodo
        self.tamaño += 1
    
    def desapilar(self):
        if self.esta_vacia():
            return None
        compra = self.tope.datos
        self.tope = self.tope.siguiente
        self.tamaño -= 1
        return compra
    
    def ver_tope(self):
        if self.esta_vacia():
            return None
        return self.tope.datos
    
    def obtener_historial(self):
        historial = []
        actual = self.tope
        while actual:
            historial.append(actual.datos)
            actual = actual.siguiente
        return historial

class TablaHash:
    def __init__(self, tamaño=100):
        self.tamaño = tamaño
        self.tabla = [[] for _ in range(tamaño)]
        self.contador = 0
    
    def _hash(self, valor):
        # Función hash para strings (DNI o correo)
        hash_valor = 0
        for char in str(valor):
            hash_valor = (hash_valor * 31 + ord(char)) % self.tamaño
        return hash_valor
    
    def insertar(self, clave, valor):
        indice = self._hash(clave)
        # Verificar si la clave ya existe
        for item in self.tabla[indice]:
            if item[0] == clave:
                return False  # La clave ya existe
        
        self.tabla[indice].append((clave, valor))
        self.contador += 1
        
        # Factor de carga > 0.7, redimensionar
        if self.contador / self.tamaño > 0.7:
            self._redimensionar()
        
        return True
    
    def buscar(self, clave):
        indice = self._hash(clave)
        for item in self.tabla[indice]:
            if item[0] == clave:
                return item[1]
        return None
    
    def eliminar(self, clave):
        indice = self._hash(clave)
        for i, item in enumerate(self.tabla[indice]):
            if item[0] == clave:
                self.tabla[indice].pop(i)
                self.contador -= 1
                return True
        return False
    
    def _redimensionar(self):
        self.tamaño *= 2
        tabla_antigua = self.tabla
        self.tabla = [[] for _ in range(self.tamaño)]
        self.contador = 0
        
        # Reinsertando elementos
        for lista in tabla_antigua:
            for clave, valor in lista:
                self.insertar(clave, valor)


