# Migración de Backend: Flask a NestJS

## Resumen de la Migración

Este documento describe la migración completa del backend del Sistema POS SmartSalon de Flask a NestJS, implementando una arquitectura modular y escalable.

## Cambios Realizados

### 1. Arquitectura del Backend

**Antes (Flask):**
- Estructura monolítica
- Rutas en archivos separados
- Configuración manual de CORS y middleware

**Después (NestJS):**
- Arquitectura modular con decoradores
- Inyección de dependencias
- Estructura organizada por módulos

### 2. Estructura de Módulos

El nuevo backend NestJS incluye los siguientes módulos:

#### Módulo de Compañías (`/src/companias/`)
- **Controller:** Manejo de rutas HTTP
- **Service:** Lógica de negocio
- **DTOs:** Validación de datos de entrada
- **Entities:** Definición de tipos
- **Funcionalidades:** CRUD completo, paginación, soft delete

#### Módulo de Tiendas (`/src/tiendas/`)
- **Controller:** Gestión de sucursales
- **Service:** Operaciones de tiendas
- **DTOs:** Validación de datos
- **Entities:** Estructura de datos
- **Funcionalidades:** CRUD, relación con compañías

#### Módulo de Usuarios (`/src/usuarios/`)
- **Controller:** Gestión de usuarios
- **Service:** Autenticación y autorización
- **DTOs:** Validación de credenciales
- **Entities:** Estructura de usuario
- **Funcionalidades:** Login, registro, gestión de perfiles

#### Módulo de Personas (`/src/personas/`)
- **Controller:** Datos personales
- **Service:** Gestión de información personal
- **DTOs:** Validación de datos personales
- **Entities:** Estructura de persona
- **Funcionalidades:** CRUD de datos personales

#### Módulo de Roles (`/src/roles/`)
- **Controller:** Gestión de roles y permisos
- **Service:** Lógica de autorización
- **DTOs:** Validación de roles
- **Entities:** Estructura de roles
- **Funcionalidades:** CRUD de roles, gestión de permisos

### 3. Base de Datos

#### Nuevas Tablas Creadas:
- `companias` - Información de empresas
- `tiendas` - Sucursales por compañía
- `personas` - Datos personales
- `roles` - Roles y permisos del sistema
- `usuarios_nestjs` - Usuarios del sistema NestJS

#### Características:
- Relaciones entre tablas con claves foráneas
- Soft delete implementado
- Índices para optimización
- Timestamps automáticos

### 4. Autenticación y Seguridad

**Implementaciones:**
- JWT (JSON Web Tokens) para autenticación
- Bcrypt para hash de contraseñas
- Guards para protección de rutas
- Estrategias de Passport (Local y JWT)

### 5. Configuración del Entorno

**Variables de Entorno (.env):**
```
PORT=3000
DB_HOST=localhost
DB_PORT=5432
DB_NAME=pos_barberia
DB_USER=pos_user
DB_PASSWORD=pos_password
JWT_SECRET=smartsalon-pos-secret-key
JWT_EXPIRES_IN=24h
```

## Usuarios de Prueba

| Usuario | Email | Contraseña | Rol |
|---------|-------|------------|-----|
| admin | admin@barberia.com | admin123 | Administrador |
| gerente | gerente@barberia.com | gerente123 | Gerente |
| empleado | empleado@barberia.com | empleado123 | Empleado |
| recepcion | recepcion@barberia.com | recepcion123 | Recepcionista |

## Comandos de Instalación y Ejecución

### Backend NestJS:
```bash
cd backend
npm install
npm run start:dev
```

### Frontend React:
```bash
cd frontend
npm install
npm run dev
```

### Base de Datos:
```bash
# Crear tablas
sudo -u postgres psql -d pos_barberia < database/nestjs_schema.sql

# Insertar datos de prueba
sudo -u postgres psql -d pos_barberia < database/nestjs_seed_data.sql
```

## Endpoints de la API

### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `GET /api/auth/profile` - Obtener perfil del usuario

### Compañías
- `GET /api/companias` - Listar compañías
- `POST /api/companias` - Crear compañía
- `GET /api/companias/:id` - Obtener compañía
- `PATCH /api/companias/:id` - Actualizar compañía
- `DELETE /api/companias/:id` - Eliminar compañía

### Tiendas
- `GET /api/tiendas` - Listar tiendas
- `POST /api/tiendas` - Crear tienda
- `GET /api/tiendas/:id` - Obtener tienda
- `PATCH /api/tiendas/:id` - Actualizar tienda
- `DELETE /api/tiendas/:id` - Eliminar tienda

### Usuarios
- `GET /api/usuarios` - Listar usuarios
- `POST /api/usuarios` - Crear usuario
- `GET /api/usuarios/:id` - Obtener usuario
- `PATCH /api/usuarios/:id` - Actualizar usuario
- `DELETE /api/usuarios/:id` - Eliminar usuario

### Personas
- `GET /api/personas` - Listar personas
- `POST /api/personas` - Crear persona
- `GET /api/personas/:id` - Obtener persona
- `PATCH /api/personas/:id` - Actualizar persona
- `DELETE /api/personas/:id` - Eliminar persona

### Roles
- `GET /api/roles` - Listar roles
- `POST /api/roles` - Crear rol
- `GET /api/roles/:id` - Obtener rol
- `PATCH /api/roles/:id` - Actualizar rol
- `DELETE /api/roles/:id` - Eliminar rol

## Beneficios de la Migración

1. **Escalabilidad:** Arquitectura modular permite crecimiento fácil
2. **Mantenibilidad:** Código organizado y estructurado
3. **Tipo de Seguridad:** TypeScript proporciona tipado estático
4. **Documentación Automática:** Swagger integrado
5. **Testing:** Framework de testing robusto
6. **Inyección de Dependencias:** Mejor gestión de dependencias
7. **Decoradores:** Código más limpio y expresivo

## Estado del Proyecto

✅ **Completado:**
- Migración completa del backend a NestJS
- Todos los módulos implementados
- Base de datos configurada
- Autenticación funcionando
- Frontend integrado
- Documentación actualizada

🔄 **Próximos Pasos:**
- Implementar módulos adicionales (productos, servicios, ventas)
- Agregar validaciones avanzadas
- Implementar testing unitario
- Optimizar rendimiento de consultas
- Agregar logging y monitoreo

## Contacto y Soporte

Para cualquier consulta sobre la migración o el sistema, contactar al equipo de desarrollo de SmartSalon POS.

---
*Documento generado el 16 de julio de 2025*

