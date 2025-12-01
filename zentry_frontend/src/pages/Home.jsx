import { useEffect, useState } from 'react';
import api from '../api/axios';
import Navbar from '../components/Navbar';
import EventCard from '../components/EventCard';
import { Loader2 } from 'lucide-react';

export default function Home() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sortOrder, setSortOrder] = useState('asc'); // Estado para el orden

  useEffect(() => {
    const fetchEvents = async () => {
      setLoading(true); // Reiniciar loading al cambiar filtro
      try {
        // Enviamos el parámetro 'order' a la API
        const res = await api.get(`events/?order=${sortOrder}`);
        setEvents(res.data);
      } catch (err) {
        console.error(err);
        setError("No se pudo conectar con el servidor.");
      } finally {
        setLoading(false);
      }
    };
    fetchEvents();
  }, [sortOrder]); // Se ejecuta cuando cambia sortOrder

  return (
    <div className="min-h-screen bg-zentry-dark pb-20">
      <Navbar />

      {/* HERO */}
      <div className="relative border-b border-white/5 py-20 px-4 mb-12 overflow-hidden">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full bg-gradient-to-b from-zentry-primary/10 to-transparent pointer-events-none"></div>
        <div className="max-w-7xl mx-auto text-center relative z-10">
          <h1 className="text-5xl md:text-7xl font-extrabold text-white mb-6 tracking-tight">
            Vive la música <span className="text-transparent bg-clip-text bg-gradient-to-r from-zentry-primary to-zentry-secondary">en vivo</span>
          </h1>
          <p className="text-xl text-zentry-muted max-w-2xl mx-auto">
            Descubre los mejores conciertos. Reserva tus entradas sin filas virtuales eternas gracias a nuestra tecnología de Colas FIFO.
          </p>
        </div>
      </div>

      {/* GRID */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row justify-between items-center mb-8 gap-4">
          <h2 className="text-2xl font-bold text-white">Eventos Disponibles</h2>

          {/* SELECTOR DE ORDEN */}
          <div className="flex items-center gap-3 bg-white/5 px-4 py-2 rounded-lg border border-white/10">
            <span className="text-sm text-zentry-muted">Ordenar por fecha:</span>
            <select
              value={sortOrder}
              onChange={(e) => setSortOrder(e.target.value)}
              className="bg-transparent text-white text-sm font-medium focus:outline-none cursor-pointer"
            >
              <option value="asc" className="bg-zentry-dark text-white">Ascendente (Más próximos)</option>
              <option value="desc" className="bg-zentry-dark text-white">Descendente (Más lejanos)</option>
            </select>
          </div>
        </div>

        {loading && (
          <div className="flex justify-center py-20">
            <Loader2 className="h-10 w-10 text-zentry-primary animate-spin" />
          </div>
        )}

        {error && (
          <div className="text-center py-10 text-zentry-error bg-zentry-error/5 rounded-xl border border-zentry-error/10">
            {error}
          </div>
        )}

        {!loading && !error && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {events.map((event) => (
              <EventCard key={event.id} event={event} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}