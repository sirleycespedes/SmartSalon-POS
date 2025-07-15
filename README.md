# Sistema POS para Peluquerías y Barberías

Un sistema de punto de venta (POS) completo diseñado específicamente para peluquerías y barberías, desarrollado con React, Flask y PostgreSQL.

## 🚀 Características Principales

### Gestión de Clientes
- Registro completo de información del cliente
- Historial de servicios y compras
- Sistema de búsqueda avanzada
- Notas personalizadas por cliente

### Gestión de Empleados
- Control de acceso por roles (Administrador, Empleado)
- Gestión de horarios y disponibilidad
- Seguimiento de comisiones y ventas

### Servicios y Productos
- Catálogo completo de servicios de peluquería/barbería
- Gestión de inventario de productos
- Control de stock con alertas automáticas
- Precios dinámicos y promociones

### Sistema de Citas
- Calendario interactivo
- Gestión de disponibilidad por empleado
- Recordatorios automáticos
- Estados de cita (Programada, En Proceso, Completada, Cancelada)

### Punto de Venta
- Interfaz intuitiva para ventas rápidas
- Combinación de servicios y productos
- Múltiples métodos de pago
- Generación automática de recibos

### Reportes y Estadísticas
- Dashboard con métricas en tiempo real
- Reportes de ventas por período
- Análisis de productos más vendidos
- Estadísticas de empleados y clientes

## 🛠️ Tecnologías Utilizadas

### Frontend
- **React 18** - Biblioteca de JavaScript para interfaces de usuario
- **React Router** - Navegación entre páginas
- **Tailwind CSS** - Framework de CSS para diseño responsive
- **Lucide React** - Iconos modernos
- **Recharts** - Gráficos y visualizaciones

### Backend
- **Flask** - Framework web de Python
- **SQLAlchemy** - ORM para base de datos
- **Flask-JWT-Extended** - Autenticación JWT
- **Flask-CORS** - Manejo de CORS
- **Bcrypt** - Encriptación de contraseñas

### Base de Datos
- **PostgreSQL** - Base de datos relacional
- **Psycopg2** - Adaptador de PostgreSQL para Python

## 📋 Requisitos del Sistema

### Software Requerido
- Python 3.11+
- Node.js 18+
- PostgreSQL 12+
- npm o pnpm

### Dependencias Python
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-CORS==4.0.0
Flask-JWT-Extended==4.5.3
psycopg2-binary==2.9.10
bcrypt==4.0.1
```

### Dependencias Node.js
```
react==18.2.0
react-dom==18.2.0
react-router-dom==6.15.0
tailwindcss==3.3.3
lucide-react==0.263.1
recharts==2.8.0
```

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/pos-barberia-system.git
cd pos-barberia-system
```

### 2. Configurar la Base de Datos
```bash
# Instalar PostgreSQL (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib

# Iniciar el servicio
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Crear base de datos y usuario
sudo -u postgres psql
CREATE DATABASE pos_barberia;
CREATE USER pos_user WITH PASSWORD 'pos_password';
GRANT ALL PRIVILEGES ON DATABASE pos_barberia TO pos_user;
\q

# Ejecutar el esquema
sudo -u postgres psql -d pos_barberia < database/schema.sql
sudo -u postgres psql -d pos_barberia < database/seed_data.sql
```

### 3. Configurar el Backend
```bash
cd backend/pos_api

# Crear entorno virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno (opcional)
export DATABASE_URL="postgresql://pos_user:pos_password@localhost/pos_barberia"
export JWT_SECRET_KEY="tu-clave-secreta-jwt"

# Iniciar el servidor
python src/main.py
```

### 4. Configurar el Frontend
```bash
cd frontend

# Instalar dependencias
pnpm install

# Iniciar el servidor de desarrollo
pnpm run dev
```

## 🔧 Configuración

### Variables de Entorno

#### Backend (.env)
```
DATABASE_URL=postgresql://pos_user:pos_password@localhost/pos_barberia
JWT_SECRET_KEY=tu-clave-secreta-muy-segura
FLASK_ENV=development
FLASK_DEBUG=True
```

#### Frontend (.env)
```
VITE_API_BASE_URL=http://localhost:5000/api
```

## 👥 Usuarios de Prueba

El sistema incluye usuarios de prueba para facilitar las pruebas:

### Administrador
- **Email:** admin@barberia.com
- **Contraseña:** admin123
- **Permisos:** Acceso completo al sistema

### Empleado
- **Email:** juan@barberia.com
- **Contraseña:** admin123
- **Permisos:** Acceso limitado (sin gestión de empleados ni reportes avanzados)

## 📱 Uso del Sistema

### Acceso al Sistema
1. Abrir el navegador en `http://localhost:5173`
2. Iniciar sesión con las credenciales de prueba
3. Navegar por los diferentes módulos usando el menú lateral

### Flujo de Trabajo Típico
1. **Registrar Cliente:** Agregar información del cliente en el módulo de Clientes
2. **Programar Cita:** Usar el calendario para agendar servicios
3. **Realizar Venta:** Procesar servicios y productos en el POS
4. **Generar Reportes:** Revisar estadísticas y métricas en el Dashboard

## 🗂️ Estructura del Proyecto

