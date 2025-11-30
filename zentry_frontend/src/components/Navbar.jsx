import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';
import { Ticket, ShoppingCart, LogOut, User, LayoutDashboard, Scan } from 'lucide-react'; // <--- AGREGAR SCAN

export default function Navbar() {
  const { user, logout } = useAuth();
  const { cartItems } = useCart(); 
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isAdmin = user?.role === 'ADMIN';
  const isEmployee = user?.role === 'EMPLEADO'; // <--- NUEVA LÓGICA

  return (
    <nav className="bg-zentry-card border-b border-white/10 sticky top-0 z-50 backdrop-blur-md bg-opacity-90">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          <Link to="/" className="flex items-center gap-2 group">
            <Ticket className="h-8 w-8 text-zentry-primary group-hover:rotate-12 transition-transform" />
            <span className="text-2xl font-bold tracking-wider bg-gradient-to-r from-zentry-primary to-zentry-secondary bg-clip-text text-transparent">
              ZENTRY
            </span>
            {/* ETIQUETAS DE ROL */}
            {isAdmin && <span className="text-xs bg-red-500 text-white px-2 py-0.5 rounded ml-2">ADMIN</span>}
            {isEmployee && <span className="text-xs bg-blue-500 text-white px-2 py-0.5 rounded ml-2">STAFF</span>}
          </Link>

          <div className="flex items-center gap-4 sm:gap-6">
            
            {/* --- SOLO ADMIN --- */}
            {user && isAdmin && (
                 <Link to="/admin" className="flex items-center gap-2 text-gray-300 hover:text-white transition-colors">
                    <LayoutDashboard className="h-5 w-5" />
                    <span className="font-medium hidden sm:block">Panel Gestión</span>
                 </Link>
            )}

            {/* --- SOLO EMPLEADO (NUEVO) --- */}
            {user && isEmployee && (
                 <Link to="/validator" className="flex items-center gap-2 text-zentry-primary hover:text-white transition-colors border border-zentry-primary/30 px-3 py-1.5 rounded-lg bg-zentry-primary/10">
                    <Scan className="h-5 w-5" />
                    <span className="font-bold">Escanear</span>
                 </Link>
            )}

            {/* --- SOLO CLIENTE (Si NO es admin NI empleado) --- */}
            {user && !isAdmin && !isEmployee ? (
              <>
                <Link to="/" className="text-gray-300 hover:text-white transition-colors text-sm font-medium hidden sm:block">Eventos</Link>
                <Link to="/tickets" className="flex items-center gap-2 text-gray-300 hover:text-white transition-colors"><Ticket className="h-5 w-5" /></Link>
                <Link to="/cart" className="relative p-2 text-gray-400 hover:text-white transition-colors">
                  <ShoppingCart className="h-6 w-6" />
                  {cartItems.length > 0 && <span className="absolute top-0 right-0 bg-zentry-primary text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full animate-pulse-once">{cartItems.length}</span>}
                </Link>
                <div className="h-6 w-px bg-white/10 mx-1"></div>
                <Link to="/profile" className="flex items-center gap-2 px-2 py-1.5 rounded-lg hover:bg-white/5 transition-colors"><User className="h-5 w-5" /></Link>
              </>
            ) : null}
            
            {/* BOTÓN SALIR / ENTRAR */}
            {user ? (
                <button onClick={handleLogout} className="flex items-center gap-2 text-sm text-zentry-muted hover:text-white transition-colors ml-2" title="Cerrar Sesión">
                  <LogOut className="h-5 w-5" />
                </button>
            ) : (
              <Link to="/login" className="bg-zentry-primary hover:bg-zentry-secondary text-white px-5 py-2 rounded-full text-sm font-medium transition-all shadow-lg">Iniciar Sesión</Link>
            )}

          </div>
        </div>
      </div>
    </nav>
  );
}