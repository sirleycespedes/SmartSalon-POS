-- Datos de prueba para el sistema POS de peluquerías y barberías

-- Insertar usuarios del sistema
INSERT INTO usuarios (nombre, email, password_hash, rol) VALUES
('Administrador', 'admin@barberia.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/VcSAg9S6O', 'admin'), -- password: admin123
('Juan Pérez', 'juan@barberia.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/VcSAg9S6O', 'empleado'), -- password: admin123
('María García', 'maria@barberia.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/VcSAg9S6O', 'empleado'); -- password: admin123

-- Insertar empleados
INSERT INTO empleados (usuario_id, nombre, apellido, telefono, direccion, fecha_contratacion, salario_base, comision_porcentaje) VALUES
(2, 'Juan', 'Pérez', '555-0101', 'Calle Principal 123', '2024-01-15', 2500.00, 15.00),
(3, 'María', 'García', '555-0102', 'Avenida Central 456', '2024-02-01', 2300.00, 12.00);

-- Insertar clientes
INSERT INTO clientes (nombre, apellido, telefono, email, direccion, fecha_nacimiento, notas) VALUES
('Carlos', 'Rodríguez', '555-1001', 'carlos@email.com', 'Calle 1 #100', '1985-03-15', 'Cliente frecuente, prefiere cortes clásicos'),
('Ana', 'López', '555-1002', 'ana@email.com', 'Calle 2 #200', '1990-07-22', 'Alérgica a ciertos productos químicos'),
('Pedro', 'Martínez', '555-1003', 'pedro@email.com', 'Calle 3 #300', '1988-11-10', 'Le gusta probar estilos nuevos'),
('Laura', 'Sánchez', '555-1004', 'laura@email.com', 'Calle 4 #400', '1992-05-18', 'Viene cada mes para mantenimiento'),
('Miguel', 'Torres', '555-1005', 'miguel@email.com', 'Calle 5 #500', '1987-09-03', 'Prefiere citas temprano en la mañana');

-- Insertar servicios
INSERT INTO servicios (nombre, descripcion, precio, duracion_minutos) VALUES
('Corte de Cabello Hombre', 'Corte tradicional para hombre con lavado', 25.00, 30),
('Corte de Cabello Mujer', 'Corte y peinado para mujer con lavado', 35.00, 45),
('Afeitado Clásico', 'Afeitado tradicional con navaja y toalla caliente', 20.00, 25),
('Barba y Bigote', 'Arreglo y diseño de barba y bigote', 15.00, 20),
('Tinte de Cabello', 'Aplicación de tinte con lavado y secado', 50.00, 90),
('Peinado Especial', 'Peinado para eventos especiales', 30.00, 40),
('Lavado y Secado', 'Lavado profundo con acondicionador y secado', 12.00, 20),
('Tratamiento Capilar', 'Tratamiento nutritivo para el cabello', 40.00, 60);

-- Insertar productos
INSERT INTO productos (nombre, descripcion, precio, stock_actual, stock_minimo, codigo_barras, proveedor) VALUES
('Champú Profesional 500ml', 'Champú para uso profesional, fórmula suave', 18.50, 25, 5, '7501234567890', 'Distribuidora Beauty'),
('Acondicionador 500ml', 'Acondicionador hidratante para todo tipo de cabello', 16.00, 20, 5, '7501234567891', 'Distribuidora Beauty'),
('Gel Fijador Fuerte', 'Gel de fijación fuerte, larga duración', 12.00, 30, 8, '7501234567892', 'Productos Estilo'),
('Cera Modeladora', 'Cera para modelar y dar textura al cabello', 15.00, 15, 3, '7501234567893', 'Productos Estilo'),
('Espuma de Afeitar', 'Espuma cremosa para afeitado suave', 8.50, 40, 10, '7501234567894', 'Barbería Supply'),
('Loción Aftershave', 'Loción calmante post-afeitado', 22.00, 12, 3, '7501234567895', 'Barbería Supply'),
('Tinte Castaño Oscuro', 'Tinte permanente color castaño oscuro', 28.00, 8, 2, '7501234567896', 'Color Pro'),
('Tinte Rubio Claro', 'Tinte permanente color rubio claro', 28.00, 6, 2, '7501234567897', 'Color Pro'),
('Aceite Capilar', 'Aceite nutritivo para cabello seco', 25.00, 10, 2, '7501234567898', 'Natural Hair'),
('Spray Fijador', 'Spray de fijación media, acabado natural', 14.00, 22, 5, '7501234567899', 'Productos Estilo');

-- Insertar citas de ejemplo
INSERT INTO citas (cliente_id, empleado_id, fecha_hora, duracion_minutos, estado, notas) VALUES
(1, 1, '2024-07-15 09:00:00', 30, 'completada', 'Corte regular, cliente satisfecho'),
(2, 2, '2024-07-15 10:30:00', 45, 'completada', 'Corte y peinado para evento'),
(3, 1, '2024-07-15 14:00:00', 25, 'completada', 'Afeitado clásico'),
(4, 2, '2024-07-16 11:00:00', 90, 'programada', 'Tinte de cabello - confirmar color'),
(5, 1, '2024-07-16 15:30:00', 30, 'programada', 'Corte mensual');

-- Insertar servicios por cita
INSERT INTO cita_servicios (cita_id, servicio_id, precio) VALUES
(1, 1, 25.00),
(2, 2, 35.00),
(3, 3, 20.00),
(4, 5, 50.00),
(5, 1, 25.00);

-- Insertar ventas de ejemplo
INSERT INTO ventas (cliente_id, empleado_id, cita_id, subtotal, impuesto, total, metodo_pago, estado) VALUES
(1, 1, 1, 25.00, 2.00, 27.00, 'efectivo', 'completada'),
(2, 2, 2, 35.00, 2.80, 37.80, 'tarjeta', 'completada'),
(3, 1, 3, 20.00, 1.60, 21.60, 'efectivo', 'completada');

-- Insertar servicios vendidos
INSERT INTO venta_servicios (venta_id, servicio_id, cantidad, precio_unitario, subtotal) VALUES
(1, 1, 1, 25.00, 25.00),
(2, 2, 1, 35.00, 35.00),
(3, 3, 1, 20.00, 20.00);

-- Insertar algunos productos vendidos
INSERT INTO venta_productos (venta_id, producto_id, cantidad, precio_unitario, subtotal) VALUES
(2, 3, 1, 12.00, 12.00),
(3, 5, 1, 8.50, 8.50);

-- Actualizar totales de ventas que incluyen productos
UPDATE ventas SET 
    subtotal = subtotal + 12.00,
    impuesto = (subtotal + 12.00) * 0.08,
    total = (subtotal + 12.00) * 1.08
WHERE id = 2;

UPDATE ventas SET 
    subtotal = subtotal + 8.50,
    impuesto = (subtotal + 8.50) * 0.08,
    total = (subtotal + 8.50) * 1.08
WHERE id = 3;

