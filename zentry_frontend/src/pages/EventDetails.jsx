import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api/axios';
import Navbar from '../components/Navbar';
import { Loader2, Calendar, MapPin, Clock, Users, ArrowLeft, ShoppingCart, AlertCircle } from 'lucide-react';
import { Button } from "../components/ui/button";
import { Badge } from "../components/ui/badge";
import { motion } from "framer-motion";
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';

export default function EventDetails() {
  const { id } = useParams();
  const { user } = useAuth();
  const { addToCart } = useCart();
  const navigate = useNavigate();

  const [event, setEvent] = useState(null);
  const [matrix, setMatrix] = useState([]);
  const [selectedSeats, setSelectedSeats] = useState([]);
  const [loading, setLoading] = useState(true);

  // --- LÓGICA DE PERMISOS ---
  const isAdmin = user?.role === 'ADMIN';
  const isEmployee = user?.role === 'EMPLEADO';
  const canBuy = !isAdmin && !isEmployee;

  // 1. Cargar Datos (Evento y Matriz)
  useEffect(() => {
    const fetchData = async () => {
      try {
        const eventRes = await api.get(`events/${id}/`);
        setEvent(eventRes.data);

        const mapRes = await api.get(`reservations/mapa/${id}/`);
        setMatrix(mapRes.data.mapa || []);
      } catch (error) {
        console.error("Error cargando datos:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [id]);

  // 2. Manejar Click en Asiento
  const handleSeatClick = (seat) => {
    if (!seat || seat.status === 'SOLD' || (!canBuy && seat.status !== 'AVAILABLE')) return;

    // Verificar si ya está seleccionado
    const isSelected = selectedSeats.some(s => s.id === seat.id);

    if (isSelected) {
      setSelectedSeats(selectedSeats.filter(s => s.id !== seat.id));
    } else {
      // Agregar objeto completo del asiento
      setSelectedSeats([...selectedSeats, seat]);
    }
  };

  // 3. Agregar al Carrito
  const handleAddToCart = async () => {
    if (!user) return navigate('/login');

    // Mapear al formato que espera tu CartContext
    const itemsToAdd = selectedSeats.map(seat => ({
      id: seat.id,
      seat_label: seat.nombre, // FIXED: Map 'nombre' to 'seat_label' for Cart.jsx
      price: seat.price,
      zone: seat.zone_name,
      eventName: event?.title || "Evento Zentry"
    }));

    const result = await addToCart(itemsToAdd);

    if (result.success) {
      navigate('/cart');
    } else {
      alert(result.error);
    }
  };

  // Cálculos para la UI
  const calculateTotal = () => {
    return selectedSeats.reduce((sum, s) => sum + parseFloat(s.price), 0);
  };

  // Colores por zona
  const getZoneColor = (zoneName) => {
    const name = zoneName?.toUpperCase() || "";
    if (name.includes("VIP")) return "border-yellow-500 bg-yellow-500/20 text-yellow-500";
    if (name.includes("PREFERENCIAL")) return "border-purple-500 bg-purple-500/20 text-purple-500";
    return "border-blue-500 bg-blue-500/20 text-blue-500"; // General
  };

  if (loading) return (
    <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center text-white">
      <Loader2 className="animate-spin h-10 w-10 text-[#6366f1]" />
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0a0a0f] via-[#13131a] to-[#1a1a24] text-white font-sans">
      <Navbar />

      <div className="max-w-7xl mx-auto px-6 py-8">

        {/* Botón Volver */}
        <button
          onClick={() => navigate("/")}
          className="flex items-center text-gray-400 hover:text-white mb-8 transition-colors group"
        >
          <ArrowLeft className="mr-2 w-5 h-5 group-hover:-translate-x-1 transition-transform" />
          Volver a Eventos
        </button>

        <div className="grid lg:grid-cols-[35%_65%] gap-8">

          {/* COLUMNA IZQUIERDA: INFO EVENTO */}
          <div className="space-y-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="rounded-2xl overflow-hidden shadow-2xl border border-white/10"
            >
              <img
                src={event?.image_url || "https://images.unsplash.com/photo-1492684223066-81342ee5ff30"}
                alt={event?.title}
                className="w-full h-[350px] object-cover hover:scale-105 transition-transform duration-500"
              />
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="bg-[#1a1a24]/80 backdrop-blur-md border border-white/10 rounded-2xl p-6 shadow-xl"
            >
              <h1 className="text-3xl font-bold text-white mb-2 leading-tight">
                {event?.title}
              </h1>
              <Badge className="bg-[#6366f1]/20 text-[#6366f1] mb-4 border-none px-3 py-1">
                {event?.category || "Concierto"}
              </Badge>

              <div className="space-y-4 text-sm text-gray-300">
                <div className="flex items-center gap-3 p-3 rounded-lg bg-white/5">
                  <Calendar className="w-5 h-5 text-[#6366f1]" />
                  <span>{new Date(event?.date).toLocaleDateString('es-ES', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</span>
                </div>
                <div className="flex items-center gap-3 p-3 rounded-lg bg-white/5">
                  <Clock className="w-5 h-5 text-[#6366f1]" />
                  <span>{new Date(event?.date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} hrs</span>
                </div>
                <div className="flex items-center gap-3 p-3 rounded-lg bg-white/5">
                  <MapPin className="w-5 h-5 text-[#6366f1]" />
                  <span>{event?.venue}</span>
                </div>
              </div>
            </motion.div>
          </div>

          {/* COLUMNA DERECHA: SELECCIÓN ASIENTOS */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-[#1a1a24]/50 border border-white/10 rounded-2xl p-8 flex flex-col items-center relative overflow-hidden"
          >
            {/* LEYENDA */}
            <div className="flex flex-wrap justify-center gap-4 mb-8 text-sm w-full">
              <div className="flex items-center gap-2"><div className="w-4 h-4 rounded bg-white/10 border border-white/20"></div> <span className="text-gray-400">Libre</span></div>
              <div className="flex items-center gap-2"><div className="w-4 h-4 rounded bg-[#6366f1] shadow-[0_0_10px_#6366f1]"></div> <span className="text-gray-200">Tu Selección</span></div>
              <div className="flex items-center gap-2"><div className="w-4 h-4 rounded bg-white/5 opacity-30 flex items-center justify-center text-[8px]">X</div> <span className="text-gray-500">Ocupado</span></div>
              <div className="flex items-center gap-2"><div className="w-4 h-4 rounded bg-yellow-500/20 border border-yellow-500"></div> <span className="text-yellow-500">VIP</span></div>
            </div>

            {/* ESCENARIO */}
            <div className="w-3/4 h-12 bg-gradient-to-b from-[#6366f1]/30 to-transparent mb-12 rounded-t-[100%] flex items-end justify-center border-t border-[#6366f1]/50 shadow-[0_-10px_30px_rgba(99,102,241,0.2)]">
              <span className="text-[#6366f1] font-bold tracking-[0.5em] text-xs mb-2">ESCENARIO</span>
            </div>

            {/* MATRIZ DE ASIENTOS */}
            <div className="w-full overflow-x-auto pb-12 flex justify-center">
              <div className="flex flex-col gap-3 min-w-max">
                {matrix.map((row, i) => (
                  <div key={i} className="flex justify-center gap-2 md:gap-3">
                    {/* Número de Fila */}
                    <span className="text-gray-600 text-xs w-6 flex items-center justify-center">{row[0]?.nombre?.split('-')[0]}</span>

                    {row.map((seat, j) => {
                      if (!seat) return <div key={j} className="w-8 h-8 md:w-10 md:h-10" />; // Espacio vacío

                      const isSold = seat.status === 'SOLD';
                      const isReserved = seat.status === 'RESERVED'; // Si quieres mostrar reservados por otros
                      const isSelected = selectedSeats.some(s => s.id === seat.id);
                      const isVip = seat.zone_name?.toUpperCase().includes('VIP');

                      // Si está ocupado/reservado y no soy yo, deshabilitar
                      const isDisabled = isSold || (isReserved && !isSelected);

                      return (
                        <motion.button
                          key={seat.id}
                          whileHover={!isDisabled && canBuy ? { scale: 1.1 } : {}}
                          whileTap={!isDisabled && canBuy ? { scale: 0.9 } : {}}
                          disabled={isDisabled || !canBuy}
                          onClick={() => handleSeatClick(seat)}
                          className={`
                                  w-8 h-8 md:w-10 md:h-10 rounded-lg text-xs font-bold transition-all duration-300 flex items-center justify-center relative
                                  
                                  ${isDisabled
                              ? 'bg-white/5 border border-white/5 text-transparent cursor-not-allowed opacity-40'
                              : ''}
                                  
                                  ${isSelected
                              ? 'bg-[#6366f1] text-white shadow-[0_0_15px_#6366f1] z-10 border-none ring-2 ring-white/20'
                              : ''}
                                  
                                  ${!isDisabled && !isSelected && isVip
                              ? 'bg-yellow-500/10 text-yellow-500 border border-yellow-500/30 hover:bg-yellow-500/20'
                              : ''}
                                  
                                  ${!isDisabled && !isSelected && !isVip
                              ? 'bg-white/10 text-gray-400 border border-white/10 hover:bg-white/20 hover:text-white'
                              : ''}
                              `}
                          title={`${seat.zone_name} - $${seat.price}`}
                        >
                          {isDisabled ? 'X' : seat.number}
                        </motion.button>
                      );
                    })}
                  </div>
                ))}
              </div>
            </div>

            {/* MENSAJE FLOTANTE SI NO PUEDE COMPRAR */}
            {!canBuy && (
              <div className="absolute bottom-4 bg-red-500/20 border border-red-500/50 text-red-200 px-4 py-2 rounded-full text-sm flex items-center gap-2">
                <AlertCircle className="w-4 h-4" />
                Vista de {user?.role}. Compra deshabilitada.
              </div>
            )}
          </motion.div>
        </div>

        {/* BARRA FLOTANTE DE TOTAL Y COMPRA */}
        {selectedSeats.length > 0 && canBuy && (
          <motion.div
            initial={{ y: 100 }}
            animate={{ y: 0 }}
            className="fixed bottom-6 left-1/2 -translate-x-1/2 w-[90%] max-w-4xl bg-[#13131a]/90 backdrop-blur-xl border border-[#6366f1]/30 p-4 rounded-2xl shadow-[0_0_50px_rgba(0,0,0,0.5)] z-50 flex items-center justify-between"
          >
            <div className="flex items-center gap-6">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-full bg-[#6366f1]/20 flex items-center justify-center text-[#6366f1]">
                  <Users className="w-6 h-6" />
                </div>
                <div>
                  <p className="text-gray-400 text-sm">Seleccionados</p>
                  <p className="text-white font-bold text-xl">{selectedSeats.length} <span className="text-sm font-normal text-gray-500">entradas</span></p>
                </div>
              </div>
              <div className="h-10 w-[1px] bg-white/10 hidden sm:block"></div>
              <div className="hidden sm:block">
                <p className="text-gray-400 text-sm">Total a pagar</p>
                <p className="text-white font-bold text-2xl text-[#6366f1]">${calculateTotal().toFixed(2)}</p>
              </div>
            </div>

            <Button
              onClick={handleAddToCart}
              className="bg-gradient-to-r from-[#6366f1] to-[#8b5cf6] hover:opacity-90 text-white font-bold py-6 px-8 rounded-xl text-lg shadow-lg shadow-[#6366f1]/20 transition-all hover:scale-105 active:scale-95"
            >
              <ShoppingCart className="mr-2 w-5 h-5" />
              Reservar Ahora
            </Button>
          </motion.div>
        )}

      </div>
    </div>
  );
}