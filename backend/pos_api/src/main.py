import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src.models.database import db
from src.config import Config

# Importar blueprints
from src.routes.auth import auth_bp
from src.routes.clientes import clientes_bp
from src.routes.empleados import empleados_bp
from src.routes.servicios import servicios_bp
from src.routes.productos import productos_bp
from src.routes.citas import citas_bp
from src.routes.ventas import ventas_bp
from src.routes.reportes import reportes_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configuración
app.config.from_object(Config)

# Inicializar extensiones
CORS(app, origins=Config.CORS_ORIGINS)
jwt = JWTManager(app)
db.init_app(app)

# Registrar blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(clientes_bp, url_prefix='/api/clientes')
app.register_blueprint(empleados_bp, url_prefix='/api/empleados')
app.register_blueprint(servicios_bp, url_prefix='/api/servicios')
app.register_blueprint(productos_bp, url_prefix='/api/productos')
app.register_blueprint(citas_bp, url_prefix='/api/citas')
app.register_blueprint(ventas_bp, url_prefix='/api/ventas')
app.register_blueprint(reportes_bp, url_prefix='/api/reportes')

# Crear tablas si no existen
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

@app.route('/api/health', methods=['GET'])
def health_check():
    return {'status': 'OK', 'message': 'API funcionando correctamente'}, 200

@app.errorhandler(404)
def not_found(error):
    return {'error': 'Endpoint no encontrado'}, 404

@app.errorhandler(500)
def internal_error(error):
    return {'error': 'Error interno del servidor'}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

