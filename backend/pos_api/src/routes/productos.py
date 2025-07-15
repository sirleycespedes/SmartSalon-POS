from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.database import db, Producto, Usuario, HistorialStock

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/', methods=['GET'])
@jwt_required()
def get_productos():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        activo = request.args.get('activo', 'true').lower() == 'true'
        bajo_stock = request.args.get('bajo_stock', 'false').lower() == 'true'
        
        query = Producto.query.filter_by(activo=activo)
        
        if search:
            query = query.filter(
                db.or_(
                    Producto.nombre.ilike(f'%{search}%'),
                    Producto.descripcion.ilike(f'%{search}%'),
                    Producto.codigo_barras.ilike(f'%{search}%'),
                    Producto.proveedor.ilike(f'%{search}%')
                )
            )
        
        if bajo_stock:
            query = query.filter(Producto.stock_actual <= Producto.stock_minimo)
        
        productos = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'productos': [producto.to_dict() for producto in productos.items],
            'total': productos.total,
            'pages': productos.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@productos_bp.route('/<int:producto_id>', methods=['GET'])
@jwt_required()
def get_producto(producto_id):
    try:
        producto = Producto.query.get_or_404(producto_id)
        return jsonify({'producto': producto.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@productos_bp.route('/', methods=['POST'])
@jwt_required()
def create_producto():
    try:
        current_user_id = get_jwt_identity()
        current_user = Usuario.query.get(current_user_id)
        
        if current_user.rol != 'admin':
            return jsonify({'error': 'No tienes permisos para crear productos'}), 403
        
        data = request.get_json()
        
        required_fields = ['nombre', 'precio']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} es requerido'}), 400
        
        producto = Producto(
            nombre=data['nombre'],
            descripcion=data.get('descripcion'),
            precio=data['precio'],
            stock_actual=data.get('stock_actual', 0),
            stock_minimo=data.get('stock_minimo', 0),
            codigo_barras=data.get('codigo_barras'),
            proveedor=data.get('proveedor')
        )
        
        db.session.add(producto)
        db.session.commit()
        
        # Registrar movimiento inicial de stock si es mayor a 0
        if producto.stock_actual > 0:
            historial = HistorialStock(
                producto_id=producto.id,
                tipo_movimiento='entrada',
                cantidad=producto.stock_actual,
                stock_anterior=0,
                stock_nuevo=producto.stock_actual,
                motivo='Stock inicial',
                usuario_id=current_user_id
            )
            db.session.add(historial)
            db.session.commit()
        
        return jsonify({
            'message': 'Producto creado exitosamente',
            'producto': producto.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@productos_bp.route('/<int:producto_id>', methods=['PUT'])
@jwt_required()
def update_producto(producto_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = Usuario.query.get(current_user_id)
        
        if current_user.rol != 'admin':
            return jsonify({'error': 'No tienes permisos para actualizar productos'}), 403
        
        producto = Producto.query.get_or_404(producto_id)
        data = request.get_json()
        
        # Actualizar campos
        if 'nombre' in data:
            producto.nombre = data['nombre']
        if 'descripcion' in data:
            producto.descripcion = data['descripcion']
        if 'precio' in data:
            producto.precio = data['precio']
        if 'stock_minimo' in data:
            producto.stock_minimo = data['stock_minimo']
        if 'codigo_barras' in data:
            producto.codigo_barras = data['codigo_barras']
        if 'proveedor' in data:
            producto.proveedor = data['proveedor']
        if 'activo' in data:
            producto.activo = data['activo']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Producto actualizado exitosamente',
            'producto': producto.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@productos_bp.route('/<int:producto_id>', methods=['DELETE'])
@jwt_required()
def delete_producto(producto_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = Usuario.query.get(current_user_id)
        
        if current_user.rol != 'admin':
            return jsonify({'error': 'No tienes permisos para eliminar productos'}), 403
        
        producto = Producto.query.get_or_404(producto_id)
        producto.activo = False
        
        db.session.commit()
        
        return jsonify({'message': 'Producto desactivado exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@productos_bp.route('/<int:producto_id>/stock', methods=['POST'])
@jwt_required()
def ajustar_stock(producto_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = Usuario.query.get(current_user_id)
        
        if current_user.rol != 'admin':
            return jsonify({'error': 'No tienes permisos para ajustar stock'}), 403
        
        producto = Producto.query.get_or_404(producto_id)
        data = request.get_json()
        
        tipo_movimiento = data.get('tipo_movimiento')  # 'entrada', 'salida', 'ajuste'
        cantidad = data.get('cantidad')
        motivo = data.get('motivo', '')
        
        if not tipo_movimiento or cantidad is None:
            return jsonify({'error': 'Tipo de movimiento y cantidad son requeridos'}), 400
        
        stock_anterior = producto.stock_actual
        
        if tipo_movimiento == 'entrada':
            producto.stock_actual += cantidad
        elif tipo_movimiento == 'salida':
            if producto.stock_actual < cantidad:
                return jsonify({'error': 'Stock insuficiente'}), 400
            producto.stock_actual -= cantidad
        elif tipo_movimiento == 'ajuste':
            producto.stock_actual = cantidad
        else:
            return jsonify({'error': 'Tipo de movimiento inválido'}), 400
        
        # Registrar en historial
        historial = HistorialStock(
            producto_id=producto.id,
            tipo_movimiento=tipo_movimiento,
            cantidad=cantidad if tipo_movimiento != 'ajuste' else cantidad - stock_anterior,
            stock_anterior=stock_anterior,
            stock_nuevo=producto.stock_actual,
            motivo=motivo,
            usuario_id=current_user_id
        )
        
        db.session.add(historial)
        db.session.commit()
        
        return jsonify({
            'message': 'Stock actualizado exitosamente',
            'producto': producto.to_dict(),
            'movimiento': historial.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@productos_bp.route('/<int:producto_id>/historial', methods=['GET'])
@jwt_required()
def get_historial_stock(producto_id):
    try:
        producto = Producto.query.get_or_404(producto_id)
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        historial = HistorialStock.query.filter_by(
            producto_id=producto_id
        ).order_by(
            HistorialStock.fecha_creacion.desc()
        ).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'producto': producto.to_dict(),
            'historial': [h.to_dict() for h in historial.items],
            'total': historial.total,
            'pages': historial.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@productos_bp.route('/bajo-stock', methods=['GET'])
@jwt_required()
def get_productos_bajo_stock():
    try:
        productos = Producto.query.filter(
            Producto.stock_actual <= Producto.stock_minimo,
            Producto.activo == True
        ).all()
        
        return jsonify({
            'productos_bajo_stock': [producto.to_dict() for producto in productos]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

