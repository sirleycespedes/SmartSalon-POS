from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.database import db, Venta, VentaServicio, VentaProducto, Cliente, Empleado, Servicio, Producto
from datetime import datetime, timedelta
from sqlalchemy import func

ventas_bp = Blueprint('ventas', __name__)

@ventas_bp.route('/', methods=['GET'])
@jwt_required()
def get_ventas():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        empleado_id = request.args.get('empleado_id', type=int)
        cliente_id = request.args.get('cliente_id', type=int)
        estado = request.args.get('estado')
        metodo_pago = request.args.get('metodo_pago')
        
        query = Venta.query
        
        if fecha_inicio:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            query = query.filter(Venta.fecha_venta >= fecha_inicio)
        
        if fecha_fin:
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d') + timedelta(days=1)
            query = query.filter(Venta.fecha_venta < fecha_fin)
        
        if empleado_id:
            query = query.filter(Venta.empleado_id == empleado_id)
        
        if cliente_id:
            query = query.filter(Venta.cliente_id == cliente_id)
        
        if estado:
            query = query.filter(Venta.estado == estado)
        
        if metodo_pago:
            query = query.filter(Venta.metodo_pago == metodo_pago)
        
        ventas = query.order_by(Venta.fecha_venta.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'ventas': [venta.to_dict() for venta in ventas.items],
            'total': ventas.total,
            'pages': ventas.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ventas_bp.route('/<int:venta_id>', methods=['GET'])
@jwt_required()
def get_venta(venta_id):
    try:
        venta = Venta.query.get_or_404(venta_id)
        return jsonify({'venta': venta.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ventas_bp.route('/', methods=['POST'])
@jwt_required()
def create_venta():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        required_fields = ['total', 'metodo_pago']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} es requerido'}), 400
        
        # Validar cliente si se proporciona
        if data.get('cliente_id'):
            cliente = Cliente.query.get(data['cliente_id'])
            if not cliente:
                return jsonify({'error': 'Cliente no encontrado'}), 404
        
        # Validar empleado si se proporciona
        if data.get('empleado_id'):
            empleado = Empleado.query.get(data['empleado_id'])
            if not empleado:
                return jsonify({'error': 'Empleado no encontrado'}), 404
        
        # Crear venta
        venta = Venta(
            cliente_id=data.get('cliente_id'),
            empleado_id=data.get('empleado_id'),
            cita_id=data.get('cita_id'),
            subtotal=data.get('subtotal', data['total']),
            impuesto=data.get('impuesto', 0),
            descuento=data.get('descuento', 0),
            total=data['total'],
            metodo_pago=data['metodo_pago'],
            estado=data.get('estado', 'completada'),
            notas=data.get('notas')
        )
        
        db.session.add(venta)
        db.session.flush()  # Para obtener el ID de la venta
        
        # Agregar servicios vendidos
        if data.get('servicios'):
            for servicio_data in data['servicios']:
                servicio = Servicio.query.get(servicio_data['servicio_id'])
                if not servicio:
                    return jsonify({'error': f'Servicio {servicio_data["servicio_id"]} no encontrado'}), 404
                
                venta_servicio = VentaServicio(
                    venta_id=venta.id,
                    servicio_id=servicio.id,
                    cantidad=servicio_data.get('cantidad', 1),
                    precio_unitario=servicio_data.get('precio_unitario', servicio.precio),
                    subtotal=servicio_data.get('cantidad', 1) * servicio_data.get('precio_unitario', servicio.precio)
                )
                db.session.add(venta_servicio)
        
        # Agregar productos vendidos
        if data.get('productos'):
            for producto_data in data['productos']:
                producto = Producto.query.get(producto_data['producto_id'])
                if not producto:
                    return jsonify({'error': f'Producto {producto_data["producto_id"]} no encontrado'}), 404
                
                cantidad = producto_data['cantidad']
                if producto.stock_actual < cantidad:
                    return jsonify({'error': f'Stock insuficiente para {producto.nombre}'}), 400
                
                venta_producto = VentaProducto(
                    venta_id=venta.id,
                    producto_id=producto.id,
                    cantidad=cantidad,
                    precio_unitario=producto_data.get('precio_unitario', producto.precio),
                    subtotal=cantidad * producto_data.get('precio_unitario', producto.precio)
                )
                db.session.add(venta_producto)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Venta creada exitosamente',
            'venta': venta.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@ventas_bp.route('/<int:venta_id>', methods=['PUT'])
@jwt_required()
def update_venta(venta_id):
    try:
        venta = Venta.query.get_or_404(venta_id)
        data = request.get_json()
        
        # Solo permitir actualizar ciertos campos
        if 'estado' in data:
            venta.estado = data['estado']
        if 'notas' in data:
            venta.notas = data['notas']
        if 'metodo_pago' in data:
            venta.metodo_pago = data['metodo_pago']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Venta actualizada exitosamente',
            'venta': venta.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@ventas_bp.route('/<int:venta_id>/anular', methods=['POST'])
@jwt_required()
def anular_venta(venta_id):
    try:
        current_user_id = get_jwt_identity()
        from src.models.database import Usuario
        current_user = Usuario.query.get(current_user_id)
        
        if current_user.rol != 'admin':
            return jsonify({'error': 'No tienes permisos para anular ventas'}), 403
        
        venta = Venta.query.get_or_404(venta_id)
        
        if venta.estado == 'cancelada':
            return jsonify({'error': 'La venta ya está cancelada'}), 400
        
        # Restaurar stock de productos vendidos
        for venta_producto in venta.productos:
            producto = venta_producto.producto
            producto.stock_actual += venta_producto.cantidad
            
            # Registrar movimiento en historial
            from src.models.database import HistorialStock
            historial = HistorialStock(
                producto_id=producto.id,
                tipo_movimiento='entrada',
                cantidad=venta_producto.cantidad,
                stock_anterior=producto.stock_actual - venta_producto.cantidad,
                stock_nuevo=producto.stock_actual,
                motivo=f'Anulación de venta #{venta.id}',
                usuario_id=current_user_id
            )
            db.session.add(historial)
        
        venta.estado = 'cancelada'
        db.session.commit()
        
        return jsonify({
            'message': 'Venta anulada exitosamente',
            'venta': venta.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@ventas_bp.route('/estadisticas', methods=['GET'])
@jwt_required()
def get_estadisticas_ventas():
    try:
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        empleado_id = request.args.get('empleado_id', type=int)
        
        # Filtros base
        query = Venta.query.filter(Venta.estado == 'completada')
        
        if fecha_inicio:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            query = query.filter(Venta.fecha_venta >= fecha_inicio)
        
        if fecha_fin:
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d') + timedelta(days=1)
            query = query.filter(Venta.fecha_venta < fecha_fin)
        
        if empleado_id:
            query = query.filter(Venta.empleado_id == empleado_id)
        
        ventas = query.all()
        
        # Calcular estadísticas
        total_ventas = len(ventas)
        total_ingresos = sum(float(venta.total) for venta in ventas)
        promedio_venta = total_ingresos / total_ventas if total_ventas > 0 else 0
        
        # Ventas por método de pago
        ventas_por_metodo = {}
        for venta in ventas:
            metodo = venta.metodo_pago
            if metodo not in ventas_por_metodo:
                ventas_por_metodo[metodo] = {'cantidad': 0, 'total': 0}
            ventas_por_metodo[metodo]['cantidad'] += 1
            ventas_por_metodo[metodo]['total'] += float(venta.total)
        
        # Ventas por día (últimos 7 días si no se especifica rango)
        if not fecha_inicio:
            fecha_inicio = datetime.now() - timedelta(days=7)
        if not fecha_fin:
            fecha_fin = datetime.now()
        
        ventas_por_dia = {}
        fecha_actual = fecha_inicio.date()
        fecha_fin_date = fecha_fin.date() if isinstance(fecha_fin, datetime) else fecha_fin
        
        while fecha_actual <= fecha_fin_date:
            ventas_por_dia[fecha_actual.isoformat()] = {'cantidad': 0, 'total': 0}
            fecha_actual += timedelta(days=1)
        
        for venta in ventas:
            fecha_venta = venta.fecha_venta.date().isoformat()
            if fecha_venta in ventas_por_dia:
                ventas_por_dia[fecha_venta]['cantidad'] += 1
                ventas_por_dia[fecha_venta]['total'] += float(venta.total)
        
        return jsonify({
            'total_ventas': total_ventas,
            'total_ingresos': total_ingresos,
            'promedio_venta': promedio_venta,
            'ventas_por_metodo': ventas_por_metodo,
            'ventas_por_dia': ventas_por_dia
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ventas_bp.route('/reporte-diario', methods=['GET'])
@jwt_required()
def get_reporte_diario():
    try:
        fecha = request.args.get('fecha', datetime.now().strftime('%Y-%m-%d'))
        fecha_inicio = datetime.strptime(fecha, '%Y-%m-%d')
        fecha_fin = fecha_inicio + timedelta(days=1)
        
        ventas = Venta.query.filter(
            Venta.fecha_venta >= fecha_inicio,
            Venta.fecha_venta < fecha_fin,
            Venta.estado == 'completada'
        ).all()
        
        # Resumen del día
        total_ventas = len(ventas)
        total_ingresos = sum(float(venta.total) for venta in ventas)
        
        # Servicios más vendidos
        servicios_vendidos = {}
        for venta in ventas:
            for venta_servicio in venta.servicios:
                servicio_id = venta_servicio.servicio_id
                if servicio_id not in servicios_vendidos:
                    servicios_vendidos[servicio_id] = {
                        'servicio': venta_servicio.servicio.to_dict(),
                        'cantidad': 0,
                        'total': 0
                    }
                servicios_vendidos[servicio_id]['cantidad'] += venta_servicio.cantidad
                servicios_vendidos[servicio_id]['total'] += float(venta_servicio.subtotal)
        
        # Productos más vendidos
        productos_vendidos = {}
        for venta in ventas:
            for venta_producto in venta.productos:
                producto_id = venta_producto.producto_id
                if producto_id not in productos_vendidos:
                    productos_vendidos[producto_id] = {
                        'producto': venta_producto.producto.to_dict(),
                        'cantidad': 0,
                        'total': 0
                    }
                productos_vendidos[producto_id]['cantidad'] += venta_producto.cantidad
                productos_vendidos[producto_id]['total'] += float(venta_producto.subtotal)
        
        return jsonify({
            'fecha': fecha,
            'resumen': {
                'total_ventas': total_ventas,
                'total_ingresos': total_ingresos
            },
            'servicios_vendidos': list(servicios_vendidos.values()),
            'productos_vendidos': list(productos_vendidos.values()),
            'ventas_detalle': [venta.to_dict() for venta in ventas]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

