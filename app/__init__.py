from flask import Flask

def create_app():
    app = Flask(__name__)

    # =========================
    # REGISTRO DE ROTAS
    # =========================
    from app.routes.hardware_routes import hardware_bp
    from app.routes.server_routes import server_bp

    app.register_blueprint(hardware_bp)
    app.register_blueprint(server_bp)

    return app
