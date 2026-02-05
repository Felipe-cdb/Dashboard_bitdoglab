from flask import Blueprint, request, jsonify

hardware_bp = Blueprint("hardware", __name__)

# -----------------------------
# VISITAS
# -----------------------------
@hardware_bp.route("/visit", methods=["POST"])
def receive_visit():
    data = request.get_json(silent=True)

    if not data or "count" not in data:
        return jsonify({"error": "Payload inválido"}), 400

    visit_count = data["count"]

    print(f"[VISITA] Recebida: {visit_count}")

    return jsonify({
        "status": "ok",
        "received": "visit",
        "count": visit_count
    }), 200


# -----------------------------
# TEMPERATURA / UMIDADE
# -----------------------------
@hardware_bp.route("/environment", methods=["POST"])
def receive_environment():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Payload inválido"}), 400

    temperature = data.get("temperature")
    humidity = data.get("humidity")

    print(f"[AHT10] Temp={temperature}C  Umidade={humidity}%")

    return jsonify({
        "status": "ok",
        "received": "environment"
    }), 200


# -----------------------------
# COMPRA
# -----------------------------
@hardware_bp.route("/purchase", methods=["POST"])
def receive_purchase():
    data = request.get_json(silent=True)

    if not data or "product_id" not in data:
        return jsonify({"error": "Payload inválido"}), 400

    product_id = data["product_id"]

    print(f"[COMPRA] Produto: {product_id}")

    return jsonify({
        "status": "ok",
        "received": "purchase",
        "product_id": product_id
    }), 200
