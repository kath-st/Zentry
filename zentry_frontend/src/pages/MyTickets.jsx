import { useEffect, useState } from 'react';
import api from '../api/axios';
import Navbar from '../components/Navbar';
import { Loader2, Calendar, MapPin, Ticket as TicketIcon } from 'lucide-react';

export default function MyTickets() {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTickets = async () => {
      try {
        const res = await api.get('orders/my-tickets/');
        setTickets(res.data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };
    fetchTickets();
  }, []);

  return (
    <div className="min-h-screen bg-zentry-dark pb-20">
      <Navbar />

      <div className="max-w-4xl mx-auto px-4 py-10">
        <h1 className="text-3xl font-bold text-white mb-8 flex items-center gap-3">
          <TicketIcon className="text-zentry-primary" />
          Mis Entradas
        </h1>

        {loading && (
          <div className="flex justify-center py-20">
            <Loader2 className="h-10 w-10 text-zentry-primary animate-spin" />
          </div>
        )}

        {!loading && tickets.length === 0 && (
          <div className="text-center py-20 bg-zentry-card rounded-2xl border border-white/5">
            <p className="text-gray-400 mb-4">Aún no tienes entradas.</p>
            <a href="/" className="text-zentry-primary hover:underline">Explorar Eventos</a>
          </div>
        )}

        <div className="grid gap-6">
          {tickets.map((ticket) => (
            <div key={ticket.id} className="bg-zentry-card border border-white/10 rounded-2xl overflow-hidden flex flex-col md:flex-row hover:border-zentry-primary/30 transition-all">
              
              {/* IZQUIERDA: IMAGEN DEL EVENTO */}
              <div className="md:w-48 h-32 md:h-auto relative">
                <img 
                  src={ticket.event_image} 
                  alt={ticket.event_title} 
                  className="w-full h-full object-cover"
                />
                <div className="absolute inset-0 bg-gradient-to-r from-black/50 to-transparent md:hidden"></div>
              </div>

              {/* CENTRO: INFO */}
              <div className="p-6 flex-1">
                <h3 className="text-xl font-bold text-white mb-2">{ticket.event_title}</h3>
                
                <div className="space-y-1 text-sm text-zentry-muted">
                  <div className="flex items-center gap-2">
                    <Calendar className="h-4 w-4 text-zentry-secondary" />
                    <span>{new Date(ticket.event_date).toLocaleDateString()}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <MapPin className="h-4 w-4 text-zentry-secondary" />
                    <span>{ticket.venue}</span>
                  </div>
                </div>

                <div className="mt-4 inline-block bg-white/5 px-3 py-1 rounded-lg text-sm text-gray-300 border border-white/10">
                  Asiento: <span className="text-white font-bold">{ticket.seat_label}</span>
                </div>
              </div>

              {/* DERECHA: CÓDIGO QR SIMULADO */}
              <div className="bg-white/5 p-6 flex flex-col items-center justify-center border-t md:border-t-0 md:border-l border-white/10 border-dashed min-w-[200px]">
                <span className="text-xs text-zentry-muted uppercase tracking-widest mb-2">Código de Acceso</span>
                <div className="bg-white text-black font-mono text-xl font-bold px-4 py-2 rounded border-2 border-dashed border-gray-400">
                  {ticket.ticket_code}
                </div>
                <p className="text-[10px] text-gray-500 mt-2 text-center">Presenta este código en la entrada</p>
              </div>

            </div>
          ))}
        </div>
      </div>
    </div>
  );
}