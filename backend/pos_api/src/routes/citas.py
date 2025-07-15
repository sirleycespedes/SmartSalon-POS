from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.database import db, Cita, CitaServicio, Cliente, Empleado, Servicio
from datetime import datetime, timedelta

citas_bp = Blueprint('citas', __name__)

@citas_bp.route('/', methods=['GET'])
@jwt_required()
def get_citas():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        empleado_id = request.args.get('empleado_id', type=int)
        cliente_id = request.args.get('cliente_id', type=int)
        estado = request.args.get('estado')
        
        query = Cita.query
        
        if fecha_inicio:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            query = query.filter(Cita.fecha_hora >= fecha_inicio)
        
        if fecha_fin:
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d') + timedelta(days=1)
            query = query.filter(Cita.fecha_hora < fecha_fin)
        
        if empleado_id:
            query = query.filter(Cita.empleado_id == empleado_id)
        
        if cliente_id:
            query = query.filter(Cita.cliente_id == cliente_id)
        
        if estado:
            query = query.filter(Cita.estado == estado)
        
        citas = query.order_by(Cita.fecha_hora).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'citas': [cita.to_dict() for cita in citas.items],
            'total': citas.total,
            'pages': citas.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@citas_bp.route('/<int:cita_id>', methods=['GET'])
