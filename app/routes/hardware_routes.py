from flask import Blueprint, request, jsonify

# Prefixo único para hardware (fortemente recomendado)
hardware_bp = Blueprint("hardware", __name__, url_prefix="/api")

# -----------------------------
# VISITA (evento)
# -----------------------------
@hardware_bp.route("/visit", methods=["POST"])
def receive_visit():
    data = request.get_json(silent=True) or {}

    # Apenas evento, sem contador
    if data.get("visit") != "ok":
        return jsonify({"error": "Payload inválido"}), 400

    print("[VISITA] Evento recebido")

    return jsonify({
        "status": "ok",
        "event": "visit"
    }), 200


# -----------------------------
# TEMPERATURA / UMIDADE
# -----------------------------
@hardware_bp.route("/temp", methods=["POST"])
def receive_temperature():
    data = request.get_json(silent=True)

    if not data or "temperature" not in data:
        return jsonify({"error": "Payload inválido"}), 400

    temperature = float(data["temperature"])
    humidity = data.get("humidity")

    print(f"[TEMP] {temperature}°C | Umidade={humidity}%")

    return jsonify({
        "status": "ok",
        "event": "temperature"
    }), 200


# -----------------------------
# COMPRA (evento)
# -----------------------------
@hardware_bp.route("/compra", methods=["POST"])
def receive_purchase():
    data = request.get_json(silent=True) or {}

    # Evento simples
    if data.get("compra") != "ok":
        return jsonify({"error": "Payload inválido"}), 400

    print("[COMPRA] Evento recebido")

    return jsonify({
        "status": "ok",
        "event": "compra"
    }), 200
