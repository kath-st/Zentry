import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api/axios';
import Navbar from '../components/Navbar';
import { Loader2, Armchair, AlertCircle } from 'lucide-react'; // Importamos todos los iconos necesarios
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';

export default function EventDetails() {
  const { id } = useParams();
  const { user } = useAuth();
  const { addToCart } = useCart();
  const navigate = useNavigate();

  const [matrix, setMatrix] = useState([]);
  const [selectedSeats, setSelectedSeats] = useState([]); // IDs de los asientos seleccionados
  const [loading, setLoading] = useState(true);

  // --- LÓGICA DE PERMISOS ---
  const isAdmin = user?.role === 'ADMIN';
  const isEmployee = user?.role === 'EMPLEADO';
  
  // Regla: Solo puede comprar si NO es admin Y NO es empleado
  const canBuy = !isAdmin && !isEmployee; 

  // 1. Cargar la Matriz desde Django
  useEffect(() => {
    const fetchMap = async () => {
      try {
        const res = await api.get(`events/${id}/seats/`);
        // Aseguramos que recibimos la matriz correctamente
        setMatrix(res.data.mapa_matriz || []);
      } catch (error) {
        console.error("Error cargando mapa:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchMap();
  }, [id]);

  // 2. Manejar Click en Asiento
  const handleSeatClick = (seat) => {
    // Si no existe el asiento o ya está vendido, no hacemos nada
    if (!seat || seat.status === 'SOLD') return;

    const isSelected = selectedSeats.includes(seat.id);
    if (isSelected) {
      // Si ya estaba, lo quitamos
      setSelectedSeats(selectedSeats.filter(sId => sId !== seat.id));
    } else {
      // Si no estaba, lo agregamos
      setSelectedSeats([...selectedSeats, seat.id]);
    }
  };

  // 3. Agregar al Carrito (Lógica Corregida con Precios Reales)
  const handleAddToCart = async () => {
    if (!user) return navigate('/login');

    // Buscamos la información completa de los asientos seleccionados
    const selectedObjects = [];
    
    // Recorremos la matriz para encontrar los objetos completos de los IDs seleccionados
    matrix.forEach(row => {
        row.forEach(seat => {
            if (seat && selectedSeats.includes(seat.id)) {
                selectedObjects.push({
                    ...seat,
                    eventId: id,
                    // CORRECCIÓN: Usamos el precio y nombre real que viene del backend
                    price: seat.price, 
                    eventName: seat.event_title || "Concierto Seleccionado"
                });
            }
        });
    });

    // Guardamos en el contexto global (ahora sincronizado con backend)
    const result = await addToCart(selectedObjects);
    
    if (result.success) {
        // Redirigimos al carrito
        navigate('/cart');
    } else {
        alert(result.error);
    }
  };

  if (loading) return (
    <div className="min-h-screen bg-zentry-dark flex items-center justify-center text-white">
        <Loader2 className="animate-spin h-10 w-10 text-zentry-primary"/>
    </div>
  );

  return (
    <div className="min-h-screen bg-zentry-dark text-white pb-20">
      <Navbar />

      <div className="max-w-5xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-2">Selecciona tus asientos</h1>
        <p className="text-zentry-muted mb-8">Haz clic en los asientos disponibles para reservarlos.</p>

        {/* LEYENDA */}
        <div className="flex gap-6 mb-8 justify-center flex-wrap bg-white/5 p-4 rounded-xl border border-white/5">
            <div className="flex items-center gap-2"><div className="w-5 h-5 bg-white/10 rounded border border-white/5"></div> <span className="text-xs text-gray-400">General</span></div>
            <div className="flex items-center gap-2"><div className="w-5 h-5 bg-yellow-500/20 border border-yellow-500/50 rounded"></div> <span className="text-xs text-yellow-500 font-bold">VIP</span></div>
            <div className="flex items-center gap-2"><div className="w-5 h-5 bg-zentry-primary rounded shadow-lg shadow-zentry-primary/40"></div> <span className="text-xs text-white">Tu Selección</span></div>
            <div className="flex items-center gap-2"><div className="w-5 h-5 bg-white/5 opacity-30 cursor-not-allowed rounded text-white/20 flex items-center justify-center text-[8px]">X</div> <span className="text-xs text-gray-500">Ocupado</span></div>
        </div>

        {/* ESCENARIO */}
        <div className="w-full h-16 bg-gradient-to-b from-zentry-primary/20 to-transparent mb-12 rounded-t-[50%] flex items-end justify-center border-t border-zentry-primary/50 shadow-[0_-10px_40px_rgba(99,102,241,0.2)]">
            <span className="text-zentry-primary font-bold tracking-[0.5em] text-sm mb-4">ESCENARIO</span>
        </div>

        {/* MATRIZ (Renderizado) */}
        <div className="flex flex-col gap-2 items-center overflow-x-auto pb-12 custom-scrollbar">
          {matrix.map((fila, i) => (
            <div key={i} className="flex gap-2">
              {fila.map((seat, j) => {
                 const isSold = seat?.status === 'SOLD';
                 const isSelected = seat && selectedSeats.includes(seat.id);
                 
                 // Detectar si es VIP por el nombre de la zona (que viene del backend)
                 const isVip = seat?.zone_name?.toUpperCase().includes('VIP');
                 
                 return (
                    <button
                        key={j}
                        disabled={!seat || isSold}
                        onClick={() => seat && handleSeatClick(seat)}
                        className={`
                            w-9 h-9 sm:w-10 sm:h-10 rounded-lg text-xs font-medium transition-all duration-200 flex items-center justify-center relative
                            ${!seat ? 'invisible' : ''}
                            
                            /* OCUPADO */
                            ${isSold ? 'bg-white/5 text-transparent cursor-not-allowed border border-white/5' : ''}
                            
                            /* SELECCIONADO */
                            ${isSelected ? 'bg-zentry-primary text-white shadow-[0_0_15px_rgba(99,102,241,0.6)] scale-110 z-10 border-transparent' : ''}
                            
                            /* VIP DISPONIBLE */
                            ${!isSold && !isSelected && isVip ? 'bg-yellow-500/10 text-yellow-500 border border-yellow-500/30 hover:bg-yellow-500/30 hover:shadow-[0_0_10px_rgba(234,179,8,0.2)]' : ''}
                            
                            /* GENERAL DISPONIBLE */
                            ${!isSold && !isSelected && !isVip ? 'bg-white/10 hover:bg-white/20 text-white/50 hover:text-white border border-white/5' : ''}
                        `}
                        title={seat ? `${seat.zone_name} - $${seat.price}` : ''}
                    >
                        {seat ? seat.number : ''}
                        {isSold && <div className="absolute inset-0 flex items-center justify-center text-white/20 font-sans">X</div>}
                    </button>
                 );
              })}
            </div>
          ))}
        </div>

        {/* BARRA INFERIOR (Solo si puede comprar) */}
        {selectedSeats.length > 0 && canBuy && (
            <div className="fixed bottom-0 left-0 w-full bg-zentry-card border-t border-white/10 p-4 animate-slide-up z-40 backdrop-blur-lg bg-opacity-90">
                <div className="max-w-4xl mx-auto flex justify-between items-center">
                    <div>
                        <p className="text-zentry-muted text-sm">Seleccionados</p>
                        <p className="text-3xl font-bold text-white tracking-tight">
                            {selectedSeats.length} <span className="text-sm font-normal text-zentry-muted">entradas</span>
                        </p>
                    </div>
                    <button 
                        onClick={handleAddToCart}
                        className="bg-zentry-primary hover:bg-zentry-secondary px-8 py-3 rounded-xl font-bold text-white transition-all shadow-lg shadow-zentry-primary/30 flex items-center gap-3 transform hover:scale-105 active:scale-95"
                    >
                        <Armchair className="w-5 h-5" />
                        Agregar al Carrito
                    </button>
                </div>
            </div>
        )}

        {/* AVISO FLOTANTE (ADMIN/EMPLEADO - Sin botón de compra) */}
        {selectedSeats.length > 0 && !canBuy && (
            <div className="fixed bottom-10 left-1/2 -translate-x-1/2 bg-black/80 px-6 py-3 rounded-full border border-white/20 text-sm text-gray-300 backdrop-blur-md shadow-xl flex items-center gap-2 z-50 animate-bounce-in">
                <AlertCircle className="w-4 h-4 text-zentry-warning" />
                <span>
                    {isAdmin ? "Vista Admin" : "Vista Staff"}: Modo solo lectura. No puedes comprar.
                </span>
            </div>
        )}

      </div>
    </div>
  );
}