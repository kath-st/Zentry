import os
import django
import sys

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zentry_django.settings')
django.setup()

from events.models import Event, Zone, Asiento
from datetime import datetime, timedelta

print("Creando eventos...")

eventos_data = [
    {
        'name': 'Concierto Rock Nacional',
        'venue': 'Estadio Nacional',
        'date': datetime.now() + timedelta(days=30),
        'description': 'Gran concierto de rock nacional',
        'direccion': 'Av. José Díaz 1390, Lima'
    },
    {
        'name': 'Festival Electrónico',
        'venue': 'Parque de la Exposición',
        'date': datetime.now() + timedelta(days=45),
        'description': 'El mejor festival electrónico',
        'direccion': 'Av. 28 de Julio, Lima'
    },
    {
        'name': 'Teatro Musical',
        'venue': 'Gran Teatro Nacional',
        'date': datetime.now() + timedelta(days=15),
        'description': 'Musical clásico',
        'direccion': 'Av. Javier Prado Este 2225, San Borja'
    },
    {
        'name': 'Partido de Fútbol',
        'venue': 'Estadio Monumental',
        'date': datetime.now() + timedelta(days=7),
        'description': 'Partido clasificatorio',
        'direccion': 'Av. Tomás Valle, Lima'
    }
]

for evento_data in eventos_data:
    evento, created = Event.objects.get_or_create(
        name=evento_data['name'],
        defaults=evento_data
    )
    if created:
        print(f"✓ Creado: {evento.name}")
        
        zone_data = [
            {'code': 'VIP', 'name': 'VIP', 'capacity': 500, 'price': 200.00, 'filas': 10, 'columnas': 50},
            {'code': 'PLA', 'name': 'Platea', 'capacity': 1500, 'price': 120.00, 'filas': 30, 'columnas': 50},
            {'code': 'GEN', 'name': 'General', 'capacity': 3000, 'price': 50.00, 'filas': 60, 'columnas': 50},
        ]
        
        for zd in zone_data:
            zona = Zone.objects.create(event=evento, **zd)
            
            for fila_num in range(1, zd['filas'] + 1):
                fila_letra = chr(64 + fila_num) if fila_num <= 26 else f"A{fila_num-26}"
                for col_num in range(1, zd['columnas'] + 1):
                    Asiento.objects.create(
                        zona=zona,
                        fila=fila_letra,
                        columna=col_num
                    )
            
            print(f"  → Zona {zona.name} creada con {zd['filas']*zd['columnas']} asientos")
    else:
        print(f"- Ya existe: {evento.name}")

print("\nListo! Eventos creados.")
print(f"Total eventos: {Event.objects.count()}")
print(f"Total zonas: {Zone.objects.count()}")
print(f"Total asientos: {Asiento.objects.count()}")

