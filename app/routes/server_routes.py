from flask import Blueprint, render_template, request
from app.services.mdns_service import  encerrar_servidor
from app.services.blockly_service import executar_codigo
from flask import render_template

server = Blueprint("server", __name__)

@server.route("/")
def index():
    return render_template("index.html")

@server.route("/executar", methods=["POST"])
def executar():
    dados = request.get_json()
    return executar_codigo(dados)

@server.route("/shutdown", methods=["POST"])
def shutdown():
    return encerrar_servidor()