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