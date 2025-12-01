import requests
from django.conf import settings
from django.utils.dateparse import parse_datetime
from .models import Event, Zone, Seat
import requests

#ESTA FUNCION DE AQUI LA USE USANDO POSTMAAAAAN CREO QUE NO ESTA IMPLEMENTADA EN NINGUN LADO, ES MÁS QUE NADA PARA CARGAR LA BASE DE DATOS SIN TENER QUE HACERLO MANUALMENTE EVENTO POR EVENTO (http://localhost:8000/api/events/import/tm/)
def importar_eventos_ticketmaster(keyword="concert"):
    """
    1. Conecta a la API de Ticketmaster.
    2. Descarga eventos.
    3. Genera la Matriz de Asientos localmente.
    """
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": settings.TM_API_KEY,
        "keyword": keyword,
        "size": 30, # Traemos 30 
        "sort": "date,asc"
    }

    response = requests.get(url, params=params)
    data = response.json()

    eventos_creados = []

    if '_embedded' in data and 'events' in data['_embedded']:
        for item in data['_embedded']['events']:
            tm_id = item.get('id')
            
            # Evitar duplicados
            if not tm_id or Event.objects.filter(tm_id=tm_id).exists():
                continue

            # Extraer datos
            title = item.get('name', 'Untitled event')

            # Imagen: elegir la primera url disponible
            image = None
            for img in item.get('images', []):
                if img.get('url'):
                    image = img['url']
                    break

            # Fecha: preferir dateTime, si no usar localDate
            fecha_str = None
            fechas = item.get('dates', {}).get('start', {})
            fecha_str = fechas.get('dateTime') or fechas.get('localDate')

            # Venue
            venue = None
            try:
                venue = item['_embedded']['venues'][0].get('name')
            except (KeyError, IndexError, TypeError):
                venue = None

            # Categoría (segment/genre)
            cat = None
            try:
                clas = item.get('classifications', [])
                if clas:
                    cat = clas[0].get('segment', {}).get('name') or clas[0].get('genre', {}).get('name')
            except Exception:
                cat = None

            # 1. Crear Evento en BD
            evento = Event.objects.create(
                tm_id=tm_id,
                title=title,
                image_url=image or '',
                date=parse_datetime(fecha_str) if fecha_str else None,
                venue=venue or '',
                category=cat or ''
            )

            # 2. Crear Zona "General" Automáticamente
            zona = Zone.objects.create(event=evento, name="General", price=100.00)

            # 3. Generar Asientos Automáticamente
            generar_asientos_automaticos(zona)

            #4. Crear Zona "VIP" Automáticamente
            zona_vip = Zone.objects.create(event=evento, name="VIP", price=200.00)

            # 5. Generar Asientos Automáticamente para VIP
            generar_asientos_automaticos(zona_vip)
            
            eventos_creados.append(title)
    
    return eventos_creados

def generar_asientos_automaticos(zone_instance):
    """
    Genera asientos dependiendo del nombre de la zona para evitar colisiones.
    """
    asientos = []
    
    # Lógica para separar filas por zona
    if "VIP" in zone_instance.name.upper():
        rango_filas = range(1, 6) # F1 a F5 (VIP al frente)
    else:
        rango_filas = range(6, 16) # F6 a F15 (General atrás)

    for f in rango_filas: 
        for c in range(1, 11): # Asientos 1 a 10
            asientos.append(Seat(
                zone=zone_instance,
                row_label=f"F{f}",
                number=c,
                status='AVAILABLE'
            ))
    Seat.objects.bulk_create(asientos)