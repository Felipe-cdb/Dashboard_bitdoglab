from flask import Blueprint, jsonify, render_template
from app.services.hardware_state import get_state

server_bp = Blueprint("server", __name__)

@server_bp.route("/")
def dashboard():
    return render_template("dashboard/dashboard.html")

@server_bp.route("/api/state", methods=["GET"])
def api_state():
    return jsonify(get_state()), 200
