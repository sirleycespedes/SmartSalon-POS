import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Clientes from './pages/Clientes';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/*"
            element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Dashboard />} />
            <Route path="clientes" element={<Clientes />} />
            <Route path="empleados" element={<div className="p-6">Empleados - En desarrollo</div>} />
            <Route path="servicios" element={<div className="p-6">Servicios - En desarrollo</div>} />
            <Route path="productos" element={<div className="p-6">Productos - En desarrollo</div>} />
            <Route path="citas" element={<div className="p-6">Citas - En desarrollo</div>} />
            <Route path="ventas" element={<div className="p-6">Ventas - En desarrollo</div>} />
            <Route path="reportes" element={<div className="p-6">Reportes - En desarrollo</div>} />
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;

