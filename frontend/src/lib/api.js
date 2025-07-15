const API_BASE_URL = 'http://localhost:5001/api';

class ApiClient {
  constructor() {
    this.token = localStorage.getItem('token');
  }

  setToken(token) {
    this.token = token;
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
  }

  getHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    };
    
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }
    
    return headers;
  }

  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: this.getHeaders(),
      ...options,
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Error en la petición');
      }

      return data;
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  // Métodos de autenticación
  async login(email, password) {
    const response = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    
    if (response.access_token) {
      this.setToken(response.access_token);
    }
    
    return response;
  }

  async logout() {
    this.setToken(null);
  }

  async getCurrentUser() {
    return this.request('/auth/me');
  }

  // Métodos para clientes
  async getClientes(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/clientes?${queryString}`);
  }

  async getCliente(id) {
    return this.request(`/clientes/${id}`);
  }

  async createCliente(clienteData) {
    return this.request('/clientes', {
      method: 'POST',
      body: JSON.stringify(clienteData),
    });
  }

  async updateCliente(id, clienteData) {
    return this.request(`/clientes/${id}`, {
      method: 'PUT',
      body: JSON.stringify(clienteData),
    });
  }

  async deleteCliente(id) {
    return this.request(`/clientes/${id}`, {
      method: 'DELETE',
    });
  }

  // Métodos para empleados
  async getEmpleados(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/empleados?${queryString}`);
  }

  async getEmpleado(id) {
    return this.request(`/empleados/${id}`);
  }

  async createEmpleado(empleadoData) {
    return this.request('/empleados', {
      method: 'POST',
      body: JSON.stringify(empleadoData),
    });
  }

  async updateEmpleado(id, empleadoData) {
    return this.request(`/empleados/${id}`, {
      method: 'PUT',
      body: JSON.stringify(empleadoData),
    });
  }

  // Métodos para servicios
  async getServicios(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/servicios?${queryString}`);
  }

  async getServicio(id) {
    return this.request(`/servicios/${id}`);
  }

  async createServicio(servicioData) {
    return this.request('/servicios', {
      method: 'POST',
      body: JSON.stringify(servicioData),
    });
  }

  async updateServicio(id, servicioData) {
    return this.request(`/servicios/${id}`, {
      method: 'PUT',
      body: JSON.stringify(servicioData),
    });
  }

  // Métodos para productos
  async getProductos(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/productos?${queryString}`);
  }

  async getProducto(id) {
    return this.request(`/productos/${id}`);
  }

  async createProducto(productoData) {
    return this.request('/productos', {
      method: 'POST',
      body: JSON.stringify(productoData),
    });
  }

  async updateProducto(id, productoData) {
    return this.request(`/productos/${id}`, {
      method: 'PUT',
      body: JSON.stringify(productoData),
    });
  }

  async ajustarStock(id, stockData) {
    return this.request(`/productos/${id}/stock`, {
      method: 'POST',
      body: JSON.stringify(stockData),
    });
  }

  // Métodos para citas
  async getCitas(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/citas?${queryString}`);
  }

  async getCita(id) {
    return this.request(`/citas/${id}`);
  }

  async createCita(citaData) {
    return this.request('/citas', {
      method: 'POST',
      body: JSON.stringify(citaData),
    });
  }

  async updateCita(id, citaData) {
    return this.request(`/citas/${id}`, {
      method: 'PUT',
      body: JSON.stringify(citaData),
    });
  }

  async deleteCita(id) {
    return this.request(`/citas/${id}`, {
      method: 'DELETE',
    });
  }

  async getDisponibilidad(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/citas/disponibilidad?${queryString}`);
  }

  async getCalendario(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/citas/calendario?${queryString}`);
  }

  // Métodos para ventas
  async getVentas(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/ventas?${queryString}`);
  }

  async getVenta(id) {
    return this.request(`/ventas/${id}`);
  }

  async createVenta(ventaData) {
    return this.request('/ventas', {
      method: 'POST',
      body: JSON.stringify(ventaData),
    });
  }

  async updateVenta(id, ventaData) {
    return this.request(`/ventas/${id}`, {
      method: 'PUT',
      body: JSON.stringify(ventaData),
    });
  }

  async anularVenta(id) {
    return this.request(`/ventas/${id}/anular`, {
      method: 'POST',
    });
  }

  // Métodos para reportes
  async getDashboard() {
    return this.request('/reportes/dashboard');
  }

  async getReporteVentas(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/reportes/ventas-periodo?${queryString}`);
  }

  async getReporteInventario(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/reportes/inventario?${queryString}`);
  }

  async getReporteClientes() {
    return this.request('/reportes/clientes');
  }
}

export const apiClient = new ApiClient();

