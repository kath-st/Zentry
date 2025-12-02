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
            // 1. ITERAR: Tu backend protege asiento por asiento (Atomicidad)
            // Por eso, en lugar de enviar una lista gigante, enviamos uno por uno
            // a tu endpoint de bloqueo seguro.
            for (const item of items) {
                await api.post('reservations/bloquear/', { seat_id: item.id });
            }

            // 2. ACTUALIZAR ESTADO LOCAL (Solo si el backend no dio error)
            setCartItems(prev => [...prev, ...items]);

            // 3. TIEMPO DE EXPIRACIÓN
            // Como tu backend maneja 10 minutos fijos (según tu services.py),
            // configuramos el timer visual aquí.
            const expiration = new Date(new Date().getTime() + 10 * 60000);
            setExpirationTime(expiration);

            return { success: true, message: "Asientos bloqueados exitosamente" };

        } catch (error) {
            console.error("Error en bloqueo:", error);
            // Si falla (ej. alguien te ganó el asiento), mostramos el error de tu backend
            const errorMsg = error.response?.data?.error || "Error al reservar asiento";
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