```
pos-barberia-system/
├── backend/
│   └── pos_api/
│       ├── src/
│       │   ├── main.py              # Aplicación principal
│       │   ├── config.py            # Configuración
│       │   ├── models/
│       │   │   └── database.py      # Modelos de datos
│       │   └── routes/
│       │       ├── auth.py          # Autenticación
│       │       ├── clientes.py      # Gestión de clientes
│       │       ├── empleados.py     # Gestión de empleados
│       │       ├── servicios.py     # Gestión de servicios
│       │       ├── productos.py     # Gestión de productos
│       │       ├── citas.py         # Gestión de citas
│       │       ├── ventas.py        # Punto de venta
│       │       └── reportes.py      # Reportes y estadísticas
│       ├── venv/                    # Entorno virtual
│       └── requirements.txt         # Dependencias Python
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Layout.jsx           # Layout principal
│   │   │   └── ProtectedRoute.jsx   # Rutas protegidas
│   │   ├── contexts/
│   │   │   └── AuthContext.jsx      # Contexto de autenticación
│   │   ├── lib/
│   │   │   └── api.js               # Cliente API
│   │   ├── pages/
│   │   │   ├── Login.jsx            # Página de login
│   │   │   ├── Dashboard.jsx        # Dashboard principal
│   │   │   └── Clientes.jsx         # Gestión de clientes
│   │   └── App.jsx                  # Componente principal
│   ├── package.json                 # Dependencias Node.js
│   └── tailwind.config.js           # Configuración Tailwind
├── database/
│   ├── schema.sql                   # Esquema de la base de datos
│   └── seed_data.sql                # Datos de prueba
└── README.md                        # Este archivo
```

## 🔌 API Endpoints

### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `GET /api/auth/me` - Obtener usuario actual

### Clientes
- `GET /api/clientes` - Listar clientes
- `POST /api/clientes` - Crear cliente
- `GET /api/clientes/{id}` - Obtener cliente
- `PUT /api/clientes/{id}` - Actualizar cliente
- `DELETE /api/clientes/{id}` - Desactivar cliente

### Empleados
- `GET /api/empleados` - Listar empleados
- `POST /api/empleados` - Crear empleado
- `GET /api/empleados/{id}` - Obtener empleado
- `PUT /api/empleados/{id}` - Actualizar empleado

### Servicios
- `GET /api/servicios` - Listar servicios
- `POST /api/servicios` - Crear servicio
- `PUT /api/servicios/{id}` - Actualizar servicio

### Productos
- `GET /api/productos` - Listar productos
- `POST /api/productos` - Crear producto
- `PUT /api/productos/{id}` - Actualizar producto
- `POST /api/productos/{id}/stock` - Ajustar stock

### Citas
- `GET /api/citas` - Listar citas
- `POST /api/citas` - Crear cita
- `PUT /api/citas/{id}` - Actualizar cita
- `DELETE /api/citas/{id}` - Cancelar cita
- `GET /api/citas/disponibilidad` - Verificar disponibilidad
- `GET /api/citas/calendario` - Vista de calendario

### Ventas
- `GET /api/ventas` - Listar ventas
- `POST /api/ventas` - Crear venta
- `PUT /api/ventas/{id}` - Actualizar venta
- `POST /api/ventas/{id}/anular` - Anular venta

### Reportes
- `GET /api/reportes/dashboard` - Datos del dashboard
- `GET /api/reportes/ventas-periodo` - Reporte de ventas
- `GET /api/reportes/inventario` - Reporte de inventario
- `GET /api/reportes/clientes` - Estadísticas de clientes

## 🔒 Seguridad

### Autenticación
- Sistema JWT para autenticación stateless
- Tokens con expiración configurable
- Encriptación de contraseñas con bcrypt

### Autorización
- Control de acceso basado en roles
- Rutas protegidas en frontend y backend
- Validación de permisos por endpoint

### Base de Datos
- Conexiones seguras a PostgreSQL
- Validación de entrada en todos los endpoints
- Prevención de inyección SQL con SQLAlchemy ORM

## 🧪 Testing

### Backend
```bash
cd backend/pos_api
source venv/bin/activate
python -m pytest tests/
```

### Frontend
```bash
cd frontend
pnpm test
```

## 📦 Deployment

### Producción con Docker
```bash
# Construir imágenes
docker-compose build

# Iniciar servicios
docker-compose up -d
```

### Deployment Manual
1. Configurar servidor con Python 3.11+ y Node.js 18+
2. Instalar PostgreSQL y crear base de datos
3. Configurar variables de entorno de producción
4. Construir frontend: `pnpm run build`
5. Configurar servidor web (Nginx) como proxy reverso
6. Usar Gunicorn para servir la aplicación Flask

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o preguntas sobre el sistema:

- **Email:** soporte@possystem.com
- **Documentación:** [Wiki del Proyecto](https://github.com/tu-usuario/pos-barberia-system/wiki)
- **Issues:** [GitHub Issues](https://github.com/tu-usuario/pos-barberia-system/issues)

## 🔄 Changelog

### v1.0.0 (2025-07-15)
- ✅ Sistema completo de gestión de clientes
- ✅ Autenticación y autorización
- ✅ Dashboard con estadísticas en tiempo real
- ✅ API REST completa
- ✅ Interfaz responsive con React
- ✅ Base de datos PostgreSQL optimizada
- ✅ Documentación completa

---

**Desarrollado con ❤️ para la comunidad de peluquerías y barberías**

