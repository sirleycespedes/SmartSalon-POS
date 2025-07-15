# Guía de Instalación - Sistema POS Barbería

Esta guía te llevará paso a paso por la instalación completa del Sistema POS para Peluquerías y Barberías.

## 📋 Requisitos Previos

### Sistema Operativo
- Ubuntu 20.04+ / Debian 11+
- Windows 10+ (con WSL2)
- macOS 11+

### Software Base
- Python 3.11 o superior
- Node.js 18.0 o superior
- PostgreSQL 12 o superior
- Git

## 🔧 Instalación Paso a Paso

### 1. Preparación del Sistema

#### Ubuntu/Debian
```bash
# Actualizar el sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias del sistema
sudo apt install -y python3.11 python3.11-venv python3-pip nodejs npm postgresql postgresql-contrib git curl

# Instalar pnpm globalmente
npm install -g pnpm
```

#### Windows (WSL2)
```bash
# Instalar WSL2 y Ubuntu
wsl --install -d Ubuntu

# Seguir los pasos de Ubuntu/Debian dentro de WSL
```

#### macOS
```bash
# Instalar Homebrew si no está instalado
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar dependencias
brew install python@3.11 node postgresql git
brew services start postgresql
```

### 2. Configuración de PostgreSQL

#### Inicialización del Servicio
```bash
# Ubuntu/Debian
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Verificar que PostgreSQL esté corriendo
sudo systemctl status postgresql
```

#### Creación de Base de Datos y Usuario
```bash
# Acceder a PostgreSQL como superusuario
sudo -u postgres psql

# Dentro de PostgreSQL, ejecutar:
CREATE DATABASE pos_barberia;
CREATE USER pos_user WITH PASSWORD 'pos_password_segura';
GRANT ALL PRIVILEGES ON DATABASE pos_barberia TO pos_user;
ALTER USER pos_user CREATEDB;
\q
```

#### Configuración de Acceso
```bash
# Editar archivo de configuración (Ubuntu/Debian)
sudo nano /etc/postgresql/*/main/pg_hba.conf

# Agregar o modificar la línea para permitir conexiones locales:
local   all             pos_user                                md5

# Reiniciar PostgreSQL
sudo systemctl restart postgresql
```

### 3. Descarga del Proyecto

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/pos-barberia-system.git
cd pos-barberia-system

# Verificar la estructura del proyecto
ls -la
```

### 4. Configuración de la Base de Datos

```bash
# Ejecutar el esquema de la base de datos
sudo -u postgres psql -d pos_barberia -f database/schema.sql

# Cargar datos de prueba
sudo -u postgres psql -d pos_barberia -f database/seed_data.sql

# Verificar que las tablas se crearon correctamente
sudo -u postgres psql -d pos_barberia -c "\dt"
```

### 5. Configuración del Backend

#### Crear Entorno Virtual
```bash
cd backend/pos_api

# Crear entorno virtual
python3.11 -m venv venv

# Activar entorno virtual
source venv/bin/activate  # Linux/macOS
# o
venv\Scripts\activate     # Windows
```

#### Instalar Dependencias
```bash
# Actualizar pip
pip install --upgrade pip

# Instalar dependencias del proyecto
pip install -r requirements.txt

# Verificar instalación
pip list
```

#### Configurar Variables de Entorno
```bash
# Crear archivo de configuración
cp .env.example .env  # Si existe
# o crear manualmente:
nano .env
```

Contenido del archivo `.env`:
```env
# Configuración de Base de Datos
DATABASE_URL=postgresql://pos_user:pos_password_segura@localhost/pos_barberia

# Configuración JWT
JWT_SECRET_KEY=tu-clave-secreta-muy-segura-y-larga-para-jwt

# Configuración Flask
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_APP=src/main.py

# Configuración CORS
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

#### Probar el Backend
```bash
# Asegurarse de estar en el directorio correcto y con el entorno activado
cd backend/pos_api
source venv/bin/activate

# Iniciar el servidor
python src/main.py

# En otra terminal, probar la API
curl http://localhost:5000/api/health
```

### 6. Configuración del Frontend

#### Instalar Dependencias
```bash
# Ir al directorio del frontend
cd frontend

# Instalar dependencias con pnpm
pnpm install

# Verificar instalación
pnpm list
```

#### Configurar Variables de Entorno
```bash
# Crear archivo de configuración del frontend
nano .env.local
```

Contenido del archivo `.env.local`:
```env
# URL del API Backend
VITE_API_BASE_URL=http://localhost:5000/api

# Configuración de desarrollo
VITE_NODE_ENV=development
```

