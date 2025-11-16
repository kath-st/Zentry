from django.core.management.base import BaseCommand
from eventos.modulo.reservas.services import GestorDeReservas  


class Command(BaseCommand):
    help = "Libera las reservas expiradas y desactiva las sesiones vencidas."

    def handle(self, *args, **options):
        gestor = GestorDeReservas()
        liberadas = gestor.liberar_expiradas()

        self.stdout.write(self.style.SUCCESS(
            f"Reservas liberadas: {len(liberadas)}"
        ))
