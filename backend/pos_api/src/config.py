import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'pos-barberia-secret-key-2024'
    
    # Configuración de PostgreSQL
    POSTGRES_USER = os.environ.get('POSTGRES_USER') or 'pos_user'
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD') or 'pos_password'
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST') or 'localhost'
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT') or '5432'
    POSTGRES_DB = os.environ.get('POSTGRES_DB') or 'pos_barberia'
    
    SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración CORS
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5173', '*']
    
    # Configuración de paginación
    ITEMS_PER_PAGE = 20
    
    # Configuración de JWT (si se implementa autenticación)
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-pos-barberia'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hora en segundos

