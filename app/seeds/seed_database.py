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
    # Usamos datetime.now() para pegar a hora local do sistema
    now = datetime.now()

    for day in range(days):
        base_day = now - timedelta(days=day)
        visits_today = random.randint(40, max_per_day)

        for _ in range(visits_today):
            # Garante que a hora randômica não ultrapasse a hora atual se for o dia 0 (hoje)
            max_hour = now.hour if day == 0 else 22
            min_hour = 8
            
            # Ajuste caso o script rode antes das 8 da manhã
            actual_max = max(min_hour, max_hour)
            
            created_at = base_day.replace(
                hour=random.randint(min_hour, actual_max),
                minute=random.randint(0, 59)
            )
            
            # Trava final de segurança: se gerou algo no futuro, traz para o agora
            if created_at > now:
                created_at = now

            db.session.add(Visit(created_at=created_at))
    db.session.commit()

def seed_sales(days=7, max_per_day=30):
    print("[SEED] Criando vendas...")
    now = datetime.now()

    for day in range(days):
        base_day = now - timedelta(days=day)
        sales_today = random.randint(10, max_per_day)

        for _ in range(sales_today):
            max_hour = now.hour if day == 0 else 21
            min_hour = 9
            actual_max = max(min_hour, max_hour)

            created_at = base_day.replace(
                hour=random.randint(min_hour, actual_max),
                minute=random.randint(0, 59)
            )

            if created_at > now:
                created_at = now

            db.session.add(Sale(created_at=created_at))
    db.session.commit()

def seed_environment(hours=24):
    print("[SEED] Criando dados ambientais...")
    # Ponto chave: agora começamos do 'now' e subtraímos o índice
    now = datetime.now()
    total_minutes = hours * 60

    temperature = random.uniform(24, 27)
    humidity = random.uniform(50, 65)

    for i in range(total_minutes):
        temperature += random.uniform(-0.05, 0.05)
        humidity += random.uniform(-0.1, 0.1)

        temperature = max(22, min(30, temperature))
        humidity = max(40, min(80, humidity))

        # Subtraímos i do momento atual. Se i=0 (primeiro registro), é exatamente agora.
        # Se i=1, é um minuto atrás. Isso garante que NADA fique no futuro.
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