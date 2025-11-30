import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { CartProvider } from './context/CartContext'; // <--- IMPORTAR
import AdminDashboard from './pages/admin/AdminDashboard'; // <---
import AdminEventForm from './pages/admin/AdminEventForm';
import Profile from './pages/Profile';

import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import EventDetails from './pages/EventDetails';
import MyTickets from './pages/MyTickets';
import Validator from './pages/Validator';
import Cart from './pages/Cart'; // <--- (Lo crearemos en el Paso 4)

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <CartProvider> {/* <--- ENVOLVER AQUÍ */}
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/event/:id" element={<EventDetails />} />
            <Route path="/tickets" element={<MyTickets />} />
            <Route path="/validator" element={<Validator />} />
            <Route path="/cart" element={<Cart />} /> {/* <--- NUEVA RUTA */}
            <Route path="/profile" element={<Profile />} />
            <Route path="/admin" element={<AdminDashboard />} />
            <Route path="/admin/create" element={<AdminEventForm />} />
            <Route path="/admin/edit/:id" element={<AdminEventForm />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </CartProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;