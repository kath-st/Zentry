import { useState } from 'react';
import api from '../api/axios';
import { useNavigate, Link } from 'react-router-dom';
import { Ticket, Loader2, CreditCard, User, Mail, Lock, FileBadge } from 'lucide-react';

export default function Register() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    dni: '',
    password: '',
    card_number: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Enviamos los datos a Django
      await api.post('auth/register/', formData);
      
      // Si funciona, redirigimos al login
      alert("¡Cuenta creada exitosamente! Por favor inicia sesión.");
      navigate('/login');
    } catch (err) {
      // Aquí atrapamos el error del ÁRBOL BINARIO (BST) si el DNI está duplicado
      setError(err.response?.data?.error || "Error al registrarse. Revisa tus datos.");
      console.error(err.response?.data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-zentry-dark px-4 py-12 relative overflow-hidden">
      {/* Decoración de fondo */}
      <div className="absolute top-[-20%] right-[-10%] w-[500px] h-[500px] bg-zentry-primary/10 rounded-full blur-3xl pointer-events-none"></div>

      <div className="max-w-xl w-full bg-zentry-card border border-white/10 rounded-2xl p-8 shadow-2xl relative z-10">
        
        <div className="text-center mb-8">
          <Ticket className="h-10 w-10 text-zentry-primary mx-auto mb-4" />
          <h2 className="text-3xl font-bold text-white">Crea tu cuenta</h2>
          <p className="text-zentry-muted">Únete a Zentry para reservar tus entradas</p>
        </div>

        {error && (
          <div className="bg-zentry-error/10 border border-zentry-error/20 text-zentry-error text-sm p-4 rounded-lg mb-6 text-center">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          
          {/* Nombre y Apellido */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-xs text-gray-400 uppercase font-bold ml-1">Nombre</label>
              <div className="relative">
                <User className="absolute left-3 top-3 h-5 w-5 text-gray-500" />
                <input
                  name="first_name"
                  type="text"
                  required
                  className="w-full bg-zentry-dark border border-white/10 rounded-lg pl-10 pr-4 py-3 text-white focus:border-zentry-primary focus:outline-none"
                  onChange={handleChange}
                />
              </div>
            </div>
            <div>
              <label className="text-xs text-gray-400 uppercase font-bold ml-1">Apellido</label>
              <input
                name="last_name"
                type="text"
                required
                className="w-full bg-zentry-dark border border-white/10 rounded-lg px-4 py-3 text-white focus:border-zentry-primary focus:outline-none"
                onChange={handleChange}
              />
            </div>
          </div>

          {/* DNI (Validado por BST) */}
          <div>
            <label className="text-xs text-gray-400 uppercase font-bold ml-1">DNI (Único)</label>
            <div className="relative">
              <FileBadge className="absolute left-3 top-3 h-5 w-5 text-gray-500" />
              <input
                name="dni"
                type="text"
                required
                maxLength="10"
                className="w-full bg-zentry-dark border border-white/10 rounded-lg pl-10 pr-4 py-3 text-white focus:border-zentry-primary focus:outline-none"
                placeholder="Documento de Identidad"
                onChange={handleChange}
              />
            </div>
          </div>

          {/* Email */}
          <div>
            <label className="text-xs text-gray-400 uppercase font-bold ml-1">Correo Electrónico</label>
            <div className="relative">
              <Mail className="absolute left-3 top-3 h-5 w-5 text-gray-500" />
              <input
                name="email"
                type="email"
                required
                className="w-full bg-zentry-dark border border-white/10 rounded-lg pl-10 pr-4 py-3 text-white focus:border-zentry-primary focus:outline-none"
                placeholder="nombre@ejemplo.com"
                onChange={handleChange}
              />
            </div>
          </div>

          {/* Password */}
          <div>
            <label className="text-xs text-gray-400 uppercase font-bold ml-1">Contraseña</label>
            <div className="relative">
              <Lock className="absolute left-3 top-3 h-5 w-5 text-gray-500" />
              <input
                name="password"
                type="password"
                required
                className="w-full bg-zentry-dark border border-white/10 rounded-lg pl-10 pr-4 py-3 text-white focus:border-zentry-primary focus:outline-none"
                placeholder="••••••••"
                onChange={handleChange}
              />
            </div>
          </div>

          {/* Tarjeta (Simulación) */}
          <div>
            <label className="text-xs text-gray-400 uppercase font-bold ml-1 flex justify-between">
              <span>Tarjeta de Crédito</span>
              <span className="text-zentry-warning text-[10px] font-normal tracking-wide">SOLO SIMULACIÓN</span>
            </label>
            <div className="relative">
              <CreditCard className="absolute left-3 top-3 h-5 w-5 text-gray-500" />
              <input
                name="card_number"
                type="text"
                maxLength="16"
                className="w-full bg-zentry-dark border border-white/10 rounded-lg pl-10 pr-4 py-3 text-white focus:border-zentry-primary focus:outline-none font-mono"
                placeholder="4000 1234 5678 9010"
                onChange={handleChange}
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full mt-6 bg-zentry-primary hover:bg-zentry-secondary text-white font-bold py-3 rounded-lg transition-all flex justify-center items-center gap-2"
          >
            {loading ? <Loader2 className="animate-spin" /> : "Crear Cuenta"}
          </button>

        </form>

        <div className="mt-6 text-center text-sm text-zentry-muted">
          ¿Ya tienes cuenta?{' '}
          <Link to="/login" className="text-zentry-primary hover:text-white transition-colors font-medium">
            Inicia Sesión
          </Link>
        </div>
      </div>
    </div>
  );
}