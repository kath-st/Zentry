import requests
from django.conf import settings
from django.utils.dateparse import parse_datetime
from .models import Event, Zone, Seat

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
        "size": 5, # Traemos solo 5 para probar
        "sort": "date,asc"
    }

    response = requests.get(url, params=params)
    data = response.json()

    eventos_creados = []

    if '_embedded' in data:
        for item in data['_embedded']['events']:
            tm_id = item['id']
            
            # Evitar duplicados
            if Event.objects.filter(tm_id=tm_id).exists():
                continue

            # Extraer datos
            title = item['name']
            try:
                image = item['images'][0]['url'] # Tomamos la primera imagen
                fecha_str = item['dates']['start']['dateTime']
                venue = item['_embedded']['venues'][0]['name']
                cat = item['classifications'][0]['segment']['name']
            except (KeyError, IndexError):
                continue # Si faltan datos, saltamos

            # 1. Crear Evento en BD
            evento = Event.objects.create(
                tm_id=tm_id,
                title=title,
                image_url=image,
                date=parse_datetime(fecha_str),
                venue=venue,
                category=cat
            )

            # 2. Crear Zona "General" Automáticamente
            zona = Zone.objects.create(event=evento, name="General", price=45.00)

            # 3. Generar Asientos Automáticamente
            generar_asientos_automaticos(zona)
            
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