-- Datos de prueba para SmartSalon POS - Backend NestJS

-- Insertar compañía de prueba
INSERT INTO companias (nit, nombre, razon_social, direccion, telefono, email, sitio_web) VALUES
('900123456-1', 'SmartSalon Group', 'SmartSalon Group S.A.S.', 'Calle 123 #45-67, Bogotá', '+57 1 234-5678', 'info@smartsalon.com', 'https://smartsalon.com')
ON CONFLICT (nit) DO NOTHING;

-- Insertar tiendas de prueba
INSERT INTO tiendas (compania_id, codigo, nombre, direccion, telefono, email, horario_apertura, horario_cierre) VALUES
(1, 'BOG001', 'SmartSalon Chapinero', 'Carrera 13 #63-45, Chapinero, Bogotá', '+57 1 345-6789', 'chapinero@smartsalon.com', '08:00:00', '20:00:00'),
(1, 'BOG002', 'SmartSalon Zona Rosa', 'Calle 82 #12-34, Zona Rosa, Bogotá', '+57 1 456-7890', 'zonarosa@smartsalon.com', '09:00:00', '21:00:00')
ON CONFLICT (codigo) DO NOTHING;

-- Insertar roles de prueba
INSERT INTO roles (nombre, descripcion, permisos) VALUES
('Administrador', 'Acceso completo al sistema', '{"all": true}'),
('Gerente', 'Gestión de tienda y empleados', '{"tienda": true, "empleados": true, "reportes": true}'),
('Empleado', 'Operaciones básicas de POS', '{"ventas": true, "clientes": true, "servicios": true}'),
('Recepcionista', 'Gestión de citas y clientes', '{"citas": true, "clientes": true}')
ON CONFLICT (nombre) DO NOTHING;

-- Insertar personas de prueba
INSERT INTO personas (tipo_documento, numero_documento, nombres, apellidos, fecha_nacimiento, genero, telefono, email, direccion) VALUES
('CC', '12345678', 'Juan Carlos', 'Administrador', '1985-05-15', 'M', '+57 300 123-4567', 'admin@barberia.com', 'Calle 100 #15-20'),
('CC', '87654321', 'María Elena', 'Gerente', '1990-08-22', 'F', '+57 310 987-6543', 'gerente@barberia.com', 'Carrera 50 #25-30'),
('CC', '11223344', 'Carlos Alberto', 'Empleado', '1992-03-10', 'M', '+57 320 456-7890', 'empleado@barberia.com', 'Avenida 68 #40-50'),
('CC', '44332211', 'Ana Sofía', 'Recepcionista', '1995-11-05', 'F', '+57 315 789-0123', 'recepcion@barberia.com', 'Calle 72 #30-40')
ON CONFLICT (numero_documento) DO NOTHING;

-- Insertar usuarios de prueba (con contraseñas hasheadas para 'admin123', 'gerente123', etc.)
-- Nota: Las contraseñas están hasheadas con bcrypt
INSERT INTO usuarios_nestjs (persona_id, tienda_id, role_id, username, email, password_hash) VALUES
(1, 1, 1, 'admin', 'admin@barberia.com', '$2a$10$DgnwiAYHYdd2xTFbcetagOUj17.LKWIapwNlnVmhiIf6n0c2.WQ3.'),
(2, 1, 2, 'gerente', 'gerente@barberia.com', '$2a$10$qDnKrqpSRgBduIN16x/Khe0ONceIeXl/xOCOM4f1QQRcsBXDx48re'),
(3, 1, 3, 'empleado', 'empleado@barberia.com', '$2a$10$dl9GvJ70YOrk6h4RQoW1AuZqx/1Xg6P4muWXFckeKHeSXwV8A4t7S'),
(4, 2, 4, 'recepcion', 'recepcion@barberia.com', '$2a$10$.kUfF0V8mHnn9NqwP3at2e05LNG7DSV5vRXzhnTxS67qfGJZOLmLC')
ON CONFLICT (username) DO NOTHING;

-- Verificar que los datos se insertaron correctamente
SELECT 'Compañías insertadas:' as info, COUNT(*) as total FROM companias;
SELECT 'Tiendas insertadas:' as info, COUNT(*) as total FROM tiendas;
SELECT 'Roles insertados:' as info, COUNT(*) as total FROM roles;
SELECT 'Personas insertadas:' as info, COUNT(*) as total FROM personas;
SELECT 'Usuarios insertados:' as info, COUNT(*) as total FROM usuarios_nestjs;

