from flask import Blueprint, jsonify, render_template
from app.models import Visit, Sale, EnvironmentLog
from app.db import db
from sqlalchemy import func
from datetime import datetime, timedelta
from sqlalchemy import func

server_bp = Blueprint("server", __name__)


@server_bp.route("/")
def dashboard():
    return render_template("dashboard.html")


@server_bp.route("/analytics")
def analytics():
    return render_template("analytics.html")


@server_bp.route("/environment")
def environment():
    return render_template("environment.html")


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

@server_bp.route("/api/dashboard/kpis")
def dashboard_kpis():
    visits = db.session.query(func.count(Visit.id)).scalar()
    sales = db.session.query(func.count(Sale.id)).scalar()

    conversion = (sales / visits * 100) if visits else 0

    avg_temp = db.session.query(func.avg(EnvironmentLog.temperature)).scalar()

    return jsonify({
        "visits": visits,
        "sales": sales,
        "conversion": round(conversion, 2),
        "avg_temperature": round(avg_temp, 1) if avg_temp else None
    })

@server_bp.route("/api/dashboard/hourly")
def dashboard_hourly():
    today = datetime.utcnow().date()

    visits = dict(
        db.session.query(
            func.strftime("%H", Visit.created_at),
            func.count(Visit.id)
        )
        .filter(func.date(Visit.created_at) == today)
        .group_by(func.strftime("%H", Visit.created_at))
        .all()
    )

    sales = dict(
        db.session.query(
            func.strftime("%H", Sale.created_at),
            func.count(Sale.id)
        )
        .filter(func.date(Sale.created_at) == today)
        .group_by(func.strftime("%H", Sale.created_at))
        .all()
    )

    temps = dict(
        db.session.query(
            func.strftime("%H", EnvironmentLog.created_at),
            func.avg(EnvironmentLog.temperature)
        )
        .filter(func.date(EnvironmentLog.created_at) == today)
        .group_by(func.strftime("%H", EnvironmentLog.created_at))
        .all()
    )

    return jsonify({
        "visits": visits,
        "sales": sales,
        "temperature": temps
    })

@server_bp.route("/api/environment/summary")
def environment_summary():
    today = datetime.utcnow().date()

    # Temperatura média, máxima e umidade média
    avg_temp = db.session.query(func.avg(EnvironmentLog.temperature)).scalar()
    max_temp = db.session.query(func.max(EnvironmentLog.temperature)).scalar()
    avg_hum = db.session.query(func.avg(EnvironmentLog.humidity)).scalar()

    # Temperatura e umidade por hora
    hourly = db.session.query(
        func.strftime("%H", EnvironmentLog.created_at).label("hour"),
        func.avg(EnvironmentLog.temperature).label("temperature"),
        func.avg(EnvironmentLog.humidity).label("humidity")
    ).filter(
        func.date(EnvironmentLog.created_at) == today
    ).group_by("hour").all()

    hours = {}
    for h, t, u in hourly:
        hours[h] = {
            "temperature": round(t, 2),
            "humidity": round(u, 2)
        }

    return jsonify({
        "avg_temp": round(avg_temp, 2) if avg_temp else None,
        "max_temp": round(max_temp, 2) if max_temp else None,
        "avg_humidity": round(avg_hum, 2) if avg_hum else None,
        "hourly": hours
    })
