import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../../api/axios';
import Navbar from '../../components/Navbar';
import { Plus, Edit, Trash2, Calendar, MapPin, Loader2 } from 'lucide-react';

export default function AdminDashboard() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchEvents = async () => {
    try {
      const res = await api.get('events/');
      setEvents(res.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvents();
  }, []);

  const handleDelete = async (id) => {
    if (!window.confirm("¿Estás seguro? Esto borrará el evento y TODOS sus tickets vendidos.")) return;

    try {
      // Llamamos al endpoint de DELETE que creamos en el backend
      await api.delete(`events/${id}/manage/`);
      setEvents(events.filter(e => e.id !== id)); // Actualizamos la lista visualmente
      alert("Evento eliminado correctamente.");
    } catch (error) {
      alert("Error al eliminar: " + (error.response?.data?.error || "Error desconocido"));
    }
  };

  return (
    <div className="min-h-screen bg-zentry-dark text-white pb-20">
      <Navbar />

      <div className="max-w-6xl mx-auto px-4 py-10">
        
        {/* HEADER */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white">Panel de Administración</h1>
            <p className="text-zentry-muted">Gestiona tus conciertos y aforos</p>
          </div>
          <Link 
            to="/admin/create" 
            className="bg-zentry-primary hover:bg-zentry-secondary px-6 py-3 rounded-xl font-bold flex items-center gap-2 transition-all shadow-lg shadow-zentry-primary/20"
          >
            <Plus size={20} /> Nuevo Evento
          </Link>
        </div>

        {loading ? (
          <div className="flex justify-center py-20"><Loader2 className="animate-spin text-zentry-primary h-10 w-10"/></div>
        ) : (
          <div className="bg-zentry-card border border-white/10 rounded-2xl overflow-hidden shadow-xl">
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-white/5 border-b border-white/10 text-xs uppercase text-zentry-muted">
                    <th className="p-4">Evento</th>
                    <th className="p-4">Fecha</th>
                    <th className="p-4">Lugar</th>
                    <th className="p-4 text-center">Acciones</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  {events.map((event) => (
                    <tr key={event.id} className="hover:bg-white/5 transition-colors">
                      <td className="p-4 flex items-center gap-4">
                        <img src={event.image_url} alt="" className="w-12 h-12 rounded-lg object-cover bg-white/10" />
                        <span className="font-bold">{event.title}</span>
                      </td>
                      <td className="p-4 text-sm text-gray-300">
                        <div className="flex items-center gap-2"><Calendar size={14} /> {new Date(event.date).toLocaleDateString()}</div>
                      </td>
                      <td className="p-4 text-sm text-gray-300">
                        <div className="flex items-center gap-2"><MapPin size={14} /> {event.venue}</div>
                      </td>
                      <td className="p-4">
                        <div className="flex justify-center gap-2">
                          <Link 
                            to={`/admin/edit/${event.id}`}
                            className="p-2 bg-blue-500/10 text-blue-400 hover:bg-blue-500 hover:text-white rounded-lg transition-all"
                            title="Editar"
                          >
                            <Edit size={18} />
                          </Link>
                          <button 
                            onClick={() => handleDelete(event.id)}
                            className="p-2 bg-red-500/10 text-red-400 hover:bg-red-500 hover:text-white rounded-lg transition-all"
                            title="Eliminar (Cuidado)"
                          >
                            <Trash2 size={18} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {events.length === 0 && <p className="text-center py-10 text-gray-500">No hay eventos registrados.</p>}
          </div>
        )}
      </div>
    </div>
  );
}