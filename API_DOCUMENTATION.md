# Documentación de API - Sistema POS Barbería

Esta documentación describe todos los endpoints disponibles en la API REST del Sistema POS para Peluquerías y Barberías.

## 🔗 URL Base

```
http://localhost:5000/api
```

## 🔐 Autenticación

La API utiliza JWT (JSON Web Tokens) para autenticación. Todos los endpoints (excepto login y health) requieren un token válido.

### Headers Requeridos
```http
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

## 📋 Endpoints Disponibles

### 🏥 Health Check

#### GET /health
Verifica el estado de la API.

**Respuesta:**
```json
{
  "status": "OK",
  "message": "API funcionando correctamente"
}
```

---

## 🔐 Autenticación

### POST /auth/login
Autentica un usuario y devuelve un token JWT.

**Parámetros:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Respuesta Exitosa (200):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "usuario": {
    "id": 1,
    "nombre": "Administrador",
    "email": "admin@barberia.com",
    "rol": "administrador"
  }
}
```

**Errores:**
- `400`: Credenciales inválidas
- `401`: Usuario inactivo

### GET /auth/me
Obtiene información del usuario autenticado.

**Headers:** `Authorization: Bearer <token>`

**Respuesta (200):**
```json
{
  "usuario": {
    "id": 1,
    "nombre": "Administrador",
    "email": "admin@barberia.com",
    "rol": "administrador",
    "activo": true,
    "fecha_creacion": "2025-01-15T10:00:00"
  }
}
```

---

## 👥 Clientes

### GET /clientes
Lista todos los clientes activos.

**Parámetros de consulta:**
- `search` (opcional): Buscar por nombre, apellido o email
- `page` (opcional): Número de página (default: 1)
- `per_page` (opcional): Elementos por página (default: 20)

**Respuesta (200):**
```json
{
  "clientes": [
    {
      "id": 1,
      "nombre": "Juan",
      "apellido": "Pérez",
      "telefono": "+1234567890",
      "email": "juan@email.com",
      "direccion": "Calle 123",
      "fecha_nacimiento": "1990-05-15",
      "notas": "Cliente frecuente",
      "activo": true,
      "fecha_creacion": "2025-01-15T10:00:00",
      "fecha_actualizacion": "2025-01-15T10:00:00"
    }
  ],
  "total": 1,
  "page": 1,
  "per_page": 20,
  "pages": 1
}
```

### POST /clientes
Crea un nuevo cliente.

**Parámetros:**
```json
{
  "nombre": "string (requerido)",
  "apellido": "string (requerido)",
  "telefono": "string (opcional)",
  "email": "string (opcional)",
  "direccion": "string (opcional)",
  "fecha_nacimiento": "date (opcional, formato: YYYY-MM-DD)",
  "notas": "string (opcional)"
}
```

**Respuesta (201):**
```json
{
  "message": "Cliente creado exitosamente",
  "cliente": {
    "id": 2,
    "nombre": "María",
    "apellido": "García",
    "telefono": "+0987654321",
    "email": "maria@email.com",
    "direccion": "Avenida 456",
    "fecha_nacimiento": "1985-08-20",
    "notas": "Prefiere cortes modernos",
    "activo": true,
    "fecha_creacion": "2025-01-15T11:00:00",
    "fecha_actualizacion": "2025-01-15T11:00:00"
  }
}
```

### GET /clientes/{id}
Obtiene un cliente específico por ID.

**Respuesta (200):**
```json
{
  "cliente": {
    "id": 1,
    "nombre": "Juan",
    "apellido": "Pérez",
    "telefono": "+1234567890",
    "email": "juan@email.com",
    "direccion": "Calle 123",
    "fecha_nacimiento": "1990-05-15",
    "notas": "Cliente frecuente",
    "activo": true,
    "fecha_creacion": "2025-01-15T10:00:00",
    "fecha_actualizacion": "2025-01-15T10:00:00"
  }
}
```

### PUT /clientes/{id}
Actualiza un cliente existente.

**Parámetros:** (Mismos que POST, todos opcionales)

**Respuesta (200):**
```json
{
  "message": "Cliente actualizado exitosamente",
  "cliente": { /* datos actualizados */ }
}
```

### DELETE /clientes/{id}
Desactiva un cliente (soft delete).

**Respuesta (200):**
```json
{
  "message": "Cliente desactivado exitosamente"
}
```

---

## 👨‍💼 Empleados

