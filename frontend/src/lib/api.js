const API_BASE_URL = 'http://localhost:3000/api';

export const api = {
  login: async (username, password) => {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });
    return response.json();
  },

  getProfile: async (token) => {
    const response = await fetch(`${API_BASE_URL}/auth/profile`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return response.json();
  },

  // Ejemplo de cómo se harían las llamadas a los nuevos módulos
  getCompanias: async (token) => {
    const response = await fetch(`${API_BASE_URL}/companias`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return response.json();
  },

  getTiendas: async (token) => {
    const response = await fetch(`${API_BASE_URL}/tiendas`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return response.json();
  },

  getUsuarios: async (token) => {
    const response = await fetch(`${API_BASE_URL}/usuarios`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return response.json();
  },

  getPersonas: async (token) => {
    const response = await fetch(`${API_BASE_URL}/personas`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return response.json();
  },

  getRoles: async (token) => {
    const response = await fetch(`${API_BASE_URL}/roles`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return response.json();
  },

  // Puedes añadir más funciones para CRUD de cada módulo aquí
};


