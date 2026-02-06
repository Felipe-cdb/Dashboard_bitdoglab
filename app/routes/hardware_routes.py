from flask import Blueprint, request, jsonify
from app.services.hardware_repository import (
    save_visit,
    save_sale,
    save_environment
)

hardware_bp = Blueprint("hardware", __name__, url_prefix="/api")


@hardware_bp.route("/visit", methods=["POST"])
def receive_visit():
    data = request.get_json(silent=True) or {}

    if data.get("visit") != "ok":
        return jsonify({"error": "Payload inválido"}), 400

    save_visit()
    print("[VISIT] Persistida no banco")

    return jsonify({"status": "ok"}), 200


@hardware_bp.route("/sale", methods=["POST"])
def receive_sale():
    data = request.get_json(silent=True) or {}

    if data.get("sale") != "ok":
        return jsonify({"error": "Payload inválido"}), 400

    save_sale()
    print("[SALE] Persistida no banco")

    return jsonify({"status": "ok"}), 200


@hardware_bp.route("/temp", methods=["POST"])
def receive_temperature():
    data = request.get_json(silent=True)

    if not data or "temperature" not in data:
        return jsonify({"error": "Payload inválido"}), 400

    save_environment(
        temperature=float(data["temperature"]),
        humidity=float(data.get("humidity", 0))
    )

    print("[ENV] Temperatura e umidade persistidas")

    return jsonify({"status": "ok"}), 200
