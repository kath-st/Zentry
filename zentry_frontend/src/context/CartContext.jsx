import { createContext, useState, useContext, useEffect } from 'react';
import api from '../api/axios';

const CartContext = createContext();

export const useCart = () => useContext(CartContext);

export const CartProvider = ({ children }) => {
    // Carrito en memoria local
    const [cartItems, setCartItems] = useState([]);
    const [expirationTime, setExpirationTime] = useState(null);

    // Función para agregar ítems y reservarlos en el backend
    const addToCart = async (items) => {
        try {
            // Extraer IDs de los asientos
            const seatIds = items.map(item => item.id);
            
            // Llamar al backend para reservar
            const res = await api.post('orders/cart/add/', { seat_ids: seatIds });
            
            // Agregar al carrito local con los datos completos
            setCartItems(prev => [...prev, ...items]);
            
            // Guardar tiempo de expiración
            if (res.data.seats && res.data.seats[0]?.expires_at) {
                setExpirationTime(new Date(res.data.seats[0].expires_at));
            }
            
            return { success: true, message: res.data.message };
        } catch (error) {
            const errorMsg = error.response?.data?.error || "Error al reservar asientos";
            return { success: false, error: errorMsg };
        }
    };

    // Función para deshacer (Stack LIFO) usando el backend
    const undoLastItem = async () => {
        try {
            const res = await api.post('orders/cart/undo/');
            
            // Remover el último item del carrito local
            if (cartItems.length > 0) {
                const seatIdToRemove = res.data.seat_id;
                setCartItems(prev => prev.filter(item => item.id !== seatIdToRemove));
            }
            
            return { success: true, message: res.data.message };
        } catch (error) {
            return { success: false, error: error.response?.data?.error || "Error al deshacer" };
        }
    };

    // Función para liberar un asiento específico
    const releaseReservation = async (seatId) => {
        try {
            await api.post('orders/cart/release/', { seat_id: seatId });
            setCartItems(prev => prev.filter(item => item.id !== seatId));
            return { success: true };
        } catch (error) {
            return { success: false, error: error.response?.data?.error };
        }
    };

    // Limpiar carrito al comprar
    const clearCart = () => {
        setCartItems([]);
        setExpirationTime(null);
    };

    // Calcular Total
    const cartTotal = cartItems.reduce((total, item) => total + parseFloat(item.price), 0);

    // Timer para verificar expiración
    useEffect(() => {
        if (!expirationTime) return;

        const interval = setInterval(() => {
            if (new Date() >= expirationTime) {
                alert("⏰ Tu reserva ha expirado. Los asientos han sido liberados.");
                clearCart();
            }
        }, 1000);

        return () => clearInterval(interval);
    }, [expirationTime]);

    return (
        <CartContext.Provider value={{ 
            cartItems, 
            addToCart, 
            undoLastItem,
            releaseReservation,
            clearCart, 
            cartTotal,
            expirationTime
        }}>
            {children}
        </CartContext.Provider>
    );
};