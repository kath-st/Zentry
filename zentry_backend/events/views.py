from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from .models import Event, Seat, Zone
from .services import importar_eventos_ticketmaster, generar_asientos_automaticos
from .estructuras import MatrizAsientos, LinkedList
from .serializers import EventSerializer, EventAdminSerializer
from rest_framework.permissions import AllowAny, IsAdminUser
from orders.models import Ticket

# 1. API para Listar Eventos (Público)
class EventListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def list(self, request, *args, **kwargs):
        """
        Sobreescribimos el método list para usar nuestra Lista Enlazada y Merge Sort.
        """
        # 1. Obtener datos de la BD (QuerySet)
        queryset = self.get_queryset()

        # 2. Llenar la Lista Enlazada
        linked_list = LinkedList()
        for event in queryset:
            linked_list.append(event)
        
        # 3. Ordenar usando Merge Sort (Por fecha)
        # Leemos el parámetro 'order' de la URL (default: 'asc')
        order_param = request.query_params.get('order', 'asc')
        ascending = (order_param.lower() == 'asc')
        
        linked_list.sort(ascending=ascending)

        # 4. Convertir de nuevo a lista para serializar
        sorted_events = linked_list.to_list()

        # 5. Serializar y responder
        serializer = self.get_serializer(sorted_events, many=True)
        return Response(serializer.data)

# 2. API para Importar desde Ticketmaster (Admin)
class ImportEventsView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            nuevos = importar_eventos_ticketmaster()
            return Response({"message": f"Se importaron {len(nuevos)} eventos.", "data": nuevos})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

# 3. API del Mapa de Asientos (Usa la Estructura Matriz)
class SeatMapView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, event_id):
        # Obtenemos asientos planos de la BD
        asientos_bd = Seat.objects.filter(zone__event_id=event_id)
        
        # Instanciamos la Estructura de Datos
        sala = MatrizAsientos(filas=10, columnas=10)
        sala.cargar_desde_db(asientos_bd)
        
        # Usamos el algoritmo de búsqueda (Opcional, para mostrar al profe)
        sugerencia = sala.buscar_consecutivos(2) # Busca 2 juntos
        
        return Response({
            "mapa_matriz": sala.obtener_json(), # Esto va al Frontend para dibujarse
            "sugerencia_inteligente": sugerencia
        })
    
class EventCreateView(APIView):
    # permission_classes = [IsAdminUser] # Descomenta para restringir solo a admins

    def post(self, request):
        serializer = EventAdminSerializer(data=request.data)
        if serializer.is_valid():
            datos = serializer.validated_data
            zones_data = datos.pop('zones_input', []) # Sacamos las zonas aparte
            
            # A. Crear el Evento
            # Generamos un ID falso de Ticketmaster si no existe
            import uuid
            if 'tm_id' not in datos: 
                datos['tm_id'] = f"MANUAL-{uuid.uuid4().hex[:8]}"
            
            event = Event.objects.create(**datos)

            # B. Crear Zonas y Asientos (Matriz)
            if not zones_data:
                # Si no mandan zonas, creamos una General por defecto
                zones_data = [{'name': 'General', 'price': 50.00}]
            
            for zone_info in zones_data:
                zona = Zone.objects.create(event=event, **zone_info)
                generar_asientos_automaticos(zona) # <--- ¡MAGIA DE ESTRUCTURA!

            return Response({
                "message": "Evento creado y matriz de asientos generada.",
                "event_id": event.id,
                "title": event.title
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 2. MODIFICAR Y ELIMINAR (PUT, DELETE)
class EventAdminDetailView(APIView):
    # permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return None

    def put(self, request, pk):
        """ Modificar Evento """
        event = self.get_object(pk)
        if not event:
            return Response({"error": "Evento no encontrado"}, status=404)

        serializer = EventAdminSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Evento actualizado", "data": serializer.data})
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        """ Eliminar Evento (Soft Delete o Hard Delete) """
        event = self.get_object(pk)
        if not event:
            return Response({"error": "Evento no encontrado"}, status=404)
        
        # Antes de borrar el evento, borramos explícitamente los tickets asociados
        # Buscamos tickets cuyo asiento (seat) pertenezca a una zona (zone) de este evento
        tickets_asociados = Ticket.objects.filter(seat__zone__event=event)
        
        count = tickets_asociados.count()
        tickets_asociados.delete() # Borramos los tickets (liberamos la protección)
        # Django borra en cascada (Event -> Zones -> Seats -> Tickets)
        event.delete()
        return Response({"message": "Evento y todos sus datos eliminados correctamente."}, status=204)