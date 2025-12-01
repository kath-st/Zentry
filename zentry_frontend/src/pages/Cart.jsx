import { useState, useEffect } from 'react';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import api from '../api/axios';
import Navbar from '../components/Navbar';
import { useNavigate } from 'react-router-dom';
import { Trash2, CreditCard, Loader2, ArrowRight, Undo2, Clock } from 'lucide-react';

export default function Cart() {
  const { cartItems, undoLastItem, releaseReservation, clearCart, cartTotal, expirationTime } = useCart();
  const { user } = useAuth();
  const navigate = useNavigate();

  const [cvv, setCvv] = useState('');
  const [processing, setProcessing] = useState(false);
  const [timeRemaining, setTimeRemaining] = useState('');

  // Calcular tiempo restante
  useEffect(() => {
    if (!expirationTime) return;

    const interval = setInterval(() => {
      const now = new Date();
      const diff = expirationTime - now;

      if (diff <= 0) {
        setTimeRemaining('Expirado');
        clearInterval(interval);
      } else {
        const minutes = Math.floor(diff / 60000);
        const seconds = Math.floor((diff % 60000) / 1000);
        setTimeRemaining(`${minutes}:${seconds.toString().padStart(2, '0')}`);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [expirationTime]);

  // Función para deshacer última acción (Stack LIFO)
  const handleUndo = async () => {
    const result = await undoLastItem();
    if (result.success) {
      // Opcional: mostrar mensaje de éxito
    } else {
      alert(result.error);
    }
  };

  // Función para eliminar un item específico
  const handleRemoveItem = async (seatId) => {
    const result = await releaseReservation(seatId);
    if (!result.success) {
      alert(result.error);
    }
  };

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
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">Mi Carrito de Compras</h1>
          {/* TIMER DE EXPIRACIÓN */}
          {cartItems.length > 0 && expirationTime && (
            <div className="flex items-center gap-2 bg-orange-500/10 px-4 py-2 rounded-lg border border-orange-500/30">
              <Clock className="text-orange-500" size={20} />
              <span className="text-orange-500 font-mono font-bold">{timeRemaining}</span>
            </div>
          )}
        </div>

        {cartItems.length === 0 ? (
           <div className="text-center py-20 bg-zentry-card rounded-2xl border border-white/5">
             <p className="text-gray-400 mb-4">Tu carrito está vacío.</p>
             <button onClick={() => navigate('/')} className="text-zentry-primary hover:underline">Ir al Catálogo</button>
           </div>
        ) : (
           <div className="grid md:grid-cols-3 gap-8">
             
             {/* LISTA DE ÍTEMS */}
             <div className="md:col-span-2 space-y-4">
               {/* BOTÓN DESHACER (STACK LIFO) */}
               {cartItems.length > 0 && (
                 <button
                   onClick={handleUndo}
                   className="w-full bg-yellow-500/10 hover:bg-yellow-500/20 text-yellow-500 py-3 rounded-xl font-bold flex items-center justify-center gap-2 transition-all border border-yellow-500/30"
                 >
                   <Undo2 size={20} /> Deshacer Última Selección (Stack LIFO)
                 </button>
               )}

               {cartItems.map((item) => (
                 <div key={item.id} className="bg-zentry-card p-4 rounded-xl border border-white/10 flex justify-between items-center hover:border-zentry-primary/30 transition-all">
                    <div>
                        <h3 className="font-bold text-lg">{item.event_title}</h3>
                        <p className="text-zentry-muted text-sm">Asiento: {item.seat_label}</p>
                    </div>
                    <div className="flex items-center gap-4">
                        <span className="font-bold">${item.price}</span>
                        <button 
                            onClick={() => handleRemoveItem(item.id)}
                            className="text-red-400 hover:text-red-300 p-2"
                            title="Eliminar y liberar reserva"
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