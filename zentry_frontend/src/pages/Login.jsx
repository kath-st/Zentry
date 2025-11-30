import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';
import { Ticket, Loader2 } from 'lucide-react';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    // Llamamos a la función del Contexto
    const result = await login(email, password);

    if (result.success) {
      navigate('/'); // Redirigir al inicio
    } else {
      setError(result.error); // Mostrar error del backend (ej: "Email no existe en Hash Table")
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-zentry-dark px-4 relative overflow-hidden">
      
      {/* Círculos de fondo decorativos */}
      <div className="absolute top-[-10%] left-[-10%] w-96 h-96 bg-zentry-primary/20 rounded-full blur-3xl pointer-events-none"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-96 h-96 bg-zentry-secondary/20 rounded-full blur-3xl pointer-events-none"></div>

      <div className="max-w-md w-full bg-zentry-card border border-white/10 rounded-2xl p-8 shadow-2xl relative z-10 backdrop-blur-xl bg-opacity-80">
        
        {/* LOGO */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-white/5 mb-4">
            <Ticket className="h-8 w-8 text-zentry-primary" />
          </div>
          <h2 className="text-3xl font-bold text-white mb-2">Bienvenido a Zentry</h2>
          <p className="text-zentry-muted">Ingresa para gestionar tus entradas</p>
        </div>

        {/* ERROR MESSAGE */}
        {error && (
          <div className="bg-zentry-error/10 border border-zentry-error/20 text-zentry-error text-sm p-3 rounded-lg mb-6 text-center">
            {error}
          </div>
        )}

        {/* FORMULARIO */}
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Correo Electrónico</label>
            <input
              type="email"
              required
              className="w-full bg-zentry-dark border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-zentry-primary focus:ring-1 focus:ring-zentry-primary transition-all"
              placeholder="ejemplo@correo.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Contraseña</label>
            <input
              type="password"
              required
              className="w-full bg-zentry-dark border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-zentry-primary focus:ring-1 focus:ring-zentry-primary transition-all"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full bg-gradient-to-r from-zentry-primary to-zentry-secondary hover:opacity-90 text-white font-bold py-3 rounded-lg transition-all transform hover:scale-[1.02] active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center gap-2"
          >
            {isSubmitting ? (
              <>
                <Loader2 className="h-5 w-5 animate-spin" />
                Ingresando...
              </>
            ) : (
              "Iniciar Sesión"
            )}
          </button>
        </form>

        <div className="mt-6 text-center text-sm text-zentry-muted">
          ¿No tienes cuenta?{' '}
          <Link to="/register" className="text-zentry-primary hover:text-white transition-colors font-medium">
            Regístrate aquí
          </Link>
        </div>
      </div>
    </div>
  );
}