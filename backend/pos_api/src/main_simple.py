from flask import Flask, jsonify, request
from flask_cors import CORS
import bcrypt

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

# Datos de prueba en memoria
users = [
    {
        "id": 1,
        "nombre": "Administrador",
        "email": "admin@barberia.com",
        "password_hash": bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        "rol": "administrador",
        "activo": True
    }
]

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "OK",
        "message": "API funcionando correctamente"
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # Buscar usuario
    user = next((u for u in users if u['email'] == email), None)
    
    if not user:
        return jsonify({"error": "Credenciales inválidas"}), 400
    
    # Verificar contraseña
    if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        return jsonify({"error": "Credenciales inválidas"}), 400
    
    # Simular token JWT
    token = "fake-jwt-token-for-demo"
    
    return jsonify({
        "access_token": token,
        "usuario": {
            "id": user["id"],
            "nombre": user["nombre"],
            "email": user["email"],
            "rol": user["rol"]
        }
    })

@app.route('/api/auth/me', methods=['GET'])
def get_current_user():
    # Simular usuario autenticado
    return jsonify({
        "usuario": {
            "id": 1,
            "nombre": "Administrador",
            "email": "admin@barberia.com",
            "rol": "administrador",
            "activo": True
        }
    })

@app.route('/api/reportes/dashboard', methods=['GET'])
def dashboard():
    return jsonify({
        "resumen_dia": {
            "ingresos": 450.00,
            "ventas": 12,
            "citas": 8,
            "citas_por_estado": {
                "programada": 3,
                "en_proceso": 1,
                "completada": 4
            }
        },
        "estadisticas_generales": {
            "clientes_activos": 156,
            "productos_bajo_stock": 3,
            "empleados_activos": 4
        },
        "servicios_populares": [
            {"nombre": "Corte de Cabello", "total_ventas": 25},
            {"nombre": "Barba", "total_ventas": 18},
            {"nombre": "Lavado", "total_ventas": 12}
        ],
        "ingresos_semanales": [
            {"semana": "2025-W01", "ingresos": 2200.00},
            {"semana": "2025-W02", "ingresos": 2500.00},
            {"semana": "2025-W03", "ingresos": 2800.00}
        ]
    })

@app.route('/api/clientes', methods=['GET'])
def get_clientes():
    clientes_demo = [
        {
            "id": 1,
            "nombre": "Juan",
            "apellido": "Pérez",
            "telefono": "+1234567890",
            "email": "juan@email.com",
            "direccion": "Calle 123",
            "fecha_nacimiento": "1990-05-15",
            "notas": "Cliente frecuente",
            "activo": True,
            "fecha_creacion": "2025-01-15T10:00:00"
        },
        {
            "id": 2,
            "nombre": "María",
            "apellido": "García",
            "telefono": "+0987654321",
            "email": "maria@email.com",
            "direccion": "Avenida 456",
            "fecha_nacimiento": "1985-08-20",
            "notas": "Prefiere cortes modernos",
            "activo": True,
            "fecha_creacion": "2025-01-10T14:30:00"
        }
    ]
    
    return jsonify({
        "clientes": clientes_demo,
        "total": len(clientes_demo)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

