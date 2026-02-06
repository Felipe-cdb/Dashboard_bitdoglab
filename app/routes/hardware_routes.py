from flask import Blueprint, request, jsonify
from app.services.hardware_state import (
    register_visit,
    register_sales,
    update_environment
)

hardware_bp = Blueprint("hardware", __name__, url_prefix="/api")

@hardware_bp.route("/visit", methods=["POST"])
def receive_visit():
    data = request.get_json(silent=True) or {}

    if data.get("visit") != "ok":
        return jsonify({"error": "Payload inválido"}), 400

    register_visit()
    print("[VISITA] Registrada")

    return jsonify({"status": "ok"}), 200


@hardware_bp.route("/compra", methods=["POST"])
def receive_sales():
    data = request.get_json(silent=True) or {}

    if data.get("compra") != "ok":
        return jsonify({"error": "Payload inválido"}), 400

    register_sales()
    print("[COMPRA] Registrada")

    return jsonify({"status": "ok"}), 200


@hardware_bp.route("/temp", methods=["POST"])
def receive_temperature():
    data = request.get_json(silent=True)

    if not data or "temperature" not in data:
        return jsonify({"error": "Payload inválido"}), 400

    update_environment(
        float(data["temperature"]),
        float(data.get("humidity", 0))
    )

    print("[TEMP] Atualizada")

    return jsonify({"status": "ok"}), 200
