from app.db import db
from datetime import datetime

class EnvironmentLog(db.Model):
    __tablename__ = "environment_logs"

    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
