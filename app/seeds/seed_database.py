import random
from datetime import datetime, timedelta

from app import create_app
from app.db import db
from app.models import Visit, Sale, EnvironmentLog

app = create_app()


def clear_database():
    print("[SEED] Limpando banco...")
    db.session.query(Visit).delete()
    db.session.query(Sale).delete()
    db.session.query(EnvironmentLog).delete()
    db.session.commit()


def seed_visits(days=7, max_per_day=120):
    print("[SEED] Criando visitas...")
    now = datetime.utcnow()

    for day in range(days):
        base_day = now - timedelta(days=day)
        visits_today = random.randint(30, max_per_day)

        for _ in range(visits_today):
            created_at = base_day.replace(
                hour=random.randint(8, 22),
                minute=random.randint(0, 59),
                second=random.randint(0, 59)
            )
            db.session.add(Visit(created_at=created_at))

    db.session.commit()


def seed_sales(days=7, max_per_day=25):
    print("[SEED] Criando vendas...")
    now = datetime.utcnow()

    for day in range(days):
        base_day = now - timedelta(days=day)
        sales_today = random.randint(5, max_per_day)

        for _ in range(sales_today):
            created_at = base_day.replace(
                hour=random.randint(9, 21),
                minute=random.randint(0, 59),
                second=random.randint(0, 59)
            )
            db.session.add(Sale(created_at=created_at))

    db.session.commit()


def seed_environment(hours=24):
    print("[SEED] Criando dados ambientais...")
    now = datetime.utcnow()
    total_minutes = hours * 60

    temperature = random.uniform(24, 27)
    humidity = random.uniform(50, 65)

    for i in range(total_minutes):
        temperature += random.uniform(-0.05, 0.05)
        humidity += random.uniform(-0.1, 0.1)

        temperature = max(22, min(30, temperature))
        humidity = max(40, min(80, humidity))

        created_at = now - timedelta(minutes=i)

        db.session.add(
            EnvironmentLog(
                temperature=round(temperature, 2),
                humidity=round(humidity, 2),
                created_at=created_at
            )
        )

    db.session.commit()


def run_seed():
    with app.app_context():
        clear_database()
        seed_visits()
        seed_sales()
        seed_environment()
        print("[SEED] Banco populado com sucesso!")


if __name__ == "__main__":
    run_seed()