### GET /empleados
Lista todos los empleados activos.

**Respuesta (200):**
```json
{
  "empleados": [
    {
      "id": 1,
      "nombre": "Juan Carlos",
      "apellido": "Rodríguez",
      "telefono": "+1234567890",
      "email": "juan@barberia.com",
      "direccion": "Calle Principal 123",
      "fecha_nacimiento": "1985-03-15",
      "fecha_contratacion": "2024-01-01",
      "salario": 2500.00,
      "comision_porcentaje": 15.0,
      "especialidades": "Corte clásico, Barba",
      "horario_trabajo": "Lunes a Viernes 9:00-18:00",
      "activo": true,
      "fecha_creacion": "2025-01-15T10:00:00"
    }
  ]
}
```

### POST /empleados
Crea un nuevo empleado.

**Parámetros:**
```json
{
  "nombre": "string (requerido)",
  "apellido": "string (requerido)",
  "telefono": "string (opcional)",
  "email": "string (opcional)",
  "direccion": "string (opcional)",
  "fecha_nacimiento": "date (opcional)",
  "fecha_contratacion": "date (requerido)",
  "salario": "decimal (opcional)",
  "comision_porcentaje": "decimal (opcional)",
  "especialidades": "string (opcional)",
  "horario_trabajo": "string (opcional)"
}
```

### GET /empleados/{id}
Obtiene un empleado específico.

### PUT /empleados/{id}
Actualiza un empleado existente.

---

## ✂️ Servicios

### GET /servicios
Lista todos los servicios disponibles.

**Respuesta (200):**
```json
{
  "servicios": [
    {
      "id": 1,
      "nombre": "Corte de Cabello Clásico",
      "descripcion": "Corte tradicional con tijeras",
      "precio": 25.00,
      "duracion_minutos": 30,
      "categoria": "Corte",
      "activo": true,
      "fecha_creacion": "2025-01-15T10:00:00"
    }
  ]
}
```

### POST /servicios
Crea un nuevo servicio.

**Parámetros:**
```json
{
  "nombre": "string (requerido)",
  "descripcion": "string (opcional)",
  "precio": "decimal (requerido)",
  "duracion_minutos": "integer (requerido)",
  "categoria": "string (opcional)"
}
```

### PUT /servicios/{id}
Actualiza un servicio existente.

---

## 📦 Productos

### GET /productos
Lista todos los productos.

**Parámetros de consulta:**
- `categoria` (opcional): Filtrar por categoría
- `bajo_stock` (opcional): Solo productos con stock bajo

**Respuesta (200):**
```json
{
  "productos": [
    {
      "id": 1,
      "nombre": "Shampoo Premium",
      "descripcion": "Shampoo para todo tipo de cabello",
      "precio": 15.50,
      "categoria": "Cuidado Capilar",
      "stock_actual": 25,
      "stock_minimo": 10,
      "codigo_barras": "1234567890123",
      "activo": true,
      "fecha_creacion": "2025-01-15T10:00:00"
    }
  ]
}
```

### POST /productos
Crea un nuevo producto.

**Parámetros:**
```json
{
  "nombre": "string (requerido)",
  "descripcion": "string (opcional)",
  "precio": "decimal (requerido)",
  "categoria": "string (opcional)",
  "stock_actual": "integer (requerido)",
  "stock_minimo": "integer (opcional)",
  "codigo_barras": "string (opcional)"
}
```

### PUT /productos/{id}
Actualiza un producto existente.

### POST /productos/{id}/stock
Ajusta el stock de un producto.

**Parámetros:**
```json
{
  "tipo": "entrada|salida|ajuste",
  "cantidad": "integer",
  "motivo": "string (opcional)"
}
```

**Respuesta (200):**
```json
{
  "message": "Stock ajustado exitosamente",
  "stock_anterior": 25,
  "stock_nuevo": 30
}
```

---

## 📅 Citas

### GET /citas
Lista las citas.

**Parámetros de consulta:**
- `fecha_inicio` (opcional): Filtrar desde fecha (YYYY-MM-DD)
- `fecha_fin` (opcional): Filtrar hasta fecha (YYYY-MM-DD)
- `empleado_id` (opcional): Filtrar por empleado
- `estado` (opcional): Filtrar por estado

