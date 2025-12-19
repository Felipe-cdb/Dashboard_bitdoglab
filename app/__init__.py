from flask import Flask
import os
import sys

# === Variável Global para a URL Base do Servidor ===
BASE_URL = ""

# === Caminho absoluto para compatibilidade com PyInstaller ===
def caminho_absoluto(caminho_relativo):
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, caminho_relativo)

def create_app():
    app = Flask(
        __name__,
        template_folder=caminho_absoluto("app/templates"),
        static_folder=caminho_absoluto("app/static")
    )

    from app.routes.server_routes import server
    from app.routes.hardware_routes import hardware
    from app.routes.wifi_routes import wifi
    from app.routes.pin_routes import pin

    app.register_blueprint(server)
    app.register_blueprint(hardware)
    app.register_blueprint(wifi)
    app.register_blueprint(pin)

    return app