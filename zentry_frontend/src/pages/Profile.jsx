import { useState, useEffect } from 'react';
import api from '../api/axios';
import Navbar from '../components/Navbar';
import { User, Mail, CreditCard, FileBadge, Save, X, Edit2, Loader2 } from 'lucide-react';

export default function Profile() {
  const [profile, setProfile] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  // 1. Cargar datos del Backend
  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const res = await api.get('auth/profile/');
      setProfile(res.data);
      setFormData(res.data); // Preparamos el formulario con los datos actuales
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  // 2. Manejar cambios en inputs
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // 3. Guardar cambios (PATCH)
  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      // Enviamos solo los campos editables
      const res = await api.patch('auth/profile/', {
        first_name: formData.first_name,
        last_name: formData.last_name,
        email: formData.email,
        card_number: formData.card_number
        // No enviamos DNI porque es read-only en el backend (BST)
      });
      
      setProfile(res.data.data); // Actualizamos la vista con la respuesta
      setIsEditing(false);
      alert("Perfil actualizado correctamente.");
    } catch (error) {
      alert("Error: " + (error.response?.data?.error || "No se pudo actualizar"));
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="min-h-screen bg-zentry-dark flex items-center justify-center text-white"><Loader2 className="animate-spin" /></div>;

  return (
    <div className="min-h-screen bg-zentry-dark pb-20 text-white">
      <Navbar />

      <div className="max-w-2xl mx-auto px-4 py-10">
        
        {/* CABECERA */}
        <div className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold flex items-center gap-3">
                <div className="bg-zentry-primary/20 p-3 rounded-full">
                    <User className="text-zentry-primary h-8 w-8" />
                </div>
                Mi Perfil
            </h1>
            
            {!isEditing && (
                <button 
                    onClick={() => setIsEditing(true)}
                    className="flex items-center gap-2 text-zentry-primary hover:text-white transition-colors bg-zentry-card px-4 py-2 rounded-lg border border-white/10"
                >
                    <Edit2 className="h-4 w-4" /> Editar
                </button>
            )}
        </div>

        {/* TARJETA DE DATOS */}
        <div className="bg-zentry-card border border-white/10 rounded-2xl p-8 shadow-2xl relative overflow-hidden">
            {/* Fondo decorativo */}
            <div className="absolute top-0 right-0 w-64 h-64 bg-zentry-primary/5 rounded-full blur-3xl pointer-events-none -translate-y-1/2 translate-x-1/2"></div>

            <form onSubmit={handleSave} className="space-y-6 relative z-10">
                
                {/* NOMBRE Y APELLIDO */}
                <div className="grid grid-cols-2 gap-6">
                    <div>
                        <label className="text-xs text-zentry-muted uppercase font-bold mb-1 block">Nombre</label>
                        <input 
                            type="text" 
                            name="first_name"
                            disabled={!isEditing}
                            value={formData.first_name}
                            onChange={handleChange}
                            className="w-full bg-black/20 border border-white/10 rounded-lg px-4 py-3 text-white disabled:text-gray-400 disabled:border-transparent focus:border-zentry-primary focus:outline-none transition-all"
                        />
                    </div>
                    <div>
                        <label className="text-xs text-zentry-muted uppercase font-bold mb-1 block">Apellido</label>
                        <input 
                            type="text" 
                            name="last_name"
                            disabled={!isEditing}
                            value={formData.last_name}
                            onChange={handleChange}
                            className="w-full bg-black/20 border border-white/10 rounded-lg px-4 py-3 text-white disabled:text-gray-400 disabled:border-transparent focus:border-zentry-primary focus:outline-none transition-all"
                        />
                    </div>
                </div>

                {/* EMAIL */}
                <div>
                    <label className="text-xs text-zentry-muted uppercase font-bold mb-1 block">Correo Electrónico (Login)</label>
                    <div className="relative">
                        <Mail className="absolute left-3 top-3 h-5 w-5 text-gray-500" />
                        <input 
                            type="email" 
                            name="email"
                            disabled={!isEditing}
                            value={formData.email}
                            onChange={handleChange}
                            className="w-full bg-black/20 border border-white/10 rounded-lg pl-10 pr-4 py-3 text-white disabled:text-gray-400 disabled:border-transparent focus:border-zentry-primary focus:outline-none transition-all"
                        />
                    </div>
                </div>

                {/* DNI (READ ONLY) */}
                <div>
                    <label className="text-xs text-zentry-muted uppercase font-bold mb-1 flex justify-between">
                        <span>Documento de Identidad</span>
                        {isEditing && <span className="text-zentry-warning text-[10px]">NO EDITABLE</span>}
                    </label>
                    <div className="relative">
                        <FileBadge className="absolute left-3 top-3 h-5 w-5 text-gray-500" />
                        <input 
                            type="text" 
                            disabled={true} // Siempre deshabilitado
                            value={formData.dni}
                            className="w-full bg-white/5 border border-transparent rounded-lg pl-10 pr-4 py-3 text-gray-400 cursor-not-allowed"
                        />
                    </div>
                </div>

                {/* TARJETA */}
                <div>
                    <label className="text-xs text-zentry-muted uppercase font-bold mb-1 block">Tarjeta Vinculada</label>
                    <div className="relative">
                        <CreditCard className="absolute left-3 top-3 h-5 w-5 text-gray-500" />
                        <input 
                            type="text" 
                            name="card_number"
                            disabled={!isEditing}
                            value={formData.card_number}
                            onChange={handleChange}
                            className="w-full bg-black/20 border border-white/10 rounded-lg pl-10 pr-4 py-3 text-white font-mono disabled:text-gray-400 disabled:border-transparent focus:border-zentry-primary focus:outline-none transition-all"
                        />
                    </div>
                </div>

                {/* BOTONES DE ACCIÓN */}
                {isEditing && (
                    <div className="flex gap-4 pt-4 border-t border-white/10 animate-fade-in">
                        <button 
                            type="button"
                            onClick={() => {
                                setIsEditing(false);
                                setFormData(profile); // Revertir cambios
                            }}
                            className="flex-1 bg-white/5 hover:bg-white/10 text-white py-3 rounded-lg font-bold flex justify-center items-center gap-2 transition-all"
                        >
                            <X className="h-4 w-4" /> Cancelar
                        </button>
                        <button 
                            type="submit"
                            disabled={saving}
                            className="flex-1 bg-zentry-primary hover:bg-zentry-secondary text-white py-3 rounded-lg font-bold flex justify-center items-center gap-2 transition-all"
                        >
                            {saving ? <Loader2 className="animate-spin" /> : <><Save className="h-4 w-4" /> Guardar Cambios</>}
                        </button>
                    </div>
                )}

            </form>
        </div>

      </div>
    </div>
  );
}