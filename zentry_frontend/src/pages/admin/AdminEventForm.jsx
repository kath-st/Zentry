import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../../api/axios';
import Navbar from '../../components/Navbar';
import { Save, Loader2, ArrowLeft } from 'lucide-react';

export default function AdminEventForm() {
  const { id } = useParams(); // Si hay ID, estamos editando
  const navigate = useNavigate();
  const isEditing = Boolean(id);

  const [formData, setFormData] = useState({
    title: '',
    date: '', // Formato ISO para input datetime-local
    venue: '',
    category: '',
    image_url: '',
    price_min: '',
    vip_price: '',     // Extra para crear zonas
    general_price: ''  // Extra para crear zonas
  });
  
  const [loading, setLoading] = useState(false);

  // Cargar datos si estamos editando
  useEffect(() => {
    if (isEditing) {
      const fetchEvent = async () => {
        try {
          // Usamos el endpoint público para llenar el formulario
          // Nota: El endpoint admin detail que creamos era '/manage/', usaremos ese para update
          const res = await api.get(`events/`); 
          const event = res.data.find(e => e.id === parseInt(id));
          if (event) {
            // Ajustar fecha para que el input type="datetime-local" la entienda
            const dateISO = new Date(event.date).toISOString().slice(0, 16);
            setFormData({
              ...event,
              date: dateISO,
              price_min: event.price_min
            });
          }
        } catch (error) {
          console.error(error);
        }
      };
      fetchEvent();
    }
  }, [id, isEditing]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (isEditing) {
        // --- MODO EDICIÓN (PUT) ---
        await api.put(`events/${id}/manage/`, {
            title: formData.title,
            date: formData.date,
            venue: formData.venue,
            image_url: formData.image_url,
            category: formData.category
        });
        alert("Evento actualizado correctamente.");
      } else {
        // --- MODO CREACIÓN (POST) ---
        // Preparamos el array de zonas que pide el backend para generar la matriz
        const payload = {
            title: formData.title,
            date: formData.date,
            venue: formData.venue,
            category: formData.category,
            image_url: formData.image_url,
            price_min: formData.general_price, // Precio base visual
            zones_input: [
                { name: "VIP", price: parseFloat(formData.vip_price) },
                { name: "General", price: parseFloat(formData.general_price) }
            ]
        };

        await api.post('events/create/', payload);
        alert("Evento creado y matriz de asientos generada (200 cupos).");
      }
      navigate('/admin'); // Volver al dashboard
    } catch (error) {
      alert("Error: " + (error.response?.data?.message || "Revisa los datos."));
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => setFormData({...formData, [e.target.name]: e.target.value});

  return (
    <div className="min-h-screen bg-zentry-dark text-white pb-20">
      <Navbar />
      <div className="max-w-3xl mx-auto px-4 py-10">
        
        <button onClick={() => navigate('/admin')} className="flex items-center gap-2 text-zentry-muted hover:text-white mb-6">
            <ArrowLeft size={16}/> Volver al Panel
        </button>

        <h1 className="text-3xl font-bold mb-8">{isEditing ? 'Editar Evento' : 'Nuevo Evento'}</h1>

        <form onSubmit={handleSubmit} className="bg-zentry-card p-8 rounded-2xl border border-white/10 shadow-2xl space-y-6">
            
            {/* Título */}
            <div>
                <label className="block text-xs uppercase text-zentry-muted font-bold mb-2">Nombre del Evento</label>
                <input type="text" name="title" required value={formData.title} onChange={handleChange}
                    className="w-full bg-black/20 border border-white/10 rounded-lg px-4 py-3 focus:border-zentry-primary focus:outline-none" placeholder="Ej: Concierto de Rock" />
            </div>

            {/* Fecha y Lugar */}
            <div className="grid grid-cols-2 gap-6">
                <div>
                    <label className="block text-xs uppercase text-zentry-muted font-bold mb-2">Fecha y Hora</label>
                    <input type="datetime-local" name="date" required value={formData.date} onChange={handleChange}
                        className="w-full bg-black/20 border border-white/10 rounded-lg px-4 py-3 focus:border-zentry-primary focus:outline-none text-gray-300" />
                </div>
                <div>
                    <label className="block text-xs uppercase text-zentry-muted font-bold mb-2">Lugar (Venue)</label>
                    <input type="text" name="venue" required value={formData.venue} onChange={handleChange}
                        className="w-full bg-black/20 border border-white/10 rounded-lg px-4 py-3 focus:border-zentry-primary focus:outline-none" placeholder="Ej: Estadio Nacional" />
                </div>
            </div>

            {/* Imagen y Categoría */}
            <div className="grid grid-cols-2 gap-6">
                <div>
                    <label className="block text-xs uppercase text-zentry-muted font-bold mb-2">URL de Imagen</label>
                    <input type="url" name="image_url" required value={formData.image_url} onChange={handleChange}
                        className="w-full bg-black/20 border border-white/10 rounded-lg px-4 py-3 focus:border-zentry-primary focus:outline-none" placeholder="https://..." />
                </div>
                <div>
                    <label className="block text-xs uppercase text-zentry-muted font-bold mb-2">Categoría</label>
                    <input type="text" name="category" required value={formData.category} onChange={handleChange}
                        className="w-full bg-black/20 border border-white/10 rounded-lg px-4 py-3 focus:border-zentry-primary focus:outline-none" placeholder="Ej: Pop, Rock, Jazz" />
                </div>
            </div>

            {/* PRECIOS (SOLO VISIBLE AL CREAR) */}
            {!isEditing && (
                <div className="bg-zentry-primary/10 p-6 rounded-xl border border-zentry-primary/30">
                    <h3 className="font-bold text-zentry-primary mb-4 flex items-center gap-2">Configuración de Asientos (Automático)</h3>
                    <div className="grid grid-cols-2 gap-6">
                        <div>
                            <label className="block text-xs uppercase text-zentry-muted font-bold mb-2">Precio General ($)</label>
                            <input type="number" name="general_price" required min="1" step="0.01" value={formData.general_price} onChange={handleChange}
                                className="w-full bg-black/20 border border-white/10 rounded-lg px-4 py-3 focus:border-zentry-primary focus:outline-none" placeholder="45.00" />
                        </div>
                        <div>
                            <label className="block text-xs uppercase text-zentry-muted font-bold mb-2">Precio VIP ($)</label>
                            <input type="number" name="vip_price" required min="1" step="0.01" value={formData.vip_price} onChange={handleChange}
                                className="w-full bg-black/20 border border-white/10 rounded-lg px-4 py-3 focus:border-zentry-primary focus:outline-none" placeholder="120.00" />
                        </div>
                    </div>
                    <p className="text-xs text-zentry-muted mt-3">* Esto generará automáticamente 100 asientos General y 100 VIP.</p>
                </div>
            )}

            <button type="submit" disabled={loading} className="w-full bg-zentry-primary hover:bg-zentry-secondary py-4 rounded-xl font-bold text-lg transition-all flex justify-center items-center gap-2">
                {loading ? <Loader2 className="animate-spin" /> : <><Save /> {isEditing ? 'Guardar Cambios' : 'Crear Evento'}</>}
            </button>

        </form>
      </div>
    </div>
  );
}