from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app():
    load_dotenv('.env')
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    with app.app_context():
        from .models import Usuario, Carro, Rota, Local, Atividade
        db.create_all()

    from app.controllers.LoginController import login_bp
    from app.controllers.carroController import carro_bp
    from app.controllers.localController import local_bp
    from app.controllers.rotaController import rota_bp
    from app.controllers.usuarioController import usuario_bp
    from app.controllers.atividadeController import atividade_bp

    app.register_blueprint(login_bp, url_prefix='/api')
    app.register_blueprint(carro_bp, url_prefix='/api')
    app.register_blueprint(local_bp, url_prefix='/api')
    app.register_blueprint(rota_bp, url_prefix='/api')
    app.register_blueprint(usuario_bp, url_prefix='/api')
    app.register_blueprint(atividade_bp, url_prefix='/api')
    
    if not app.debug:
        handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
        handler.setLevel(logging.ERROR)
        app.logger.addHandler(handler)   

#    for rule in app.url_map.iter_rules():
#        print(f"Endpoint: {rule.endpoint}, URL: {rule}") 

    return app
