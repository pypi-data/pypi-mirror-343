# cliente.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import socket
import threading
import logging
import time
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox

# --- Logging DEBUG en el mismo directorio del script ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
LOG_FILE   = os.path.join(SCRIPT_DIR, "remote_client_debug.log")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    filename=LOG_FILE,
    filemode="w"
)
logger = logging.getLogger("RemoteClient")
logger.debug("=== Iniciando cliente (log en %s) ===", LOG_FILE)

DEFAULT_PORT   = 9999
HEADER_LEN     = 4      # 4 bytes big-endian para longitud
FRAME_INTERVAL = 0.2    # segundos entre frames

class RemoteClient:
    def __init__(self, master):
        self.master      = master
        self.stream_sock = None
        self.ctrl_sock   = None
        self.connected   = False
        self.photo       = None
        self.lock        = threading.Lock()

        logger.debug("Construyendo UI cliente")
        self._build_ui()

    def _build_ui(self):
        self.master.title("Cliente de Control Remoto")
        self.master.geometry("1024x768")

        main = ttk.Frame(self.master); main.pack(fill=tk.BOTH, expand=True)
        ctrl = ttk.LabelFrame(main, text="Conexión", width=250)
        ctrl.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        ttk.Label(ctrl, text="IP:").pack(anchor=tk.W, padx=5, pady=(5,0))
        self.ip_e = ttk.Entry(ctrl); self.ip_e.insert(0,"127.0.0.1"); self.ip_e.pack(fill=tk.X, padx=5)

        ttk.Label(ctrl, text="Puerto:").pack(anchor=tk.W, padx=5, pady=(5,0))
        self.pt_e = ttk.Entry(ctrl); self.pt_e.insert(0,str(DEFAULT_PORT)); self.pt_e.pack(fill=tk.X, padx=5)

        ttk.Separator(ctrl, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        self.btn_conn = ttk.Button(ctrl, text="Conectar",   command=self.connect)
        self.btn_conn.pack(fill=tk.X, padx=5, pady=(0,5))
        self.btn_disc = ttk.Button(ctrl, text="Desconectar", command=self.disconnect, state=tk.DISABLED)
        self.btn_disc.pack(fill=tk.X, padx=5)

        self.status = ttk.Label(ctrl, text="Desconectado", foreground="red")
        self.status.pack(anchor=tk.W, padx=5, pady=(10,0))

        view = ttk.Frame(main); view.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.canvas = tk.Canvas(view, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # eventos ratón
        self.canvas.bind("<Button-1>",        lambda e: self._send_ctrl(f"MOUSE:CLICK:{int(self.canvas.canvasx(e.x))}:{int(self.canvas.canvasy(e.y))}"))
        self.canvas.bind("<B1-Motion>",       lambda e: self._send_ctrl(f"MOUSE:MOVE:{int(self.canvas.canvasx(e.x))}:{int(self.canvas.canvasy(e.y))}"))
        self.canvas.bind("<ButtonRelease-1>", lambda e: self._send_ctrl(f"MOUSE:UP:{int(self.canvas.canvasx(e.x))}:{int(self.canvas.canvasy(e.y))}"))

        # teclado
        self.master.bind("<Key>", self._on_key)

        self.master.protocol("WM_DELETE_WINDOW", self.disconnect)

    def connect(self):
        ip   = self.ip_e.get().strip()
        try:
            port = int(self.pt_e.get())
        except ValueError:
            logger.error("Puerto inválido en GUI")
            return messagebox.showerror("Error", "Puerto inválido")

        logger.debug("Conectando a %s:%d (stream) y %d (control)", ip, port, port+1)
        try:
            # stream
            s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s1.connect((ip, port))
            self.stream_sock = s1
            # control
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s2.connect((ip, port + 1))
            self.ctrl_sock = s2

            self.connected = True
            self.btn_conn.config(state=tk.DISABLED)
            self.btn_disc.config(state=tk.NORMAL)
            self.status.config(text="Conectado", foreground="green")
            logger.info("Conexión establecida en ambos canales")

            threading.Thread(target=self._recv_stream, daemon=True).start()
        except Exception:
            logger.exception("Error al conectar")
            messagebox.showerror("Conexión fallida", "No se pudo conectar al servidor")

    def _recvall(self, sock, n):
        buf = b""
        while len(buf) < n:
            chunk = sock.recv(n - len(buf))
            if not chunk:
                logger.warning("recv devolvió 0 bytes")
                raise ConnectionError
            buf += chunk
        return buf

    def _recv_stream(self):
        logger.debug("Iniciando bucle de recepción de vídeo")
        try:
            while self.connected:
                header = self._recvall(self.stream_sock, HEADER_LEN)
                length = int.from_bytes(header, "big")
                logger.debug("Header recibido: %d bytes", length)
                data = self._recvall(self.stream_sock, length)
                logger.debug("Payload recibido, mostrando imagen")
                img   = Image.open(BytesIO(data))
                photo = ImageTk.PhotoImage(img)
                self.master.after_idle(lambda p=photo: self._update_canvas(p))
                time.sleep(FRAME_INTERVAL)
        except Exception:
            logger.exception("Error en bucle de recepción")
        finally:
            logger.debug("Recepción finalizada, desconectando")
            self.master.after_idle(self.disconnect)

    def _update_canvas(self, photo):
        self.photo = photo
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def _send_ctrl(self, msg):
        if not self.connected:
            logger.debug("Intento de enviar control desconectado")
            return
        full = msg + "\n"
        with self.lock:
            try:
                self.ctrl_sock.sendall(full.encode())
                logger.debug("Enviado control: %s", msg)
            except Exception:
                logger.exception("Error enviando comando de control")
                self.master.after_idle(self.disconnect)

    def _on_key(self, e):
        if not self.connected:
            return
        c  = e.char
        kc = e.keycode
        if c and ord(c) >= 32:
            cmd = f"KEYBOARD:{c}"
        else:
            spec = {9:"tab",13:"enter",27:"esc",37:"left",38:"up",39:"right",40:"down"}
            cmd = f"KEYBOARD:SPECIAL:{spec[kc]}" if kc in spec else ""
        if cmd:
            self._send_ctrl(cmd)

    def disconnect(self):
        if self.connected:
            logger.debug("Desconectando cliente")
            self.connected = False
            try:
                self.ctrl_sock.sendall(b"DISCONNECT\n")
            except:
                pass
            for s in (self.stream_sock, self.ctrl_sock):
                try: s.close()
                except: pass
            self.btn_conn.config(state=tk.NORMAL)
            self.btn_disc.config(state=tk.DISABLED)
            self.status.config(text="Desconectado", foreground="red")
            self.canvas.delete("all")
        else:
            logger.debug("Cerrando ventana cliente")
            self.master.destroy()

def main():
    root = tk.Tk()
    RemoteClient(root)
    root.mainloop()

if __name__ == "__main__":
    main()
