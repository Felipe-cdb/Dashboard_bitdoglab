# run.py
import signal
import sys
import threading
import webbrowser
import time

from app import create_app
from app.services.mdns_service import (
    encontrar_porta_livre,
    registrar_mdns,
    encerrar_mdns,
)

# =========================
# CONFIGURAÇÕES
# =========================
NOME_DNS = "mydashboard"
USAR_MDNS = True

app = create_app()

# =========================
# ENCERRAMENTO LIMPO
# =========================
def shutdown_handler(signum, frame):
    print("\n[INFO] Encerrando servidor...")
    encerrar_mdns()
    print("[INFO] Servidor finalizado corretamente.")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

# =========================
# ABERTURA DO NAVEGADOR
# =========================
def abrir_navegador(url):
    time.sleep(1)  # garante que o Flask subiu
    webbrowser.open(url)

# =========================
# MAIN
# =========================
def main():
    try:
        porta = encontrar_porta_livre()
    except RuntimeError as e:
        print(f"[ERRO] {e}")
        sys.exit(1)

    if USAR_MDNS:
        host = "0.0.0.0"
        registrar_mdns(NOME_DNS, porta)
        base_url = f"http://{NOME_DNS}.local:{porta}"
    else:
        host = "127.0.0.1"
        base_url = f"http://127.0.0.1:{porta}"

    print(f"[INFO] Servidor iniciado em: {base_url}")
    app.config["BASE_URL"] = base_url

    # Thread separada para abrir navegador
    threading.Thread(
        target=abrir_navegador,
        args=(base_url,),
        daemon=True
    ).start()

    app.run(
        host=host,
        port=porta,
        debug=False,
        use_reloader=False
    )

if __name__ == "__main__":
    main()
