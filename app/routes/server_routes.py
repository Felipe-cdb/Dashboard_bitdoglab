from flask import Blueprint, jsonify, render_template
from app.models import Visit, Sale, EnvironmentLog
from app.db import db
from sqlalchemy import func

server_bp = Blueprint("server", __name__)


@server_bp.route("/")
def dashboard():
    return render_template("dashboard/dashboard.html")


@server_bp.route("/api/state", methods=["GET"])
def api_state():
    visits = db.session.query(func.count(Visit.id)).scalar()
    sales = db.session.query(func.count(Sale.id)).scalar()

    last_env = (
        db.session.query(EnvironmentLog)
        .order_by(EnvironmentLog.created_at.desc())
        .first()
    )

    return jsonify({
        "visits": visits,
        "sales": sales,
        "temperature": last_env.temperature if last_env else None,
        "humidity": last_env.humidity if last_env else None
    }), 200
