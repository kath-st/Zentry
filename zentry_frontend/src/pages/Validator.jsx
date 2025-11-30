import { useState, useEffect } from 'react';
import api from '../api/axios';
import Navbar from '../components/Navbar';
import { Scan, CheckCircle, AlertTriangle, XCircle, RefreshCw } from 'lucide-react';

export default function Validator() {
  const [code, setCode] = useState('');
  const [result, setResult] = useState(null); // null, 'success', 'warning', 'error'
  const [message, setMessage] = useState('');
  const [data, setData] = useState(null);
  const [stats, setStats] = useState({ valid: 0, duplicate: 0, invalid: 0 });

  // Cargar estadísticas al iniciar
  const fetchStats = async () => {
    try {
      const res = await api.get('access/stats/');
      setStats({
        valid: res.data.validos_hoy || 0,
        duplicate: res.data.duplicados_hoy || 0,
        invalid: res.data.invalidos_hoy || 0
      });
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  const handleScan = async (e) => {
    e.preventDefault();
    if (!code) return;

    try {
      // Petición al Backend (Validador Set O(1))
      const res = await api.post('access/validate/', { ticket_code: code });
      
      setResult('success'); // Verde
      setMessage(res.data.message);
      setData(res.data.data);
      setCode(''); // Limpiar input para el siguiente
      fetchStats(); // Actualizar contadores
      
    } catch (error) {
      // Manejar errores (404 Rojo o 409 Amarillo)
      const status = error.response?.status;
      const msg = error.response?.data?.message || "Error desconocido";
      const info = error.response?.data?.data;

      if (status === 409) {
        setResult('warning'); // Amarillo (Duplicado)
      } else {
        setResult('error'); // Rojo (Inválido)
      }
      setMessage(msg);
      setData(info);
      setCode('');
      fetchStats();
    }
  };

  return (
    <div className="min-h-screen bg-zentry-dark pb-20 text-white">
      <Navbar />

      <div className="max-w-2xl mx-auto px-4 py-10">
        
        {/* HEADER */}
        <div className="text-center mb-10">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-white/5 mb-4 border border-white/10">
            <Scan className="h-10 w-10 text-zentry-primary" />
          </div>
          <h1 className="text-3xl font-bold">Panel de Control de Acceso</h1>
          <p className="text-zentry-muted mt-2">Ingresa el código del ticket para validar (Hash Set)</p>
        </div>

        {/* INPUT DE ESCANEO */}
        <form onSubmit={handleScan} className="mb-12">
            <div className="flex gap-4">
                <input 
                    type="text" 
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    placeholder="Escribe el código (ej: ZEN-123)"
                    className="flex-1 bg-zentry-card border border-white/20 rounded-xl px-6 py-4 text-xl font-mono text-white focus:border-zentry-primary focus:outline-none uppercase"
                    autoFocus
                />
                <button 
                    type="submit"
                    className="bg-zentry-primary hover:bg-zentry-secondary px-8 py-4 rounded-xl font-bold transition-all"
                >
                    Validar
                </button>
            </div>
        </form>

        {/* RESULTADO (SEMÁFORO) */}
        {result && (
            <div className={`p-8 rounded-2xl border-2 mb-12 text-center animate-pulse-once ${
                result === 'success' ? 'bg-green-500/10 border-green-500 text-green-400' :
                result === 'warning' ? 'bg-yellow-500/10 border-yellow-500 text-yellow-400' :
                'bg-red-500/10 border-red-500 text-red-400'
            }`}>
                <div className="flex justify-center mb-4">
                    {result === 'success' && <CheckCircle className="h-16 w-16" />}
                    {result === 'warning' && <AlertTriangle className="h-16 w-16" />}
                    {result === 'error' && <XCircle className="h-16 w-16" />}
                </div>
                <h2 className="text-3xl font-bold mb-2 uppercase">{message}</h2>
                
                {data && (
                    <div className="mt-4 text-white/80 text-sm bg-black/20 p-4 rounded-lg inline-block text-left">
                        {data.usuario && <p>👤 <strong>Usuario:</strong> {data.usuario}</p>}
                        {data.evento && <p>🎵 <strong>Evento:</strong> {data.evento}</p>}
                        {data.asiento && <p>💺 <strong>Asiento:</strong> {data.asiento}</p>}
                        {data.hora_venta && <p>🕒 <strong>Vendido:</strong> {new Date(data.hora_venta).toLocaleString()}</p>}
                    </div>
                )}
            </div>
        )}

        {/* DASHBOARD DE ESTADÍSTICAS */}
        <div className="grid grid-cols-3 gap-4">
            <div className="bg-zentry-card p-6 rounded-xl border border-white/10 text-center">
                <p className="text-zentry-muted text-xs uppercase font-bold">Validados</p>
                <p className="text-4xl font-bold text-green-500 mt-2">{stats.valid}</p>
            </div>
            <div className="bg-zentry-card p-6 rounded-xl border border-white/10 text-center">
                <p className="text-zentry-muted text-xs uppercase font-bold">Duplicados</p>
                <p className="text-4xl font-bold text-yellow-500 mt-2">{stats.duplicate}</p>
            </div>
            <div className="bg-zentry-card p-6 rounded-xl border border-white/10 text-center">
                <p className="text-zentry-muted text-xs uppercase font-bold">Rechazados</p>
                <p className="text-4xl font-bold text-red-500 mt-2">{stats.invalid}</p>
            </div>
        </div>

      </div>
    </div>
  );
}