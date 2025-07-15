from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.database import db, Empleado, Usuario
from datetime import datetime

empleados_bp = Blueprint('empleados', __name__)

@empleados_bp.route('/', methods=['GET'])
@jwt_required()
def get_empleados():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        activo = request.args.get('activo', 'true').lower() == 'true'
        
        query = Empleado.query.filter_by(activo=activo)
        
        if search:
            query = query.filter(
                db.or_(
                    Empleado.nombre.ilike(f'%{search}%'),
                    Empleado.apellido.ilike(f'%{search}%'),
                    Empleado.telefono.ilike(f'%{search}%')
                )
            )
        
        empleados = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'empleados': [empleado.to_dict() for empleado in empleados.items],
            'total': empleados.total,
            'pages': empleados.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@empleados_bp.route('/<int:empleado_id>', methods=['GET'])
@jwt_required()
def get_empleado(empleado_id):
    try:
        empleado = Empleado.query.get_or_404(empleado_id)
        return jsonify({'empleado': empleado.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@empleados_bp.route('/', methods=['POST'])
@jwt_required()
def create_empleado():
    try:
        current_user_id = get_jwt_identity()
        current_user = Usuario.query.get(current_user_id)
        
        if current_user.rol != 'admin':
            return jsonify({'error': 'No tienes permisos para crear empleados'}), 403
        
        data = request.get_json()
        
        required_fields = ['nombre', 'apellido']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} es requerido'}), 400
        
        empleado = Empleado(
            usuario_id=data.get('usuario_id'),
            nombre=data['nombre'],
            apellido=data['apellido'],
            telefono=data.get('telefono'),
            direccion=data.get('direccion'),
            fecha_contratacion=datetime.strptime(data['fecha_contratacion'], '%Y-%m-%d').date() if data.get('fecha_contratacion') else None,
            salario_base=data.get('salario_base'),
            comision_porcentaje=data.get('comision_porcentaje', 0)
        )
        
        db.session.add(empleado)
        db.session.commit()
        
        return jsonify({
            'message': 'Empleado creado exitosamente',
            'empleado': empleado.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@empleados_bp.route('/<int:empleado_id>', methods=['PUT'])
@jwt_required()
def update_empleado(empleado_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = Usuario.query.get(current_user_id)
        
        if current_user.rol != 'admin':
            return jsonify({'error': 'No tienes permisos para actualizar empleados'}), 403
        
        empleado = Empleado.query.get_or_404(empleado_id)
        data = request.get_json()
        
        # Actualizar campos
        if 'nombre' in data:
            empleado.nombre = data['nombre']
        if 'apellido' in data:
            empleado.apellido = data['apellido']
        if 'telefono' in data:
            empleado.telefono = data['telefono']
        if 'direccion' in data:
            empleado.direccion = data['direccion']
        if 'fecha_contratacion' in data:
            empleado.fecha_contratacion = datetime.strptime(data['fecha_contratacion'], '%Y-%m-%d').date() if data['fecha_contratacion'] else None
        if 'salario_base' in data:
            empleado.salario_base = data['salario_base']
        if 'comision_porcentaje' in data:
            empleado.comision_porcentaje = data['comision_porcentaje']
        if 'activo' in data:
            empleado.activo = data['activo']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Empleado actualizado exitosamente',
            'empleado': empleado.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@empleados_bp.route('/<int:empleado_id>', methods=['DELETE'])
@jwt_required()
def delete_empleado(empleado_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = Usuario.query.get(current_user_id)
        
        if current_user.rol != 'admin':
            return jsonify({'error': 'No tienes permisos para eliminar empleados'}), 403
        
        empleado = Empleado.query.get_or_404(empleado_id)
        empleado.activo = False
        
        db.session.commit()
        
        return jsonify({'message': 'Empleado desactivado exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@empleados_bp.route('/<int:empleado_id>/citas', methods=['GET'])
@jwt_required()
def get_citas_empleado(empleado_id):
    try:
        empleado = Empleado.query.get_or_404(empleado_id)
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        
        query = empleado.citas
        
        if fecha_inicio:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            query = [cita for cita in query if cita.fecha_hora >= fecha_inicio]
        
        if fecha_fin:
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
            query = [cita for cita in query if cita.fecha_hora <= fecha_fin]
        
        citas = [cita.to_dict() for cita in query]
        
        return jsonify({
            'empleado': empleado.to_dict(),
            'citas': citas
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@empleados_bp.route('/<int:empleado_id>/ventas', methods=['GET'])
@jwt_required()
def get_ventas_empleado(empleado_id):
    try:
        empleado = Empleado.query.get_or_404(empleado_id)
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        
        query = empleado.ventas
        
        if fecha_inicio:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            query = [venta for venta in query if venta.fecha_venta >= fecha_inicio]
        
        if fecha_fin:
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
            query = [venta for venta in query if venta.fecha_venta <= fecha_fin]
        
        ventas = [venta.to_dict() for venta in query]
        
        # Calcular estadísticas
        total_ventas = sum(float(venta['total']) for venta in ventas)
        total_comisiones = sum(float(venta['total']) * (float(empleado.comision_porcentaje) / 100) for venta in ventas)
        
        return jsonify({
            'empleado': empleado.to_dict(),
            'ventas': ventas,
            'estadisticas': {
                'total_ventas': total_ventas,
                'total_comisiones': total_comisiones,
                'cantidad_ventas': len(ventas)
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

