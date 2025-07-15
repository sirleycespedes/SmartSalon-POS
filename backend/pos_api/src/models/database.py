from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    empleado = db.relationship('Empleado', backref='usuario', uselist=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'rol': self.rol,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }

class Empleado(db.Model):
    __tablename__ = 'empleados'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.Text)
    fecha_contratacion = db.Column(db.Date)
    salario_base = db.Column(db.Numeric(10, 2))
    comision_porcentaje = db.Column(db.Numeric(5, 2), default=0)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    citas = db.relationship('Cita', backref='empleado')
    ventas = db.relationship('Venta', backref='empleado')
    
    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'telefono': self.telefono,
            'direccion': self.direccion,
            'fecha_contratacion': self.fecha_contratacion.isoformat() if self.fecha_contratacion else None,
            'salario_base': float(self.salario_base) if self.salario_base else None,
            'comision_porcentaje': float(self.comision_porcentaje) if self.comision_porcentaje else None,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    direccion = db.Column(db.Text)
    fecha_nacimiento = db.Column(db.Date)
    notas = db.Column(db.Text)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    citas = db.relationship('Cita', backref='cliente')
    ventas = db.relationship('Venta', backref='cliente')
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'telefono': self.telefono,
            'email': self.email,
            'direccion': self.direccion,
            'fecha_nacimiento': self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None,
            'notas': self.notas,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }

class Servicio(db.Model):
    __tablename__ = 'servicios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    duracion_minutos = db.Column(db.Integer, nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    cita_servicios = db.relationship('CitaServicio', backref='servicio')
    venta_servicios = db.relationship('VentaServicio', backref='servicio')
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': float(self.precio),
            'duracion_minutos': self.duracion_minutos,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }

class Producto(db.Model):
    __tablename__ = 'productos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    stock_actual = db.Column(db.Integer, default=0)
    stock_minimo = db.Column(db.Integer, default=0)
    codigo_barras = db.Column(db.String(50))
    proveedor = db.Column(db.String(100))
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    venta_productos = db.relationship('VentaProducto', backref='producto')
    historial_stock = db.relationship('HistorialStock', backref='producto')
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': float(self.precio),
            'stock_actual': self.stock_actual,
            'stock_minimo': self.stock_minimo,
            'codigo_barras': self.codigo_barras,
            'proveedor': self.proveedor,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }

class Cita(db.Model):
    __tablename__ = 'citas'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'))
    fecha_hora = db.Column(db.DateTime, nullable=False)
    duracion_minutos = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(20), nullable=False, default='programada')
    notas = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    servicios = db.relationship('CitaServicio', backref='cita')
    venta = db.relationship('Venta', backref='cita', uselist=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'empleado_id': self.empleado_id,
            'fecha_hora': self.fecha_hora.isoformat() if self.fecha_hora else None,
            'duracion_minutos': self.duracion_minutos,
            'estado': self.estado,
            'notas': self.notas,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
            'cliente': self.cliente.to_dict() if self.cliente else None,
            'empleado': self.empleado.to_dict() if self.empleado else None,
            'servicios': [cs.to_dict() for cs in self.servicios]
        }

class CitaServicio(db.Model):
    __tablename__ = 'cita_servicios'
    
    id = db.Column(db.Integer, primary_key=True)
    cita_id = db.Column(db.Integer, db.ForeignKey('citas.id'), nullable=False)
    servicio_id = db.Column(db.Integer, db.ForeignKey('servicios.id'), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'cita_id': self.cita_id,
            'servicio_id': self.servicio_id,
            'precio': float(self.precio),
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'servicio': self.servicio.to_dict() if self.servicio else None
        }

class Venta(db.Model):
    __tablename__ = 'ventas'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'))
    cita_id = db.Column(db.Integer, db.ForeignKey('citas.id'))
    fecha_venta = db.Column(db.DateTime, default=datetime.utcnow)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    impuesto = db.Column(db.Numeric(10, 2), default=0)
    descuento = db.Column(db.Numeric(10, 2), default=0)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    metodo_pago = db.Column(db.String(20), nullable=False)
    estado = db.Column(db.String(20), nullable=False, default='pendiente')
    notas = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    servicios = db.relationship('VentaServicio', backref='venta')
    productos = db.relationship('VentaProducto', backref='venta')
    
    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'empleado_id': self.empleado_id,
            'cita_id': self.cita_id,
            'fecha_venta': self.fecha_venta.isoformat() if self.fecha_venta else None,
            'subtotal': float(self.subtotal),
            'impuesto': float(self.impuesto),
            'descuento': float(self.descuento),
            'total': float(self.total),
            'metodo_pago': self.metodo_pago,
            'estado': self.estado,
            'notas': self.notas,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
            'cliente': self.cliente.to_dict() if self.cliente else None,
            'empleado': self.empleado.to_dict() if self.empleado else None,
            'servicios': [vs.to_dict() for vs in self.servicios],
            'productos': [vp.to_dict() for vp in self.productos]
        }

class VentaServicio(db.Model):
    __tablename__ = 'venta_servicios'
    
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    servicio_id = db.Column(db.Integer, db.ForeignKey('servicios.id'), nullable=False)
    cantidad = db.Column(db.Integer, default=1)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'venta_id': self.venta_id,
            'servicio_id': self.servicio_id,
            'cantidad': self.cantidad,
            'precio_unitario': float(self.precio_unitario),
            'subtotal': float(self.subtotal),
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'servicio': self.servicio.to_dict() if self.servicio else None
        }

class VentaProducto(db.Model):
    __tablename__ = 'venta_productos'
    
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'venta_id': self.venta_id,
            'producto_id': self.producto_id,
            'cantidad': self.cantidad,
            'precio_unitario': float(self.precio_unitario),
            'subtotal': float(self.subtotal),
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'producto': self.producto.to_dict() if self.producto else None
        }

class HistorialStock(db.Model):
    __tablename__ = 'historial_stock'
    
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    tipo_movimiento = db.Column(db.String(20), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    stock_anterior = db.Column(db.Integer, nullable=False)
    stock_nuevo = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.Text)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'producto_id': self.producto_id,
            'tipo_movimiento': self.tipo_movimiento,
            'cantidad': self.cantidad,
            'stock_anterior': self.stock_anterior,
            'stock_nuevo': self.stock_nuevo,
            'motivo': self.motivo,
            'usuario_id': self.usuario_id,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'producto': self.producto.to_dict() if self.producto else None
        }

