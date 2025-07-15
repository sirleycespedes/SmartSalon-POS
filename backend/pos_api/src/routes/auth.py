from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.models.database import db, Usuario
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email y contraseña son requeridos'}), 400
        
        usuario = Usuario.query.filter_by(email=email, activo=True).first()
        
        if usuario and usuario.check_password(password):
            access_token = create_access_token(
                identity=usuario.id,
                expires_delta=timedelta(hours=24)
            )
            return jsonify({
                'access_token': access_token,
                'usuario': usuario.to_dict()
            }), 200
        else:
            return jsonify({'error': 'Credenciales inválidas'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/register', methods=['POST'])
@jwt_required()
def register():
    try:
        current_user_id = get_jwt_identity()
        current_user = Usuario.query.get(current_user_id)
        
        if current_user.rol != 'admin':
            return jsonify({'error': 'No tienes permisos para crear usuarios'}), 403
        
        data = request.get_json()
        nombre = data.get('nombre')
        email = data.get('email')
        password = data.get('password')
        rol = data.get('rol', 'empleado')
        
        if not all([nombre, email, password]):
            return jsonify({'error': 'Nombre, email y contraseña son requeridos'}), 400
        
        if Usuario.query.filter_by(email=email).first():
            return jsonify({'error': 'El email ya está registrado'}), 400
        
        usuario = Usuario(
            nombre=nombre,
            email=email,
            rol=rol
        )
        usuario.set_password(password)
        
        db.session.add(usuario)
        db.session.commit()
        
        return jsonify({
            'message': 'Usuario creado exitosamente',
            'usuario': usuario.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        current_user_id = get_jwt_identity()
        usuario = Usuario.query.get(current_user_id)
        
        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        return jsonify({'usuario': usuario.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    try:
        current_user_id = get_jwt_identity()
        usuario = Usuario.query.get(current_user_id)
        
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not all([current_password, new_password]):
            return jsonify({'error': 'Contraseña actual y nueva son requeridas'}), 400
        
        if not usuario.check_password(current_password):
            return jsonify({'error': 'Contraseña actual incorrecta'}), 400
        
        usuario.set_password(new_password)
        db.session.commit()
        
        return jsonify({'message': 'Contraseña actualizada exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

