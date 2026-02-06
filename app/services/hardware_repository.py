from app.db import db
from app.models import Visit, Sale, EnvironmentLog


# -----------------------------
# VISITS
# -----------------------------
def save_visit():
    visit = Visit()
    db.session.add(visit)
    db.session.commit()


# -----------------------------
# SALES
# -----------------------------
def save_sale():
    sale = Sale()
    db.session.add(sale)
    db.session.commit()


# -----------------------------
# ENVIRONMENT
# -----------------------------
def save_environment(temperature: float, humidity: float):
    log = EnvironmentLog(
        temperature=temperature,
        humidity=humidity
    )
    db.session.add(log)
    db.session.commit()
