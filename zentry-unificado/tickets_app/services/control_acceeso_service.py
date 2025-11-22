from collections import deque # Estructura de Datos: Cola (Queue)
from django.db.models import Q # Para consultas eficientes
from django.utils import timezone
from ..models import Ticket 

class ControlAccesoService:
    """
    Servicio encargado de la lógica de validación de tickets utilizando
    estructuras de datos para optimizar el rendimiento O(1) de las búsquedas.
    """
    
    # Estructuras de Datos en memoria:
    # 1. Hash Set (Set): Para verificar existencia y uso en tiempo O(1) promedio.
    codigos_validos = set()
    codigos_usados = set() 
    
    # 2. Cola (Deque): Para simular el orden de llegada a la fila (FIFO).
    fila_ingreso = deque()

    def __init__(self):
        """Inicializa el servicio sin cargar datos hasta que sea necesario."""
        self._initialized = False

    def _cargar_tickets_validos(self):
        """
        Consulta la DB y carga los códigos en los Hash Sets. 
        Esto se hace una vez al iniciar el servicio (o por evento).
        """
        if self._initialized:
            return
            
        print("ControlAccesoService: Cargando Hash Sets desde la base de datos...")
        self.codigos_validos.clear()
        self.codigos_usados.clear()
        
        # Consultamos solo los campos necesarios para ser más ligeros
        tickets = Ticket.objects.values('codigo_ticket', 'esta_usado')
        
        for ticket in tickets:
            codigo = ticket['codigo_ticket']
            self.codigos_validos.add(codigo) # Todo ticket existente es válido
            
            if ticket['esta_usado']:
                self.codigos_usados.add(codigo) # Los ya usados se van al Hash Set de usados
        
        self._initialized = True

    # --- Funcionalidades de Cola (FIFO) ---

    def registrar_en_fila(self, codigo_ticket: str):
        """Registra el ticket que acaba de pasar la validación en la fila de ingreso (simulación)."""
        self.fila_ingreso.append(f"[{timezone.now().strftime('%H:%M:%S')}] {codigo_ticket}")
    
    # --- Funcionalidades de Hash Set (O(1)) ---
    
    def validar_ticket(self, codigo_a_validar: str) -> dict:
        """
        Verifica la validez y unicidad del ticket.
        """
        # Cargar datos de tickets si aún no se ha hecho
        self._cargar_tickets_validos()
        
        # 1. Verificación de Validez (Hash Set: O(1))
        if codigo_a_validar not in self.codigos_validos:
            return {"status": "DENEGADO", "mensaje": "TICKET INVÁLIDO o inexistente."}

        # 2. Verificación de Uso (Hash Set: O(1))
        if codigo_a_validar in self.codigos_usados:
            return {"status": "DENEGADO", "mensaje": "TICKET YA UTILIZADO. Acceso denegado."}

        # 3. Marcar como USADO (Acceso concedido)
        
        try:
            # A. Actualizar la base de datos (Persistencia)
            ticket_db = Ticket.objects.get(codigo_ticket=codigo_a_validar)
            ticket_db.esta_usado = True
            ticket_db.fecha_uso = timezone.now()
            ticket_db.save()
            
            # B. Actualizar el Hash Set en memoria para consistencia O(1)
            self.codigos_usados.add(codigo_a_validar) 
            
            # C. Registrar en la fila de ingreso
            self.registrar_en_fila(codigo_a_validar)
            
            return {"status": "✅ ACCESO CONCEDIDO", "mensaje": "Bienvenido."}
            
        except Ticket.DoesNotExist:
            # Fallo de consistencia (Debería ser raro si el Hash Set se cargó bien)
            return {"status": "ERROR", "mensaje": "Fallo de consistencia: Código existe, pero no en DB."}