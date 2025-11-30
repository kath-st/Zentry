import { useState } from 'react';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import api from '../api/axios';
import Navbar from '../components/Navbar';
import { useNavigate } from 'react-router-dom';
import { Trash2, CreditCard, Loader2, ArrowRight } from 'lucide-react';

export default function Cart() {
  const { cartItems, removeFromCart, clearCart, cartTotal } = useCart();
  const { user } = useAuth();
  const navigate = useNavigate();

  const [cvv, setCvv] = useState('');
  const [processing, setProcessing] = useState(false);

  // Lógica de Compra Final
  const handleCheckout = async (e) => {
    e.preventDefault();
    if (!user) return navigate('/login');
    
    // VALIDACIÓN LOCAL ANTES DE ENVIAR
    if (cvv !== "123") {
        alert("Error de pago: El código de seguridad (CVV) es incorrecto.");
        return;
    }

    setProcessing(true);
    try {
      // 1. Unirse a la Cola (Queue - Requisito Backend)
      await api.post('orders/queue/join/');

      // 2. Extraer solo los IDs para el backend
      const seatIds = cartItems.map(item => item.id);

      // 3. Procesar Pago
      const res = await api.post('orders/checkout/', {
        seat_ids: seatIds,
        cvv: cvv // Enviamos el 123
      });

      alert(`¡Compra Exitosa!\nTickets: ${res.data.tickets.join(", ")}`);
      clearCart(); // Limpiar carrito
      navigate('/tickets'); // Ir a "Mis Entradas"
      
    } catch (error) {
      alert("Error: " + (error.response?.data?.error || "Falló la compra"));
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-zentry-dark pb-20 text-white">
      <Navbar />

      <div className="max-w-4xl mx-auto px-4 py-10">
        <h1 className="text-3xl font-bold mb-8">Mi Carrito de Compras</h1>

        {cartItems.length === 0 ? (
           <div className="text-center py-20 bg-zentry-card rounded-2xl border border-white/5">
             <p className="text-gray-400 mb-4">Tu carrito está vacío.</p>
             <button onClick={() => navigate('/')} className="text-zentry-primary hover:underline">Ir al Catálogo</button>
           </div>
        ) : (
           <div className="grid md:grid-cols-3 gap-8">
             
             {/* LISTA DE ÍTEMS */}
             <div className="md:col-span-2 space-y-4">
               {cartItems.map((item, index) => (
                 <div key={index} className="bg-zentry-card p-4 rounded-xl border border-white/10 flex justify-between items-center">
                    <div>
                        <h3 className="font-bold">{item.eventName || "Entrada de Concierto"}</h3>
                        <p className="text-sm text-zentry-muted">Asiento: {item.number}</p>
                    </div>
                    <div className="flex items-center gap-4">
                        <span className="font-bold">${item.price}</span>
                        <button 
                            onClick={() => removeFromCart(item.id)}
                            className="text-red-400 hover:text-red-300 p-2"
                            title="Eliminar (Stack Pop)"
                        >
                            <Trash2 size={20} />
                        </button>
                    </div>
                 </div>
               ))}
             </div>

             {/* RESUMEN DE PAGO */}
             <div className="bg-zentry-card p-6 rounded-2xl border border-white/10 h-fit">
                <h3 className="text-xl font-bold mb-4">Resumen</h3>
                
                <div className="space-y-2 mb-4 text-sm">
                    <div className="flex justify-between">
                        <span className="text-zentry-muted">Subtotal</span>
                        <span>${cartTotal.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-zentry-muted">Cargo por servicio (10%)</span>
                        <span>${(cartTotal * 0.10).toFixed(2)}</span>
                    </div>
                    <div className="border-t border-white/10 my-2 pt-2 flex justify-between text-lg font-bold text-zentry-primary">
                        <span>Total</span>
                        <span>${(cartTotal * 1.10).toFixed(2)}</span>
                    </div>
                </div>

                {/* FORMULARIO DE PAGO */}
                <form onSubmit={handleCheckout}>
                    <label className="block text-xs uppercase text-zentry-muted font-bold mb-2">Código de Seguridad (CVV)</label>
                    <div className="relative mb-6">
                        <CreditCard className="absolute left-3 top-3 h-5 w-5 text-gray-500" />
                        <input 
                            type="text" 
                            maxLength="3"
                            placeholder="123"
                            value={cvv}
                            onChange={(e) => setCvv(e.target.value)}
                            className="w-full bg-black/20 border border-white/10 rounded-lg pl-10 pr-4 py-3 focus:border-zentry-primary focus:outline-none tracking-widest"
                            required
                        />
                    </div>

                    <button 
                        type="submit"
                        disabled={processing}
                        className="w-full bg-gradient-to-r from-zentry-primary to-zentry-secondary py-3 rounded-xl font-bold hover:opacity-90 transition-all flex justify-center items-center gap-2"
                    >
                        {processing ? <Loader2 className="animate-spin" /> : <>Pagar Ahora <ArrowRight size={18} /></>}
                    </button>
                    <p className="text-xs text-center text-zentry-muted mt-3">
                        Código requerido para simulación: <strong>123</strong>
                    </p>
                </form>
             </div>

           </div>
        )}
      </div>
    </div>
  );
}