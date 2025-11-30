class ValidadorSet:
    def __init__(self):
        # Un Set es internamente una Tabla Hash, búsqueda O(1)
        self.codigos_validos = set()

    def cargar_ticket(self, codigo):
        self.codigos_validos.add(codigo)

    def es_autentico(self, codigo):
        # Esta operación es O(1)
        return codigo in self.codigos_validos

# Instancia Global
validador_acceso = ValidadorSet()