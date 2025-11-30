import { Calendar, MapPin } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function EventCard({ event }) {
  // Formatear fecha bonita
  const dateObj = new Date(event.date);
  const dateStr = dateObj.toLocaleDateString('es-ES', { day: 'numeric', month: 'short' });
  const timeStr = dateObj.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });

  return (
    <div className="bg-zentry-card rounded-2xl overflow-hidden border border-white/5 hover:border-zentry-primary/50 transition-all duration-300 group hover:-translate-y-1 shadow-xl">
      {/* IMAGEN */}
      <div className="relative h-48 overflow-hidden">
        <img 
          src={event.image_url} 
          alt={event.title} 
          className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
        />
        <div className="absolute top-3 right-3 bg-zentry-dark/80 backdrop-blur-sm text-white text-xs font-bold px-3 py-1 rounded-full uppercase border border-white/10">
          {event.category}
        </div>
      </div>

      {/* DETALLES */}
      <div className="p-5">
        <h3 className="text-lg font-bold text-white mb-3 line-clamp-1 group-hover:text-zentry-primary transition-colors">
          {event.title}
        </h3>
        
        <div className="space-y-2 mb-6">
          <div className="flex items-center gap-2 text-zentry-muted text-sm">
            <Calendar className="h-4 w-4 text-zentry-secondary" />
            <span>{dateStr} • {timeStr}</span>
          </div>
          <div className="flex items-center gap-2 text-zentry-muted text-sm">
            <MapPin className="h-4 w-4 text-zentry-secondary" />
            <span className="line-clamp-1">{event.venue}</span>
          </div>
        </div>

        {/* PRECIO */}
        <div className="flex items-center justify-between border-t border-white/10 pt-4">
          <div>
            <p className="text-xs text-zentry-muted">Tickets desde</p>
            <p className="text-xl font-bold text-white">${event.price_min}</p>
          </div>
          <Link 
            to={`/event/${event.id}`}
            className="bg-white/5 hover:bg-white/10 text-white px-4 py-2 rounded-lg text-sm font-medium transition-all"
          >
            Ver Mapa
          </Link>
        </div>
      </div>
    </div>
  );
}