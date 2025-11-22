"""
Endpoints API para el Catálogo Dinámico de Eventos.
Componente de Cerna Sifuentes - Estructura de Datos
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from datetime import datetime
from core.services.event_catalog_service import EventCatalogService
from core.domain.event_catalog import EventCatalog, SortCriteria
from api.serializers_catalog import EventCatalogSerializer, EventCatalogListSerializer
from events.models import Event, Zone


# Instancia global del servicio de catálogo
# En producción, usar inyección de dependencias
catalog_service = EventCatalogService()


class EventCatalogViewSet(viewsets.ViewSet):
    """
    ViewSet para el Catálogo Dinámico de Eventos.
    
    Endpoints:
    - GET /api/catalog/                     - Obtener todos los eventos
    - GET /api/catalog/{id}/                - Obtener evento específico
    - POST /api/catalog/                    - Crear nuevo evento
    - PATCH /api/catalog/{id}/              - Actualizar evento
    - DELETE /api/catalog/{id}/             - Eliminar evento
    - GET /api/catalog/search/              - Búsqueda avanzada
    - GET /api/catalog/sort/by-date/        - Ordenar por fecha
    - GET /api/catalog/sort/by-price/       - Ordenar por precio
    - GET /api/catalog/sort/by-popularity/  - Ordenar por popularidad
    - GET /api/catalog/trending/            - Eventos en tendencia
    - GET /api/catalog/featured/            - Eventos destacados
    - GET /api/catalog/statistics/          - Estadísticas generales
    """

    def list(self, request: Request) -> Response:
        """
        GET /api/catalog/
        Obtiene todos los eventos del catálogo.
        
        Query params:
        - sort_by: date, price, popularity (opcional)
        - limit: número máximo de eventos (opcional)
        """
        sort_by = request.query_params.get('sort_by')
        limit = request.query_params.get('limit', type=int)

        events = []
        if sort_by == 'date':
            events = catalog_service.sort_by_date()
        elif sort_by == 'price':
            events = catalog_service.sort_by_price()
        elif sort_by == 'popularity':
            events = catalog_service.sort_by_popularity()
        else:
            events = catalog_service.get_all_events()

        if limit:
            events = events[:limit]

        serializer = EventCatalogSerializer(events, many=True)
        return Response({
            'count': len(events),
            'results': serializer.data
        })

    def retrieve(self, request: Request, pk=None) -> Response:
        """
        GET /api/catalog/{id}/
        Obtiene un evento específico por ID.
        """
        try:
            event_id = int(pk)
            event = catalog_service.get_event(event_id)
            
            if not event:
                return Response(
                    {'error': f'Evento con ID {event_id} no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = EventCatalogSerializer(event)
            return Response(serializer.data)
        except ValueError:
            return Response(
                {'error': 'ID inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def create(self, request: Request) -> Response:
        """
        POST /api/catalog/
        Crea un nuevo evento en el catálogo.
        
        Body JSON:
        {
            "id": 1,
            "name": "Concert Name",
            "venue": "Venue Name",
            "date": "2024-12-31T20:00:00Z",
            "min_price": 50.0,
            "max_price": 150.0,
            "total_capacity": 5000,
            "artist_name": "Artist Name"
        }
        """
        serializer = EventCatalogSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            event_data = serializer.validated_data
            event = EventCatalog(**event_data)
            added_event = catalog_service.add_event(event)
            
            return Response(
                EventCatalogSerializer(added_event).data,
                status=status.HTTP_201_CREATED
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def partial_update(self, request: Request, pk=None) -> Response:
        """
        PATCH /api/catalog/{id}/
        Actualiza parcialmente un evento existente.
        """
        try:
            event_id = int(pk)
            event = catalog_service.update_event(event_id, **request.data)
            
            if not event:
                return Response(
                    {'error': f'Evento con ID {event_id} no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = EventCatalogSerializer(event)
            return Response(serializer.data)
        except ValueError:
            return Response(
                {'error': 'ID inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request: Request, pk=None) -> Response:
        """
        DELETE /api/catalog/{id}/
        Elimina un evento del catálogo.
        """
        try:
            event_id = int(pk)
            success = catalog_service.delete_event(event_id)
            
            if not success:
                return Response(
                    {'error': f'Evento con ID {event_id} no encontrado'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            return Response(
                {'message': f'Evento {event_id} eliminado correctamente'},
                status=status.HTTP_204_NO_CONTENT
            )
        except ValueError:
            return Response(
                {'error': 'ID inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def search(self, request: Request) -> Response:
        """
        GET /api/catalog/search/?q=search_term&type=name|artist|venue
        Búsqueda avanzada de eventos.
        
        Query params:
        - q: término de búsqueda
        - type: name, artist, venue (por defecto: name)
        """
        query = request.query_params.get('q', '').strip()
        search_type = request.query_params.get('type', 'name')

        if not query:
            return Response(
                {'error': 'Parámetro "q" requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        results = []
        if search_type == 'name':
            results = catalog_service.search_by_name(query)
        elif search_type == 'artist':
            results = catalog_service.search_by_artist(query)
        elif search_type == 'venue':
            results = catalog_service.search_by_venue(query)
        else:
            return Response(
                {'error': 'Tipo de búsqueda inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = EventCatalogSerializer(results, many=True)
        return Response({
            'query': query,
            'type': search_type,
            'count': len(results),
            'results': serializer.data
        })

    @action(detail=False, methods=['get'])
    def upcoming(self, request: Request) -> Response:
        """
        GET /api/catalog/upcoming/
        Obtiene todos los eventos futuros.
        """
        events = catalog_service.search_upcoming_events()
        serializer = EventCatalogSerializer(events, many=True)
        return Response({
            'count': len(events),
            'results': serializer.data
        })

    @action(detail=False, methods=['get'])
    def available(self, request: Request) -> Response:
        """
        GET /api/catalog/available/
        Obtiene eventos con tickets disponibles.
        """
        events = catalog_service.search_available_events()
        serializer = EventCatalogSerializer(events, many=True)
        return Response({
            'count': len(events),
            'results': serializer.data
        })

    @action(detail=False, methods=['get'])
    def price_range(self, request: Request) -> Response:
        """
        GET /api/catalog/price_range/?min=50&max=200
        Obtiene eventos en un rango de precios.
        
        Query params:
        - min: precio mínimo
        - max: precio máximo
        """
        try:
            min_price = float(request.query_params.get('min', 0))
            max_price = float(request.query_params.get('max', float('inf')))
            
            if min_price < 0 or max_price < 0:
                raise ValueError("Los precios no pueden ser negativos")
            
            events = catalog_service.search_by_price_range(min_price, max_price)
            serializer = EventCatalogSerializer(events, many=True)
            return Response({
                'min_price': min_price,
                'max_price': max_price,
                'count': len(events),
                'results': serializer.data
            })
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def sort_by_date(self, request: Request) -> Response:
        """
        GET /api/catalog/sort/by-date/?algorithm=merge
        Ordena eventos por fecha.
        
        Query params:
        - algorithm: merge o quick (por defecto: merge)
        - limit: número máximo de eventos
        """
        algorithm = request.query_params.get('algorithm', 'merge')
        limit = request.query_params.get('limit', type=int)

        if algorithm not in ['merge', 'quick']:
            return Response(
                {'error': 'Algoritmo debe ser "merge" o "quick"'},
                status=status.HTTP_400_BAD_REQUEST
            )

        events = catalog_service.sort_by_date(algorithm=algorithm)
        
        if limit:
            events = events[:limit]

        serializer = EventCatalogSerializer(events, many=True)
        return Response({
            'algorithm': algorithm,
            'count': len(events),
            'results': serializer.data
        })

    @action(detail=False, methods=['get'])
    def sort_by_price(self, request: Request) -> Response:
        """
        GET /api/catalog/sort/by-price/?algorithm=merge
        Ordena eventos por precio mínimo.
        """
        algorithm = request.query_params.get('algorithm', 'merge')
        limit = request.query_params.get('limit', type=int)

        if algorithm not in ['merge', 'quick']:
            return Response(
                {'error': 'Algoritmo debe ser "merge" o "quick"'},
                status=status.HTTP_400_BAD_REQUEST
            )

        events = catalog_service.sort_by_price(algorithm=algorithm)
        
        if limit:
            events = events[:limit]

        serializer = EventCatalogSerializer(events, many=True)
        return Response({
            'algorithm': algorithm,
            'count': len(events),
            'results': serializer.data
        })

    @action(detail=False, methods=['get'])
    def sort_by_popularity(self, request: Request) -> Response:
        """
        GET /api/catalog/sort/by-popularity/?algorithm=merge
        Ordena eventos por popularidad (más vendidos primero).
        """
        algorithm = request.query_params.get('algorithm', 'merge')
        limit = request.query_params.get('limit', type=int)

        if algorithm not in ['merge', 'quick']:
            return Response(
                {'error': 'Algoritmo debe ser "merge" o "quick"'},
                status=status.HTTP_400_BAD_REQUEST
            )

        events = catalog_service.sort_by_popularity(algorithm=algorithm)
        
        if limit:
            events = events[:limit]

        serializer = EventCatalogSerializer(events, many=True)
        return Response({
            'algorithm': algorithm,
            'count': len(events),
            'results': serializer.data
        })

    @action(detail=False, methods=['get'])
    def trending(self, request: Request) -> Response:
        """
        GET /api/catalog/trending/?limit=10
        Obtiene eventos en tendencia (más vendidos).
        """
        limit = request.query_params.get('limit', 10, type=int)
        events = catalog_service.get_trending_events(limit=limit)
        serializer = EventCatalogSerializer(events, many=True)
        return Response({
            'limit': limit,
            'count': len(events),
            'results': serializer.data
        })

    @action(detail=False, methods=['get'])
    def featured(self, request: Request) -> Response:
        """
        GET /api/catalog/featured/?limit=5
        Obtiene eventos destacados (próximos y disponibles).
        """
        limit = request.query_params.get('limit', 5, type=int)
        events = catalog_service.get_featured_events(limit=limit)
        serializer = EventCatalogSerializer(events, many=True)
        return Response({
            'limit': limit,
            'count': len(events),
            'results': serializer.data
        })

    @action(detail=False, methods=['get'])
    def statistics(self, request: Request) -> Response:
        """
        GET /api/catalog/statistics/
        Obtiene estadísticas generales del catálogo.
        """
        stats = catalog_service.get_statistics()
        return Response(stats)
