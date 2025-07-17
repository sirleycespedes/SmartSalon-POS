const API_BASE_URL = 'http://localhost:5000/api';

export const api = {
  login: async (email, password) => {
    console.log('API login called with:', { email, password: '***' });
    console.log('Making request to:', `${API_BASE_URL}/auth/login`);
    
    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });
      
      console.log('Response status:', response.status);
      console.log('Response headers:', response.headers);
      
      const data = await response.json();
      console.log('Response data:', data);
      
      return data;
    } catch (error) {
      console.error('API login error:', error);
      throw error;
    }
  },

  getProfile: async (token) => {
    const response = await fetch(`${API_BASE_URL}/auth/profile`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return response.json();
  },

  // Clientes
  getClientes: async (token) => {
    const response = await fetch(`${API_BASE_URL}/clientes`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return response.json();
  },

  // Empleados
  getEmpleados: async (token) => {
    const response = await fetch(`${API_BASE_URL}/empleados`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return response.json();
  },

  // Servicios
  getServicios: async (token) => {
    const response = await fetch(`${API_BASE_URL}/servicios`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return response.json();
  },

  // Productos
  getProductos: async (token) => {
    const response = await fetch(`${API_BASE_URL}/productos`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return response.json();
  },

  // Citas
  getCitas: async (token) => {
    const response = await fetch(`${API_BASE_URL}/citas`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return response.json();
  },

  // Ventas
  getVentas: async (token) => {
    const response = await fetch(`${API_BASE_URL}/ventas`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return response.json();
  },

  // Reportes
  getReportes: async (token) => {
    const response = await fetch(`${API_BASE_URL}/reportes`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return response.json();
  },
};


