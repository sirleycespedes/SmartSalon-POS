-- Esquema de base de datos para SmartSalon POS - Backend NestJS
-- Creación de tablas para el sistema modular

-- Tabla de Compañías
CREATE TABLE IF NOT EXISTS companias (
    id SERIAL PRIMARY KEY,
    nit VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    razon_social VARCHAR(255) NOT NULL,
    direccion TEXT,
    telefono VARCHAR(20),
    email VARCHAR(255),
    sitio_web VARCHAR(255),
    logo_url VARCHAR(500),
    activo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

-- Tabla de Tiendas/Sucursales
CREATE TABLE IF NOT EXISTS tiendas (
    id SERIAL PRIMARY KEY,
    compania_id INTEGER REFERENCES companias(id) ON DELETE CASCADE,
    codigo VARCHAR(10) UNIQUE NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    direccion TEXT NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(255),
    horario_apertura TIME,
    horario_cierre TIME,
    activo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

-- Tabla de Personas
CREATE TABLE IF NOT EXISTS personas (
    id SERIAL PRIMARY KEY,
    tipo_documento VARCHAR(10) NOT NULL DEFAULT 'CC',
    numero_documento VARCHAR(20) UNIQUE NOT NULL,
    nombres VARCHAR(255) NOT NULL,
    apellidos VARCHAR(255) NOT NULL,
    fecha_nacimiento DATE,
    genero VARCHAR(10),
    telefono VARCHAR(20),
    email VARCHAR(255),
    direccion TEXT,
    activo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

-- Tabla de Roles
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT,
    permisos JSONB DEFAULT '{}',
    activo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

-- Tabla de Usuarios (actualizada para NestJS)
CREATE TABLE IF NOT EXISTS usuarios_nestjs (
    id SERIAL PRIMARY KEY,
    persona_id INTEGER REFERENCES personas(id) ON DELETE CASCADE,
    tienda_id INTEGER REFERENCES tiendas(id) ON DELETE SET NULL,
    role_id INTEGER REFERENCES roles(id) ON DELETE SET NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    ultimo_login TIMESTAMP,
    activo BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

-- Índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_companias_nit ON companias(nit);
CREATE INDEX IF NOT EXISTS idx_tiendas_compania ON tiendas(compania_id);
CREATE INDEX IF NOT EXISTS idx_tiendas_codigo ON tiendas(codigo);
CREATE INDEX IF NOT EXISTS idx_personas_documento ON personas(numero_documento);
CREATE INDEX IF NOT EXISTS idx_personas_email ON personas(email);
CREATE INDEX IF NOT EXISTS idx_usuarios_username ON usuarios_nestjs(username);
CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios_nestjs(email);
CREATE INDEX IF NOT EXISTS idx_usuarios_persona ON usuarios_nestjs(persona_id);

-- Comentarios en las tablas
COMMENT ON TABLE companias IS 'Tabla de compañías/empresas del sistema';
COMMENT ON TABLE tiendas IS 'Tabla de tiendas/sucursales por compañía';
COMMENT ON TABLE personas IS 'Tabla de personas (datos personales)';
COMMENT ON TABLE roles IS 'Tabla de roles y permisos del sistema';
COMMENT ON TABLE usuarios_nestjs IS 'Tabla de usuarios del sistema NestJS';