**Respuesta (200):**
```json
{
  "citas": [
    {
      "id": 1,
      "cliente_id": 1,
      "empleado_id": 1,
      "fecha_hora": "2025-01-16T14:00:00",
      "estado": "programada",
      "notas": "Corte y barba",
      "precio_total": 35.00,
      "fecha_creacion": "2025-01-15T10:00:00",
      "cliente": {
        "nombre": "Juan",
        "apellido": "Pérez"
      },
      "empleado": {
        "nombre": "Juan Carlos",
        "apellido": "Rodríguez"
      },
      "servicios": [
        {
          "id": 1,
          "nombre": "Corte de Cabello",
          "precio": 25.00
        }
      ]
    }
  ]
}
```

### POST /citas
Crea una nueva cita.

**Parámetros:**
```json
{
  "cliente_id": "integer (requerido)",
  "empleado_id": "integer (requerido)",
  "fecha_hora": "datetime (requerido, formato: YYYY-MM-DD HH:MM:SS)",
  "servicios": [
    {
      "servicio_id": "integer",
      "precio": "decimal (opcional)"
    }
  ],
  "notas": "string (opcional)"
}
```

### PUT /citas/{id}
Actualiza una cita existente.

### DELETE /citas/{id}
Cancela una cita.

### GET /citas/disponibilidad
Verifica disponibilidad de horarios.

**Parámetros de consulta:**
- `empleado_id`: ID del empleado
- `fecha`: Fecha a consultar (YYYY-MM-DD)
- `duracion`: Duración en minutos

**Respuesta (200):**
```json
{
  "disponible": true,
  "horarios_disponibles": [
    "09:00",
    "09:30",
    "10:00",
    "10:30"
  ]
}
```

### GET /citas/calendario
Vista de calendario de citas.

**Parámetros de consulta:**
- `fecha_inicio`: Fecha inicio del rango
- `fecha_fin`: Fecha fin del rango
- `empleado_id` (opcional): Filtrar por empleado

---

## 💰 Ventas

### GET /ventas
Lista las ventas realizadas.

**Parámetros de consulta:**
- `fecha_inicio` (opcional): Desde fecha
- `fecha_fin` (opcional): Hasta fecha
- `empleado_id` (opcional): Por empleado

**Respuesta (200):**
```json
{
  "ventas": [
    {
      "id": 1,
      "cliente_id": 1,
      "empleado_id": 1,
      "fecha_venta": "2025-01-15T15:30:00",
      "subtotal": 40.00,
      "descuento": 0.00,
      "impuestos": 4.00,
      "total": 44.00,
      "metodo_pago": "efectivo",
      "estado": "completada",
      "notas": "Venta regular",
      "cliente": {
        "nombre": "Juan",
        "apellido": "Pérez"
      },
      "empleado": {
        "nombre": "Juan Carlos",
        "apellido": "Rodríguez"
      },
      "servicios": [
        {
          "servicio_id": 1,
          "nombre": "Corte de Cabello",
          "precio": 25.00,
          "cantidad": 1
        }
      ],
      "productos": [
        {
          "producto_id": 1,
          "nombre": "Shampoo Premium",
          "precio": 15.00,
          "cantidad": 1
        }
      ]
    }
  ]
}
```

### POST /ventas
Registra una nueva venta.

**Parámetros:**
```json
{
  "cliente_id": "integer (opcional)",
  "empleado_id": "integer (requerido)",
  "servicios": [
    {
      "servicio_id": "integer",
      "precio": "decimal",
      "cantidad": "integer (default: 1)"
    }
  ],
  "productos": [
    {
      "producto_id": "integer",
      "precio": "decimal",
      "cantidad": "integer"
    }
  ],
  "descuento": "decimal (opcional, default: 0)",
  "metodo_pago": "string (efectivo|tarjeta|transferencia)",
  "notas": "string (opcional)"
}
```

### PUT /ventas/{id}
Actualiza una venta (solo si no está completada).

### POST /ventas/{id}/anular
Anula una venta.

**Parámetros:**
```json
{
  "motivo": "string (requerido)"
}
```

---

## 📊 Reportes

### GET /reportes/dashboard
Obtiene datos para el dashboard principal.

**Respuesta (200):**
```json
{
  "resumen_dia": {
    "ingresos": 450.00,
    "ventas": 12,
    "citas": 8,
    "citas_por_estado": {
      "programada": 3,
      "en_proceso": 1,
      "completada": 4
    }
  },
  "estadisticas_generales": {
    "clientes_activos": 156,
    "productos_bajo_stock": 3,
    "empleados_activos": 4
  },
  "servicios_populares": [
    {
      "nombre": "Corte de Cabello",
      "total_ventas": 25
    }
  ],
  "ingresos_semanales": [
    {
      "semana": "2025-W02",
      "ingresos": 2500.00
    }
  ]
}
```

