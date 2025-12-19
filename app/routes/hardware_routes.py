from flask import Blueprint, request
from app.services.serial_service import listar_portas, conectar, desconectar, atualizar_baudrate, BAUDRATE

hardware = Blueprint("hardware", __name__)

@hardware.route("/listar_portas")
def listar():
    portas = listar_portas()
    return portas

@hardware.route("/conectar", methods=["POST"])
def rota_conectar():
    dados = request.get_json()
    porta = dados.get("porta")
    if conectar(porta):
        return f"Conectado à porta {porta}"
    else:
        return "Erro ao conectar", 500
    
@hardware.route("/desconectar", methods=["POST"])
def rota_desconectar():
    if desconectar():
        return "Desconectado com sucesso"
    else:
        return "Erro ao desconectar", 500
    

@hardware.route("/definir_placa", methods=["POST"])
def definir_placa():
    global placa_selecionada
    dados = request.get_json()
    placa = dados.get("placa", "arduino")
    placa_selecionada = placa
    print(f"[INFO] Placa selecionada: {placa_selecionada}")
    return "Placa atualizada"


@hardware.route("/atualiza_baudrate", methods=["POST"])
def rota_baudrate():
    data = request.get_json()
    index = int(data.get('velo'))
    # Lista de baudrates possíveis (indexado)
    BAUDRATES_DISPONIVEIS = [9600, 19200, 38400, 57600, 115200]
    baudrate = BAUDRATES_DISPONIVEIS[index] 
 
    if atualizar_baudrate(baudrate):
        return f"Conectado à velocidade {baudrate}"
    else:
        return "Erro ao conectar", 500
    