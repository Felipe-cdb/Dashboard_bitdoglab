from app import create_app
from app.services.mdns_service import iniciar_servidor, encerrar_servidor
import tkinter as tk
import threading, webbrowser
from app import BASE_URL
from datetime import datetime
import sys
from tkinter import messagebox

flask_app = create_app()

def iniciar_flask(host, porta):
    """Inicia a aplicação Flask."""
    flask_app.run(debug=False, host=host, port=porta, use_reloader=False)

# === Inicialização do servidor ===
# Caso deseja Compartilhar||Ocutar o dns com outros dispositivos
# visível na rede-> USAR_MDNS=True
# oculto apenas maquina local -> USAR_MDNS=False

# --- Configurações ---
NOME_DNS = "zoyblock"
USAR_MDNS = False  # Mude para True para acessar de outros dispositivos na mesma rede
app = create_app()

# 1. Configura o servidor e define a URL global
try:
    host, porta, BASE_URL = iniciar_servidor(NOME_DNS, USAR_MDNS)
    import app
    app.BASE_URL = BASE_URL  # Atualiza o valor global em app
except RuntimeError as e:
    print(f"[ERRO] Falha ao iniciar servidor: {e}")
    # Mostrar mensagem amigável
    import tkinter.messagebox as messagebox
    tk.Tk().withdraw()
    messagebox.showerror("Erro ao iniciar servidor", "Não foi possível iniciar o servidor.\nTodas as portas já estão em uso.\nFeche outra instância ou libere uma porta.")
    sys.exit(1)

# 2. Inicia o Flask em uma thread separada para não bloquear a interface gráfica
def iniciar_interface():
    # Cria a interface Tkinter
    root = tk.Tk()
    root.title("ZoyBlock Servidor")
    root.geometry("380x200")
    root.resizable(False, False)
    root.eval('tk::PlaceWindow . center')  # Centraliza a janela

    label = tk.Label(
        root,
        text=f"Servidor rodando em:\n{BASE_URL}",
        font=("Segoe UI", 11),
        wraplength=280,
    )
    label.pack(pady=20)

    btn_abrir_navegador = tk.Button(
        root,
        text="Abrir no Navegador",
        command=lambda: webbrowser.open_new(BASE_URL),
    )
    btn_abrir_navegador.pack(pady=5)

    btn_sair = tk.Button(root, text="Sair", command=root.quit)
    btn_sair.pack(pady=5)

    root.protocol("WM_DELETE_WINDOW", root.quit)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n[INFO] Interrupção pelo teclado recebida.")
        root.quit()

if __name__ == "__main__":
    flask_thread = threading.Thread(target=iniciar_flask, args=(host, porta), daemon=True)
    flask_thread.start()

    # Inicia a interface Tkinter na thread principal
    iniciar_interface()