### GET /reportes/ventas-periodo
Reporte de ventas por período.

**Parámetros de consulta:**
- `fecha_inicio`: Fecha inicio (YYYY-MM-DD)
- `fecha_fin`: Fecha fin (YYYY-MM-DD)
- `empleado_id` (opcional): Por empleado

**Respuesta (200):**
```json
{
  "periodo": {
    "fecha_inicio": "2025-01-01",
    "fecha_fin": "2025-01-15"
  },
  "resumen": {
    "total_ventas": 15,
    "ingresos_totales": 1250.00,
    "ticket_promedio": 83.33
  },
  "ventas_por_dia": [
    {
      "fecha": "2025-01-15",
      "ventas": 3,
      "ingresos": 180.00
    }
  ],
  "servicios_mas_vendidos": [
    {
      "nombre": "Corte de Cabello",
      "cantidad": 12,
      "ingresos": 300.00
    }
  ],
  "productos_mas_vendidos": [
    {
      "nombre": "Shampoo Premium",
      "cantidad": 8,
      "ingresos": 124.00
    }
  ]
}
```

### GET /reportes/inventario
Reporte de inventario actual.

**Respuesta (200):**
```json
{
  "resumen": {
    "total_productos": 25,
    "valor_inventario": 2500.00,
    "productos_bajo_stock": 3
  },
  "productos": [
    {
      "id": 1,
      "nombre": "Shampoo Premium",
      "stock_actual": 5,
      "stock_minimo": 10,
      "valor_stock": 77.50,
      "estado": "bajo_stock"
    }
  ],
  "movimientos_recientes": [
    {
      "producto_id": 1,
      "tipo": "salida",
      "cantidad": 2,
      "fecha": "2025-01-15T14:30:00",
      "motivo": "Venta"
    }
  ]
}
```

### GET /reportes/clientes
Estadísticas de clientes.

**Respuesta (200):**
```json
{
  "resumen": {
    "total_clientes": 156,
    "clientes_nuevos_mes": 12,
    "clientes_frecuentes": 45
  },
  "clientes_top": [
    {
      "cliente_id": 1,
      "nombre": "Juan Pérez",
      "total_gastado": 450.00,
      "visitas": 8
    }
  ],
  "nuevos_clientes": [
    {
      "cliente_id": 2,
      "nombre": "María García",
      "fecha_registro": "2025-01-10",
      "primera_compra": 65.00
    }
  ]
}
```

---

## 🚨 Códigos de Error

### Códigos HTTP Estándar
- `200`: Éxito
- `201`: Creado exitosamente
- `400`: Solicitud incorrecta
- `401`: No autorizado
- `403`: Prohibido
- `404`: No encontrado
- `422`: Entidad no procesable (errores de validación)
- `500`: Error interno del servidor

### Formato de Errores
```json
{
  "error": "Descripción del error",
  "code": "ERROR_CODE",
  "details": {
    "field": "Detalle específico del campo"
  }
}
```

### Errores Comunes
- `INVALID_CREDENTIALS`: Credenciales incorrectas
- `TOKEN_EXPIRED`: Token JWT expirado
- `VALIDATION_ERROR`: Error de validación de datos
- `RESOURCE_NOT_FOUND`: Recurso no encontrado
- `INSUFFICIENT_STOCK`: Stock insuficiente
- `APPOINTMENT_CONFLICT`: Conflicto de horario en cita

---

## 📝 Notas Adicionales

### Paginación
Los endpoints que devuelven listas soportan paginación:
- `page`: Número de página (default: 1)
- `per_page`: Elementos por página (default: 20, máximo: 100)

### Filtros de Fecha
Las fechas deben enviarse en formato ISO 8601:
- Fecha: `YYYY-MM-DD`
- Fecha y hora: `YYYY-MM-DD HH:MM:SS`

### Validaciones
- Los campos marcados como "requerido" son obligatorios
- Los emails deben tener formato válido
- Los precios deben ser números positivos
- Las fechas deben ser válidas y en formato correcto

### Límites de Rate
- 100 requests por minuto por IP
- 1000 requests por hora por usuario autenticado

---

Para más información o soporte, consulta la documentación completa del proyecto.

