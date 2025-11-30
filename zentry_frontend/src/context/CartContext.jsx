import { createContext, useState, useContext, useEffect } from 'react';

const CartContext = createContext();

export const useCart = () => useContext(CartContext);

export const CartProvider = ({ children }) => {
    // Inicializamos el carrito leyendo del LocalStorage (para no perder datos al recargar)
    const [cartItems, setCartItems] = useState(() => {
        const saved = localStorage.getItem('zentry_cart');
        return saved ? JSON.parse(saved) : [];
    });

    // Cada vez que cambia el carrito, lo guardamos en el navegador
    useEffect(() => {
        localStorage.setItem('zentry_cart', JSON.stringify(cartItems));
    }, [cartItems]);

    // Función para agregar ítems
    const addToCart = (items) => {
        // items es un array de objetos asiento
        setCartItems(prev => [...prev, ...items]);
    };

    // Función para quitar un ítem (Lógica de Pila/Stack o eliminación directa)
    const removeFromCart = (seatId) => {
        setCartItems(prev => prev.filter(item => item.id !== seatId));
    };

    // Limpiar carrito al comprar
    const clearCart = () => {
        setCartItems([]);
    };

    // Calcular Total
    const cartTotal = cartItems.reduce((total, item) => total + parseFloat(item.price), 0);

    return (
        <CartContext.Provider value={{ cartItems, addToCart, removeFromCart, clearCart, cartTotal }}>
            {children}
        </CartContext.Provider>
    );
};