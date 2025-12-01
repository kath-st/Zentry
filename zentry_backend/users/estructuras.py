class NodoUsuario:
    def __init__(self, dni, email):
        self.dni = int(dni)   # Clave de ordenamiento
        self.email = email
        self.izquierda = None
        self.derecha = None

#====================REGISTRO DE USUARIOS CON BST====================#
class ArbolUsuariosBST:
    def __init__(self):
        self.raiz = None

    def insertar(self, dni, email):
        if not self.raiz:
            self.raiz = NodoUsuario(dni, email)
        else:
            self._insertar_recursivo(self.raiz, int(dni), email)

    def _insertar_recursivo(self, nodo_actual, dni, email):
        if dni < nodo_actual.dni:
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = NodoUsuario(dni, email)
            else:
                self._insertar_recursivo(nodo_actual.izquierda, dni, email)
        elif dni > nodo_actual.dni:
            if nodo_actual.derecha is None:
                nodo_actual.derecha = NodoUsuario(dni, email)
            else:
                self._insertar_recursivo(nodo_actual.derecha, dni, email)
        # Si es igual, no hacemos nada (ya existe)

    def _buscar_recursivo(self, nodo_actual, dni):
        if nodo_actual is None:
            return False
        if dni == nodo_actual.dni:
            return True
        
        if dni < nodo_actual.dni:
            return self._buscar_recursivo(nodo_actual.izquierda, dni)
        else:
            return self._buscar_recursivo(nodo_actual.derecha, dni)
        
    def existe(self, dni):
        return self._buscar_recursivo(self.raiz, int(dni))

# Instancia Global (Memoria RAM)
indice_usuarios = ArbolUsuariosBST()

#================================INICIO DE SESION=================================#
class TablaHashUsuarios:
    """
    Estructura para búsqueda O(1) basada en Email.
    Clave: Email
    Valor: ID del Usuario (o objeto Usuario)
    """
    def __init__(self):
        self.tabla = {} # Usamos el diccionario nativo de Python que es una Hash Table

    def insertar(self, email, usuario_id):
        self.tabla[email] = usuario_id #si el usuario ya existe, se actualiza

    def obtener(self, email):
        return self.tabla.get(email) # Devuelve None (si no existe), o el ID del usuario

    def existe(self, email):
        return email in self.tabla # Usado en login para verificar existencia

    def eliminar(self, email):
        if email in self.tabla:
            del self.tabla[email] # Usado para actualizar email

# Instancia Global para el Login
tabla_login = TablaHashUsuarios()