@jwt_required()
def get_cita(cita_id):
    try:
        cita = Cita.query.get_or_404(cita_id)
        return jsonify({'cita': cita.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@citas_bp.route('/', methods=['POST'])
@jwt_required()
def create_cita():
    try:
        data = request.get_json()
        
        required_fields = ['cliente_id', 'fecha_hora', 'servicios']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} es requerido'}), 400
        
        # Validar cliente
        cliente = Cliente.query.get(data['cliente_id'])
        if not cliente:
            return jsonify({'error': 'Cliente no encontrado'}), 404
        
        # Validar empleado si se proporciona
        empleado = None
        if data.get('empleado_id'):
            empleado = Empleado.query.get(data['empleado_id'])
            if not empleado:
                return jsonify({'error': 'Empleado no encontrado'}), 404
        
        # Calcular duración total
        servicios_ids = data['servicios']
        servicios = Servicio.query.filter(Servicio.id.in_(servicios_ids)).all()
        duracion_total = sum(servicio.duracion_minutos for servicio in servicios)
        
        # Crear cita
        cita = Cita(
            cliente_id=data['cliente_id'],
            empleado_id=data.get('empleado_id'),
            fecha_hora=datetime.fromisoformat(data['fecha_hora'].replace('Z', '+00:00')),
            duracion_minutos=duracion_total,
            estado=data.get('estado', 'programada'),
            notas=data.get('notas')
        )
        
        db.session.add(cita)
        db.session.flush()  # Para obtener el ID de la cita
        
        # Agregar servicios a la cita
        for servicio in servicios:
            cita_servicio = CitaServicio(
                cita_id=cita.id,
                servicio_id=servicio.id,
                precio=servicio.precio
            )
            db.session.add(cita_servicio)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Cita creada exitosamente',
            'cita': cita.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@citas_bp.route('/<int:cita_id>', methods=['PUT'])
@jwt_required()
def update_cita(cita_id):
    try:
        cita = Cita.query.get_or_404(cita_id)
        data = request.get_json()
        
        # Actualizar campos básicos
        if 'empleado_id' in data:
            if data['empleado_id']:
                empleado = Empleado.query.get(data['empleado_id'])
                if not empleado:
                    return jsonify({'error': 'Empleado no encontrado'}), 404
            cita.empleado_id = data['empleado_id']
        
        if 'fecha_hora' in data:
            cita.fecha_hora = datetime.fromisoformat(data['fecha_hora'].replace('Z', '+00:00'))
        
        if 'estado' in data:
            cita.estado = data['estado']
        
        if 'notas' in data:
            cita.notas = data['notas']
        
        # Actualizar servicios si se proporcionan
        if 'servicios' in data:
            # Eliminar servicios existentes
            CitaServicio.query.filter_by(cita_id=cita.id).delete()
            
            # Agregar nuevos servicios
            servicios_ids = data['servicios']
            servicios = Servicio.query.filter(Servicio.id.in_(servicios_ids)).all()
            duracion_total = sum(servicio.duracion_minutos for servicio in servicios)
            
            for servicio in servicios:
                cita_servicio = CitaServicio(
                    cita_id=cita.id,
                    servicio_id=servicio.id,
                    precio=servicio.precio
                )
                db.session.add(cita_servicio)
            
            cita.duracion_minutos = duracion_total
        
        db.session.commit()
        
        return jsonify({
            'message': 'Cita actualizada exitosamente',
            'cita': cita.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@citas_bp.route('/<int:cita_id>', methods=['DELETE'])
@jwt_required()
def delete_cita(cita_id):
    try:
        cita = Cita.query.get_or_404(cita_id)
        cita.estado = 'cancelada'
        
        db.session.commit()
        
        return jsonify({'message': 'Cita cancelada exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@citas_bp.route('/disponibilidad', methods=['GET'])
@jwt_required()
def check_disponibilidad():
    try:
        fecha = request.args.get('fecha')  # YYYY-MM-DD
        empleado_id = request.args.get('empleado_id', type=int)
        duracion = request.args.get('duracion', 30, type=int)
        
        if not fecha:
            return jsonify({'error': 'Fecha es requerida'}), 400
        
        fecha_inicio = datetime.strptime(fecha, '%Y-%m-%d')
        fecha_fin = fecha_inicio + timedelta(days=1)
        
        # Obtener citas del día
        query = Cita.query.filter(
            Cita.fecha_hora >= fecha_inicio,
            Cita.fecha_hora < fecha_fin,
            Cita.estado.in_(['programada', 'confirmada', 'en_proceso'])
        )
        
        if empleado_id:
            query = query.filter(Cita.empleado_id == empleado_id)
        
        citas_ocupadas = query.all()
        
        # Generar horarios disponibles (ejemplo: 9:00 AM a 6:00 PM)
        horarios_disponibles = []
        hora_inicio = fecha_inicio.replace(hour=9, minute=0)
        hora_fin = fecha_inicio.replace(hour=18, minute=0)
        
        hora_actual = hora_inicio
        while hora_actual < hora_fin:
            # Verificar si el horario está ocupado
            ocupado = False
            for cita in citas_ocupadas:
                cita_fin = cita.fecha_hora + timedelta(minutes=cita.duracion_minutos)
                slot_fin = hora_actual + timedelta(minutes=duracion)
                
                if (hora_actual < cita_fin and slot_fin > cita.fecha_hora):
                    ocupado = True
                    break
            
            if not ocupado:
                horarios_disponibles.append(hora_actual.strftime('%H:%M'))
            
            hora_actual += timedelta(minutes=30)  # Intervalos de 30 minutos
        
        return jsonify({
            'fecha': fecha,
            'empleado_id': empleado_id,
            'horarios_disponibles': horarios_disponibles
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@citas_bp.route('/calendario', methods=['GET'])
@jwt_required()
def get_calendario():
    try:
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        empleado_id = request.args.get('empleado_id', type=int)
        
        if not fecha_inicio or not fecha_fin:
            return jsonify({'error': 'Fecha de inicio y fin son requeridas'}), 400
        
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d') + timedelta(days=1)
        
        query = Cita.query.filter(
            Cita.fecha_hora >= fecha_inicio,
            Cita.fecha_hora < fecha_fin
        )
        
        if empleado_id:
            query = query.filter(Cita.empleado_id == empleado_id)
        
        citas = query.order_by(Cita.fecha_hora).all()
        
        # Formatear para calendario
        eventos = []
        for cita in citas:
            eventos.append({
                'id': cita.id,
                'title': f"{cita.cliente.nombre} {cita.cliente.apellido}",
                'start': cita.fecha_hora.isoformat(),
                'end': (cita.fecha_hora + timedelta(minutes=cita.duracion_minutos)).isoformat(),
                'color': {
                    'programada': '#3498db',
                    'confirmada': '#2ecc71',
                    'en_proceso': '#f39c12',
                    'completada': '#27ae60',
                    'cancelada': '#e74c3c'
                }.get(cita.estado, '#3498db'),
                'extendedProps': {
                    'cliente': cita.cliente.to_dict(),
                    'empleado': cita.empleado.to_dict() if cita.empleado else None,
                    'servicios': [cs.to_dict() for cs in cita.servicios],
                    'estado': cita.estado,
                    'notas': cita.notas
                }
            })
        
        return jsonify({'eventos': eventos}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

