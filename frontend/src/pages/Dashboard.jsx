import React, { useState, useEffect } from 'react';
import { api } from '../lib/api'; // Corregido de apiClient a api
import {
  DollarSign,
  Users,
  Calendar,
  Package,
  TrendingUp,
  AlertTriangle
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      // Aquí deberías llamar a un endpoint real de dashboard en tu API NestJS
      // Por ahora, simularemos datos o usaremos un endpoint existente si aplica
      const data = { // Datos simulados para que no falle la interfaz
        resumen_dia: {
          ingresos: 450.00,
          ventas: 12,
          citas: 8
        },
        estadisticas_generales: {
          clientes_activos: 156,
          productos_bajo_stock: 3
        },
        citas_por_estado: {
          completadas: 4,
          en_proceso: 1,
          programadas: 3
        },
        servicios_populares: [
          { nombre: 'Corte de Cabello', total_ventas: 50 },
          { nombre: 'Arreglo de Barba', total_ventas: 30 },
          { nombre: 'Tinte', total_ventas: 20 },
        ],
        ingresos_semanales: [
          { semana: 'Semana 1', ingresos: 1200 },
          { semana: 'Semana 2', ingresos: 1500 },
          { semana: 'Semana 3', ingresos: 1300 },
          { semana: 'Semana 4', ingresos: 1600 },
        ]
      };
      setDashboardData(data);
    } catch (error) {
      setError('Error al cargar los datos del dashboard');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
        {error}
      </div>
    );
  }

  const { resumen_dia, estadisticas_generales, servicios_populares, ingresos_semanales } = dashboardData;

  const estadisticasCards = [
    {
      title: 'Ingresos Hoy',
      value: `$${resumen_dia.ingresos.toFixed(2)}`,
      icon: DollarSign,
      color: 'text-green-600',
      bgColor: 'bg-green-100'
    },
    {
      title: 'Ventas Hoy',
      value: resumen_dia.ventas,
      icon: TrendingUp,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100'
    },
    {
      title: 'Citas Hoy',
      value: resumen_dia.citas,
      icon: Calendar,
      color: 'text-purple-600',
      bgColor: 'bg-purple-100'
    },
    {
      title: 'Clientes Activos',
      value: estadisticas_generales.clientes_activos,
      icon: Users,
      color: 'text-indigo-600',
      bgColor: 'bg-indigo-100'
    }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Resumen general del negocio</p>
      </div>

      {/* Estadísticas principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {estadisticasCards.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div key={index} className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className={`${stat.bgColor} rounded-md p-3`}>
                  <Icon className={`h-6 w-6 ${stat.color}`} />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Alertas */}
      {estadisticas_generales.productos_bajo_stock > 0 && (
        <div className="bg-yellow-50 border border-yellow-200 text-yellow-700 px-4 py-3 rounded">
          <div className="flex items-center">
            <AlertTriangle className="h-5 w-5 text-yellow-600 mr-2" />
            <p className="text-yellow-800">
              <span className="font-medium">{estadisticas_generales.productos_bajo_stock}</span> productos con bajo stock
            </p>
          </div>
        </div>
      )}

      {/* Estado de citas del día */}
      {dashboardData.citas_por_estado && Object.keys(dashboardData.citas_por_estado).length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Estado de Citas Hoy</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {Object.entries(dashboardData.citas_por_estado).map(([estado, cantidad]) => (
              <div key={estado} className="text-center">
                <p className="text-2xl font-bold text-gray-900">{cantidad}</p>
                <p className="text-sm text-gray-600 capitalize">{estado.replace('_', ' ')}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Servicios más populares */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Servicios Más Populares</h3>
          {servicios_populares.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={servicios_populares}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="nombre" 
                  angle={-45}
                  textAnchor="end"
                  height={80}
                  fontSize={12}
                />
                <YAxis />
                <Tooltip />
                <Bar dataKey="total_ventas" fill="#3B82F6" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-gray-500 text-center py-8">No hay datos disponibles</p>
          )}
        </div>

        {/* Ingresos semanales */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Ingresos Semanales</h3>
          {ingresos_semanales.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={ingresos_semanales}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="semana" 
                  fontSize={12}
                />
                <YAxis />
                <Tooltip formatter={(value) => [`$${value.toFixed(2)}`, 'Ingresos']} />
                <Line 
                  type="monotone" 
                  dataKey="ingresos" 
                  stroke="#10B981" 
                  strokeWidth={2}
                  dot={{ fill: '#10B981' }}
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-gray-500 text-center py-8">No hay datos disponibles</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;


