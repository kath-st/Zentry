from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from core.services.cart_service import CartService
from core.datastructures.stack import StackUnderflow
from core.domain.models import StockError, LimitExceeded


# Instancia global del servicio del carrito
cart_service = CartService()


def _cart_to_dict(cart):
    """Convierte un objeto Cart a diccionario para serialización."""
    return {
        'user_id': cart.user_id,
        'items': [
            {
                'event_id': item.event_id,
                'zone_id': item.zone_id,
                'qty': item.qty,
                'unit_price': item.unit_price,
                'total_price': item.qty * item.unit_price,
                'reservation_id': item.reservation_id
            }
            for item in cart.items
        ],
        'total_qty': cart.total_qty(),
        'total_amount': cart.total_amount()
    }


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    """GET /api/cart/ - Obtiene el carrito del usuario actual."""
    try:
        cart = cart_service.get_cart(request.user)
        return Response({
            'success': True,
            'cart': _cart_to_dict(cart),
            'can_undo': cart_service.can_undo(request.user),
            'undo_count': cart_service.get_undo_count(request.user)
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_item(request):
    """POST /api/cart/add/ - Añade un item al carrito."""
    try:
        data = request.data
        event_id = data.get('event_id')
        zone_code = data.get('zone_code')
        qty = data.get('qty', 1)

        if not event_id or not zone_code:
            return Response({
                'success': False,
                'error': 'event_id y zone_code son requeridos'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(qty, int) or qty <= 0:
            return Response({
                'success': False,
                'error': 'qty debe ser un entero positivo'
            }, status=status.HTTP_400_BAD_REQUEST)

        cart = cart_service.add_item(request.user, event_id, zone_code, qty)
        
        return Response({
            'success': True,
            'message': f'Se añadieron {qty} entradas al carrito',
            'cart': _cart_to_dict(cart),
            'can_undo': cart_service.can_undo(request.user)
        })

    except StockError as e:
        return Response({
            'success': False,
            'error': f'Error de stock: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except LimitExceeded as e:
        return Response({
            'success': False,
            'error': f'Límite excedido: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except ValueError as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Error interno: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_qty(request):
    """POST /api/cart/update/ - Actualiza la cantidad de un item."""
    try:
        data = request.data
        event_id = data.get('event_id')
        zone_code = data.get('zone_code')
        new_qty = data.get('qty')

        if not event_id or not zone_code or new_qty is None:
            return Response({
                'success': False,
                'error': 'event_id, zone_code y qty son requeridos'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(new_qty, int) or new_qty < 0:
            return Response({
                'success': False,
                'error': 'qty debe ser un entero no negativo'
            }, status=status.HTTP_400_BAD_REQUEST)

        cart = cart_service.update_qty(request.user, event_id, zone_code, new_qty)
        
        action = 'eliminó' if new_qty == 0 else 'actualizó'
        return Response({
            'success': True,
            'message': f'Se {action} el item del carrito',
            'cart': _cart_to_dict(cart),
            'can_undo': cart_service.can_undo(request.user)
        })

    except StockError as e:
        return Response({
            'success': False,
            'error': f'Error de stock: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except LimitExceeded as e:
        return Response({
            'success': False,
            'error': f'Límite excedido: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except ValueError as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Error interno: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_item(request):
    """POST /api/cart/remove/ - Elimina un item del carrito."""
    try:
        data = request.data
        event_id = data.get('event_id')
        zone_code = data.get('zone_code')

        if not event_id or not zone_code:
            return Response({
                'success': False,
                'error': 'event_id y zone_code son requeridos'
            }, status=status.HTTP_400_BAD_REQUEST)

        cart = cart_service.remove_item(request.user, event_id, zone_code)
        
        return Response({
            'success': True,
            'message': 'Item eliminado del carrito',
            'cart': _cart_to_dict(cart),
            'can_undo': cart_service.can_undo(request.user)
        })

    except ValueError as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Error interno: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    """POST /api/cart/clear/ - Vacía completamente el carrito."""
    try:
        cart_service.clear_cart(request.user)
        
        return Response({
            'success': True,
            'message': 'Carrito vaciado completamente',
            'cart': _cart_to_dict(cart_service.get_cart(request.user)),
            'can_undo': cart_service.can_undo(request.user)
        })

    except Exception as e:
        return Response({
            'success': False,
            'error': f'Error interno: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def undo(request):
    """POST /api/cart/undo/ - Deshace la última operación del carrito."""
    try:
        cart = cart_service.undo(request.user)
        
        return Response({
            'success': True,
            'message': 'Operación deshecha exitosamente',
            'cart': _cart_to_dict(cart),
            'can_undo': cart_service.can_undo(request.user),
            'undo_count': cart_service.get_undo_count(request.user)
        })

    except StackUnderflow:
        return Response({
            'success': False,
            'error': 'No hay operaciones para deshacer'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Error interno: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)