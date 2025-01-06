import os
from flask import Flask
from flask_migrate import Migrate, upgrade
from flask_cors import CORS
from flask_jwt_extended import JWTManager


from .model import init_db
from .security import user_datastore, security
from application.initial_scripts.initiallize_data import initial_data_loader, add_admin_user
from .config import DevelopmentConfig,ProductionConfig


def cors_setup(app):
    CORS(app)
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,PATCH,OPTIONS')
        return response
    
    return app

    
env = os.getenv("ENV", "production")



admin_email = os.getenv('ADMIN_EMAIL')
admin_password =  os.getenv('ADMIN_PASSWORD') 
admin_name =  os.getenv('ADMIN_NAME')
    
    


def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()
    
    with app.app_context():
        from . import blueprint
    
    if os.getenv('ENV') == 'development':
        app.config.from_object(DevelopmentConfig)
    if os.getenv('ENV') == 'production':
        app.config.from_object(ProductionConfig)
    
    
    db = init_db()
    db.init_app(app)
    
    cors_setup(app)

    JWTManager(app)
    
    security.init_app(app, user_datastore)
    
    with app.app_context():
        db.create_all()
        initial_data_loader()
        add_admin_user(admin_name,admin_email, admin_password)
    
    migrate = Migrate(app, db)
    
    # with app.app_context():
    #     upgrade()
    
        
    return app