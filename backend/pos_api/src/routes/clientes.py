from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.database import db, Cliente, Usuario
from datetime import datetime

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/', methods=['GET'])
@jwt_required()
def get_clientes():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        activo = request.args.get('activo', 'true').lower() == 'true'
        
        query = Cliente.query.filter_by(activo=activo)
        
        if search:
            query = query.filter(
                db.or_(
                    Cliente.nombre.ilike(f'%{search}%'),
                    Cliente.apellido.ilike(f'%{search}%'),
                    Cliente.telefono.ilike(f'%{search}%'),
                    Cliente.email.ilike(f'%{search}%')
                )
            )
        
        clientes = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'clientes': [cliente.to_dict() for cliente in clientes.items],
            'total': clientes.total,
            'pages': clientes.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@clientes_bp.route('/<int:cliente_id>', methods=['GET'])
@jwt_required()
def get_cliente(cliente_id):
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        return jsonify({'cliente': cliente.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@clientes_bp.route('/', methods=['POST'])
@jwt_required()
def create_cliente():
    try:
        data = request.get_json()
        
        required_fields = ['nombre', 'apellido']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} es requerido'}), 400
        
        cliente = Cliente(
            nombre=data['nombre'],
            apellido=data['apellido'],
            telefono=data.get('telefono'),
            email=data.get('email'),
            direccion=data.get('direccion'),
            fecha_nacimiento=datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d').date() if data.get('fecha_nacimiento') else None,
            notas=data.get('notas')
        )
        
        db.session.add(cliente)
        db.session.commit()
        
        return jsonify({
            'message': 'Cliente creado exitosamente',
            'cliente': cliente.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@clientes_bp.route('/<int:cliente_id>', methods=['PUT'])
@jwt_required()
def update_cliente(cliente_id):
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        data = request.get_json()
        
        # Actualizar campos
        if 'nombre' in data:
            cliente.nombre = data['nombre']
        if 'apellido' in data:
            cliente.apellido = data['apellido']
        if 'telefono' in data:
            cliente.telefono = data['telefono']
        if 'email' in data:
            cliente.email = data['email']
        if 'direccion' in data:
            cliente.direccion = data['direccion']
        if 'fecha_nacimiento' in data:
            cliente.fecha_nacimiento = datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d').date() if data['fecha_nacimiento'] else None
        if 'notas' in data:
            cliente.notas = data['notas']
        if 'activo' in data:
            cliente.activo = data['activo']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Cliente actualizado exitosamente',
            'cliente': cliente.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@clientes_bp.route('/<int:cliente_id>', methods=['DELETE'])
@jwt_required()
def delete_cliente(cliente_id):
    try:
        current_user_id = get_jwt_identity()
        current_user = Usuario.query.get(current_user_id)
        
        if current_user.rol != 'admin':
            return jsonify({'error': 'No tienes permisos para eliminar clientes'}), 403
        
        cliente = Cliente.query.get_or_404(cliente_id)
        cliente.activo = False
        
        db.session.commit()
        
        return jsonify({'message': 'Cliente desactivado exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@clientes_bp.route('/<int:cliente_id>/historial', methods=['GET'])
@jwt_required()
def get_historial_cliente(cliente_id):
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        
        # Obtener citas del cliente
        citas = [cita.to_dict() for cita in cliente.citas]
        
        # Obtener ventas del cliente
        ventas = [venta.to_dict() for venta in cliente.ventas]
        
        return jsonify({
            'cliente': cliente.to_dict(),
            'citas': citas,
            'ventas': ventas
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

