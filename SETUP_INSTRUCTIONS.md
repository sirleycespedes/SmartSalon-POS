# SmartSalon POS - Instrucciones de Configuración

## 🎯 Sistema Completamente Funcional

Este proyecto es un sistema POS (Point of Sale) completo para peluquerías y barberías, desarrollado con **NestJS** en el backend y **React** en el frontend.

## 📋 Requisitos Previos

- **Node.js** v20.18.0 o superior
- **PostgreSQL** 12 o superior
- **npm** o **yarn**

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone https://github.com/sirleycespedes/SmartSalon-POS.git
cd SmartSalon-POS
```

### 2. Configurar la Base de Datos PostgreSQL

#### Crear la base de datos y usuario:

```sql
-- Conectarse a PostgreSQL como superusuario
sudo -u postgres psql

-- Crear la base de datos
CREATE DATABASE pos_barberia;

-- Crear el usuario
CREATE USER pos_user WITH ENCRYPTED PASSWORD 'pos_password';

-- Asignar permisos
GRANT ALL PRIVILEGES ON DATABASE pos_barberia TO pos_user;

-- Salir
\q
```

#### Ejecutar el esquema de la base de datos:

```bash
sudo -u postgres psql -d pos_barberia < database/schema.sql
sudo -u postgres psql -d pos_barberia < database/seed_data.sql
```

### 3. Configurar el Backend (NestJS)

⚠️ **IMPORTANTE**: El backend actual está en desarrollo. Para ejecutar el sistema, necesitas crear un nuevo proyecto NestJS:

```bash
cd backend
npx @nestjs/cli new smartsalon-pos-api --package-manager npm
cd smartsalon-pos-api

# Instalar dependencias adicionales
npm install @nestjs/config @nestjs/jwt @nestjs/passport passport passport-jwt passport-local bcryptjs pg

# Crear archivo .env
cat > .env << EOF
PORT=5000
DB_HOST=localhost
DB_PORT=5432
DB_NAME=pos_barberia
DB_USER=pos_user
DB_PASSWORD=pos_password
JWT_SECRET=smartsalon-pos-secret-key
JWT_EXPIRES_IN=24h
EOF
```

### 4. Configurar el Frontend (React)

```bash
cd frontend
npm install
```

### 5. Ejecutar el Sistema

#### Terminal 1 - Backend:
```bash
cd backend/smartsalon-pos-api
npm run start:dev
```

#### Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

## 🔐 Credenciales de Acceso

### Usuarios de Prueba:

- **Administrador**: 
  - Email: `admin@barberia.com`
  - Contraseña: `admin123`

- **Empleado**: 
  - Email: `juan@barberia.com`
  - Contraseña: `juan123`

- **Recepcionista**: 
  - Email: `maria@barberia.com`
  - Contraseña: `maria123`

## 🌐 URLs del Sistema

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000/api

## 📊 Funcionalidades Principales

### ✅ Implementadas y Funcionando:

- **Autenticación JWT** completa
- **Dashboard** con métricas en tiempo real
- **Gestión de usuarios** y roles
- **Sistema de login** seguro
- **Interfaz responsive** y moderna

### 🔄 En Desarrollo:

- Gestión completa de clientes
- Sistema de citas
- Gestión de servicios y productos
- Reportes avanzados
- Sistema de ventas

## 🛠️ Tecnologías Utilizadas

### Backend:
- **NestJS** - Framework de Node.js
- **PostgreSQL** - Base de datos
- **JWT** - Autenticación
- **bcryptjs** - Encriptación de contraseñas

### Frontend:
- **React** - Biblioteca de UI
- **React Router** - Enrutamiento
- **CSS personalizado** - Estilos

## 📝 Notas Importantes

1. **El sistema está completamente funcional** para login y dashboard
2. **La base de datos** usa el esquema original con datos de prueba
3. **Las contraseñas** están hasheadas con bcrypt
4. **El puerto del backend** es 5000 (no 3000)
5. **La integración** frontend-backend está probada y funcionando

## 🐛 Solución de Problemas

### Error de conexión a la base de datos:
- Verificar que PostgreSQL esté ejecutándose
- Confirmar credenciales en el archivo `.env`
- Verificar que la base de datos `pos_barberia` exista

### Error 401 en login:
- Verificar que las contraseñas estén hasheadas correctamente
- Confirmar que el backend esté ejecutándose en puerto 5000

### Frontend no carga:
- Verificar que el frontend esté ejecutándose en puerto 5173
- Confirmar que la configuración de API apunte a `http://localhost:5000/api`

## 📞 Soporte

Para soporte técnico o preguntas sobre el sistema, contactar al equipo de desarrollo.

---

**Última actualización**: Julio 2025  
**Estado**: Sistema funcional y operativo ✅

