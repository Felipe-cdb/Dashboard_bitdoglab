from flask import Blueprint, jsonify, render_template

server_bp = Blueprint("server", __name__)

# Página inicial do dashboard
@server_bp.route("/")
def dashboard():
    return render_template("dashboard/dashboard.html")

# Health check
@server_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "message": "Servidor Flask ativo"
    }), 200
