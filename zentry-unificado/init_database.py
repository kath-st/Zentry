#!/usr/bin/env python
"""
Script de inicialización para Zentry Django.
Crea datos de prueba en la base de datos.
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zentry_django.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from events.models import Event, Zone
from reservations.models import Reservation


def create_sample_data():
    """Crea datos de ejemplo para testing."""
    
    print("🚀 Creando datos de ejemplo para Zentry...")
    
    # Crear superusuario si no existe
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@zentry.com',
            password='admin123'
        )
        print(f"✅ Superusuario creado: {admin_user.username}")
    
    # Crear usuarios de prueba
    users_data = [
        {'username': 'katherine', 'email': 'katherine@test.com', 'password': 'test123'},
        {'username': 'testuser1', 'email': 'test1@test.com', 'password': 'test123'},
        {'username': 'testuser2', 'email': 'test2@test.com', 'password': 'test123'},
    ]
    
    for user_data in users_data:
        if not User.objects.filter(username=user_data['username']).exists():
            user = User.objects.create_user(**user_data)
            print(f"✅ Usuario creado: {user.username}")
    
    # Crear eventos de ejemplo
    events_data = [
        {
            'name': 'Festival Rock Nacional 2025',
            'date': timezone.now() + timedelta(days=45),
            'venue': 'Estadio El Campín',
            'description': 'El mejor festival de rock del país con las mejores bandas nacionales.'
        },
        {
            'name': 'Concierto Electrónico Miami',
            'date': timezone.now() + timedelta(days=60),
            'venue': 'Centro de Convenciones',
            'description': 'Una noche de música electrónica con los mejores DJs internacionales.'
        },
        {
            'name': 'Jazz en el Parque',
            'date': timezone.now() + timedelta(days=30),
            'venue': 'Parque Simón Bolívar',
            'description': 'Un evento íntimo con los mejores exponentes del jazz colombiano.'
        }
    ]
    
    events = []
    for event_data in events_data:
        event, created = Event.objects.get_or_create(
            name=event_data['name'],
            defaults=event_data
        )
        if created:
            print(f"✅ Evento creado: {event.name}")
        events.append(event)
    
    # Crear zonas para cada evento
    zones_data = [
        # Festival Rock Nacional
        [
            {'code': 'VIP', 'name': 'Zona VIP Premium', 'capacity': 200, 'price': 250000},
            {'code': 'GENERAL', 'name': 'Zona General', 'capacity': 5000, 'price': 120000},
            {'code': 'PALCO', 'name': 'Palco Presidencial', 'capacity': 50, 'price': 500000},
        ],
        # Concierto Electrónico
        [
            {'code': 'VIP', 'name': 'VIP Experience', 'capacity': 100, 'price': 180000},
            {'code': 'GENERAL', 'name': 'Pista General', 'capacity': 3000, 'price': 85000},
            {'code': 'TERRAZA', 'name': 'Terraza Premium', 'capacity': 150, 'price': 300000},
        ],
        # Jazz en el Parque
        [
            {'code': 'VIP', 'name': 'Mesa VIP', 'capacity': 80, 'price': 150000},
            {'code': 'GENERAL', 'name': 'Zona General', 'capacity': 1000, 'price': 60000},
        ]
    ]
    
    for i, event in enumerate(events):
        for zone_data in zones_data[i]:
            zone, created = Zone.objects.get_or_create(
                event=event,
                code=zone_data['code'],
                defaults=zone_data
            )
            if created:
                print(f"✅ Zona creada: {event.name} - {zone.name}")
    
    print("\n🎉 ¡Datos de ejemplo creados exitosamente!")
    print("\n📊 Resumen:")
    print(f"- Usuarios: {User.objects.count()}")
    print(f"- Eventos: {Event.objects.count()}")
    print(f"- Zonas: {Zone.objects.count()}")
    
    print("\n🔑 Credenciales de acceso:")
    print("- Superusuario: admin / admin123")
    print("- Usuario de prueba: katherine / test123")
    print("- Usuario de prueba: testuser1 / test123")
    
    print("\n🌐 URLs disponibles:")
    print("- Admin: http://localhost:8000/admin/")
    print("- API Carrito: http://localhost:8000/api/cart/")


def main():
    """Función principal."""
    try:
        create_sample_data()
    except Exception as e:
        print(f"❌ Error al crear datos: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()