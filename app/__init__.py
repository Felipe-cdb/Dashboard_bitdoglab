from flask import Flask
from app.db import db

def create_app():
    app = Flask(__name__)

    # =========================
    # CONFIG BANCO DE DADOS
    # =========================
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # =========================
    # REGISTRO DE MODELS
    # =========================
    from app.models import visit, sale, environment

    # =========================
    # REGISTRO DE ROTAS
    # =========================
    from app.routes.server_routes import server_bp
    from app.routes.hardware_routes import hardware_bp

    app.register_blueprint(server_bp)
    app.register_blueprint(hardware_bp)

    # =========================
    # CRIA BANCO AUTOMATICAMENTE
    # =========================
    with app.app_context():
        db.create_all()

    return app
