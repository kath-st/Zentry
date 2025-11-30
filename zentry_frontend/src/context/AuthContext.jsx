import { createContext, useState, useContext, useEffect } from 'react';
import api from '../api/axios';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    // Al cargar la app, revisamos si hay un token guardado en el navegador
    useEffect(() => {
        const checkAuth = () => {
            const token = localStorage.getItem('token');
            const role = localStorage.getItem('role'); // Guardaremos el rol también
            
            if (token) {
                // Restauramos la sesión
                setUser({ token, role }); 
            }
            setLoading(false);
        };
        checkAuth();
    }, []);

    const login = async (email, password) => {
        try {
            const res = await api.post('auth/login/', { email, password });
            
            // Guardamos datos críticos en el navegador
            localStorage.setItem('token', res.data.token);
            localStorage.setItem('role', res.data.role); // Asumiendo que el backend devuelve 'role'
            
            setUser({ 
                token: res.data.token, 
                role: res.data.role, 
                id: res.data.user_id 
            });
            return { success: true };
        } catch (error) {
            console.error(error);
            return { 
                success: false, 
                error: error.response?.data?.error || "Error de conexión" 
            };
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('role');
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, loading }}>
            {!loading && children}
        </AuthContext.Provider>
    );
};