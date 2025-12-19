import socket, atexit
from zeroconf import Zeroconf, ServiceInfo
from app import BASE_URL
import threading, webbrowser
import requests, sys

zeroconf = None

# === Função para registrar serviço mDNS ===
def registrar_mdns(nome, porta):
    """Registra o serviço na rede local usando mDNS/Zeroconf."""
    try:
        global zeroconf
        ip = socket.gethostbyname(socket.gethostname())
        ip_bytes = socket.inet_aton(ip)
        info = ServiceInfo(
            "_http._tcp.local.",
            f"{nome}._http._tcp.local.",
            addresses=[ip_bytes],
            port=porta,
            properties={},
            server=f"{nome}.local.",
        )
        zeroconf = Zeroconf()
        zeroconf.register_service(info, allow_name_change=True)
        print(f"[INFO] Serviço mDNS registrado como http://{nome}.local:{porta}")

        # Função para garantir que o serviço seja desregistrado ao sair
        def encerrar_mdns():
            print("[INFO] Encerrando e desregistrando serviço mDNS...")
            zeroconf.unregister_service(info)
            zeroconf.close()

        atexit.register(encerrar_mdns)

    except Exception as e:
        print(f"[ERRO] Falha ao registrar o serviço mDNS: {e}")

# === Função para encontrar porta livre ===
def encontrar_porta_livre(inicio=5000, fim=5010):
    """Verifica um intervalo de portas e retorna a primeira que estiver livre."""
    for porta in range(inicio, fim + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("localhost", porta)) != 0:
                return porta
    raise RuntimeError("Nenhuma porta livre encontrada no intervalo especificado.")

# Abri a url diretamente no navegador
def open_browser():
    """Abre a URL base do servidor no navegador padrão."""
    if BASE_URL:
        webbrowser.open_new(BASE_URL)
    else:
        print("[ERRO] URL base não definida. Não é possível abrir o navegador.")

# === Funções de controle do servidor ===
# Argumentos:
# nomeDNS apelida a url deixando mais amigavel
# usar_mdns em true, torna a url visivel a outros disposivos e false não compartilha essa url
def iniciar_servidor(nomeDNS, usar_mdns=True):
    """
    Inicia o servidor, define a URL base global e retorna a porta escolhida.
    """
    global BASE_URL
    porta_escolhida = encontrar_porta_livre()

    if usar_mdns:
        host = "0.0.0.0" # Escuta em todas as interfaces de rede
        registrar_mdns(nomeDNS, porta_escolhida)
        BASE_URL = f"http://{nomeDNS}.local:{porta_escolhida}"
    else:
        host = "127.0.0.1" # Escuta apenas localmente
        BASE_URL = f"http://127.0.0.1:{porta_escolhida}"

    # Abre o navegador após um pequeno atraso para o servidor iniciar
    threading.Timer(3.5, open_browser).start()
    print(f"[INFO] Servidor iniciado. Acesse em: {BASE_URL}")

    # Retorna o host e a porta para o Flask
    return host, porta_escolhida, BASE_URL

def encerrar_servidor():
    """Envia uma requisição para a rota /shutdown para fechar o servidor."""
    print("[INFO] Tentando encerrar o servidor...")
    try:
        requests.post(f'{BASE_URL}/shutdown', timeout=1)
    except requests.exceptions.RequestException:
        # É comum ocorrer um erro aqui, pois o servidor desliga antes de responder.
        # Isso é esperado e pode ser ignorado.
        pass
    finally:
        # Garante que o processo principal (com a janela Tkinter) seja encerrado.
        sys.exit()