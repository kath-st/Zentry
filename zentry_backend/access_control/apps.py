from django.apps import AppConfig


class AccessControlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'access_control'

    def ready(self):
        import sys
        if 'migrate' in sys.argv: return

        try:
            from orders.models import Ticket
            from .estructuras import validador_acceso
            
            # Solo cargamos tickets de órdenes PAGADAS
            tickets = Ticket.objects.select_related('order').all()
            count = 0
            for t in tickets:
                validador_acceso.cargar_ticket(t.ticket_code)
                count += 1
            
            print(f"🛡️ [SET] {count} tickets cargados en memoria para validación O(1).")
        except Exception as e:
            print(f"Error cargando sets: {e}")
