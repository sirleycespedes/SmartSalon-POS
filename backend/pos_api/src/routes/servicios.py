from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.database import db, Servicio, Usuario

servicios_bp = Blueprint('servicios', __name__)

@servicios_bp.route('/', methods=['GET'])
@jwt_required()
def get_servicios():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        activo = request.args.get('activo', 'true').lower() == 'true'
        
        query = Servicio.query.filter_by(activo=activo)
        
        if search:
            query = query.filter(
                db.or_(
                    Servicio.nombre.ilike(f'%{search}%'),
                    Servicio.descripcion.ilike(f'%{search}%')
                )
            )
        
        servicios = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'servicios': [servicio.to_dict() for servicio in servicios.items],
            'total': servicios.total,
            'pages': servicios.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@servicios_bp.route('/<int:servicio_id>', methods=['GET'])
@jwt_required()
def get_servicio(servicio_id):
    try:
        servicio = Servicio.query.get_or_404(servicio_id)
        return jsonify({'servicio': servicio.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@servicios_bp.route('/', methods=['POST'])
@jwt_required()
def create_servicio():
    try:
        current_user_id = get_jwt_identity()
        current_user = Usuario.query.get(current_user_id)
        
        if current_user.rol != 'admin':
            return jsonify({'error': 'No tienes permisos para crear servicios'}), 403
        
        data = request.get_json()
        
        required_fields = ['nombre', 'precio', 'duracion_minutos']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} es requerido'}), 400
        
        servicio = Servicio(
            nombre=data['nombre'],
            descripcion=data.get('descripcion'),
            precio=data['precio'],
            duracion_minutos=data['duracion_minutos']
        )
        
        db.session.add(servicio)
        db.session.commit()
        
        return jsonify({
            'message': 'Servicio creado exitosamente',
            'servicio': servicio.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@servicios_bp.route('/<int:servicio_id>', methods=['PUT'])
@jwt_required()
def update_servicio(servicio_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = Usuario.query.get(current_user_id)
        
        if current_user.rol != 'admin':
            return jsonify({'error': 'No tienes permisos para actualizar servicios'}), 403
        
        servicio = Servicio.query.get_or_404(servicio_id)
        data = request.get_json()
        
        # Actualizar campos
        if 'nombre' in data:
            servicio.nombre = data['nombre']
        if 'descripcion' in data:
            servicio.descripcion = data['descripcion']
        if 'precio' in data:
            servicio.precio = data['precio']
        if 'duracion_minutos' in data:
            servicio.duracion_minutos = data['duracion_minutos']
        if 'activo' in data:
            servicio.activo = data['activo']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Servicio actualizado exitosamente',
            'servicio': servicio.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@servicios_bp.route('/<int:servicio_id>', methods=['DELETE'])
@jwt_required()
def delete_servicio(servicio_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = Usuario.query.get(current_user_id)
        
        if current_user.rol != 'admin':
            return jsonify({'error': 'No tienes permisos para eliminar servicios'}), 403
        
        servicio = Servicio.query.get_or_404(servicio_id)
        servicio.activo = False
        
        db.session.commit()
        
        return jsonify({'message': 'Servicio desactivado exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@servicios_bp.route('/populares', methods=['GET'])
@jwt_required()
def get_servicios_populares():
    try:
        # Query para obtener servicios más vendidos
        from sqlalchemy import func
        from src.models.database import VentaServicio
        
        servicios_populares = db.session.query(
            Servicio,
            func.count(VentaServicio.id).label('total_ventas'),
            func.sum(VentaServicio.subtotal).label('total_ingresos')
        ).join(
            VentaServicio, Servicio.id == VentaServicio.servicio_id
        ).group_by(
            Servicio.id
        ).order_by(
            func.count(VentaServicio.id).desc()
        ).limit(10).all()
        
        resultado = []
        for servicio, total_ventas, total_ingresos in servicios_populares:
            servicio_dict = servicio.to_dict()
            servicio_dict['total_ventas'] = total_ventas
            servicio_dict['total_ingresos'] = float(total_ingresos) if total_ingresos else 0
            resultado.append(servicio_dict)
        
        return jsonify({'servicios_populares': resultado}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