#### Probar el Frontend
```bash
# Iniciar servidor de desarrollo
pnpm run dev

# El frontend estará disponible en http://localhost:5173
```

### 7. Verificación de la Instalación

#### Verificar Backend
```bash
# Probar endpoint de salud
curl -X GET http://localhost:5000/api/health

# Probar login con usuario de prueba
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@barberia.com", "password": "admin123"}'
```

#### Verificar Frontend
1. Abrir navegador en `http://localhost:5173`
2. Debería aparecer la página de login
3. Usar credenciales de prueba:
   - Email: `admin@barberia.com`
   - Contraseña: `admin123`

#### Verificar Base de Datos
```bash
# Conectar a la base de datos
sudo -u postgres psql -d pos_barberia

# Verificar datos de prueba
SELECT * FROM usuarios;
SELECT * FROM clientes LIMIT 5;
\q
```

## 🔧 Configuración Avanzada

### Configuración de Producción

#### Backend para Producción
```bash
# Instalar Gunicorn
pip install gunicorn

# Crear archivo de configuración
nano gunicorn.conf.py
```

Contenido de `gunicorn.conf.py`:
```python
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
```

#### Frontend para Producción
```bash
# Construir para producción
pnpm run build

# Los archivos estáticos estarán en dist/
ls -la dist/
```

### Configuración de Nginx (Opcional)
```bash
# Instalar Nginx
sudo apt install nginx

# Crear configuración del sitio
sudo nano /etc/nginx/sites-available/pos-barberia
```

Contenido de la configuración:
```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    # Frontend
    location / {
        root /ruta/al/proyecto/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
# Habilitar el sitio
sudo ln -s /etc/nginx/sites-available/pos-barberia /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 🐳 Instalación con Docker (Alternativa)

### Prerequisitos
```bash
# Instalar Docker y Docker Compose
sudo apt install docker.io docker-compose
sudo usermod -aG docker $USER
```

### Usar Docker Compose
```bash
# Crear archivo docker-compose.yml en la raíz del proyecto
nano docker-compose.yml
```

Contenido básico:
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: pos_barberia
      POSTGRES_USER: pos_user
      POSTGRES_PASSWORD: pos_password_segura
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database:/docker-entrypoint-initdb.d
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://pos_user:pos_password_segura@postgres/pos_barberia
    ports:
      - "5000:5000"
    depends_on:
      - postgres

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    depends_on:
      - backend

volumes:
  postgres_data:
```

```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f
```

## 🚨 Solución de Problemas Comunes

### Error de Conexión a PostgreSQL
```bash
# Verificar que PostgreSQL esté corriendo
sudo systemctl status postgresql

# Verificar configuración de conexión
sudo -u postgres psql -c "SELECT version();"

# Revisar logs de PostgreSQL
sudo tail -f /var/log/postgresql/postgresql-*.log
```

### Error de Permisos en Base de Datos
```bash
# Otorgar permisos completos al usuario
sudo -u postgres psql -d pos_barberia
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO pos_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO pos_user;
\q
```

### Error de Dependencias Python
```bash
# Limpiar caché de pip
pip cache purge

# Reinstalar dependencias
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Error de Dependencias Node.js
```bash
# Limpiar caché de pnpm
pnpm store prune

# Reinstalar dependencias
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

### Puerto en Uso
```bash
# Verificar qué proceso usa el puerto
sudo lsof -i :5000  # Para backend
sudo lsof -i :5173  # Para frontend

# Terminar proceso si es necesario
sudo kill -9 <PID>
```

## ✅ Lista de Verificación Post-Instalación

- [ ] PostgreSQL instalado y corriendo
- [ ] Base de datos `pos_barberia` creada
- [ ] Usuario `pos_user` con permisos correctos
- [ ] Esquema de base de datos ejecutado
- [ ] Datos de prueba cargados
- [ ] Backend corriendo en puerto 5000
- [ ] Frontend corriendo en puerto 5173
- [ ] Login funcional con usuarios de prueba
- [ ] API respondiendo correctamente
- [ ] Sin errores en consola del navegador

## 📞 Soporte

Si encuentras problemas durante la instalación:

1. Revisa los logs de cada componente
2. Verifica que todos los servicios estén corriendo
3. Consulta la sección de solución de problemas
4. Crea un issue en GitHub con detalles del error

---

¡Felicidades! Tu Sistema POS para Peluquerías y Barberías está listo para usar. 🎉

