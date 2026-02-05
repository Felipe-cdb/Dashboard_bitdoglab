# app/services/mdns_service.py
import socket, atexit
from zeroconf import Zeroconf, ServiceInfo

_zeroconf = None
_service_info = None

def encontrar_porta_livre(inicio=5000, fim=5010):
    for porta in range(inicio, fim + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("localhost", porta)) != 0:
                return porta
    raise RuntimeError("Nenhuma porta livre encontrada")

def registrar_mdns(nome, porta):
    global _zeroconf, _service_info

    ip = socket.gethostbyname(socket.gethostname())
    _service_info = ServiceInfo(
        "_http._tcp.local.",
        f"{nome}._http._tcp.local.",
        addresses=[socket.inet_aton(ip)],
        port=porta,
        properties={},
        server=f"{nome}.local.",
    )

    _zeroconf = Zeroconf()
    _zeroconf.register_service(_service_info)
    print(f"[mDNS] Serviço registrado: http://{nome}.local:{porta}")

def encerrar_mdns():
    global _zeroconf, _service_info
    if _zeroconf and _service_info:
        print("[mDNS] Encerrando serviço mDNS...")
        _zeroconf.unregister_service(_service_info)
        _zeroconf.close()
        _zeroconf = None
        _service_info = None
