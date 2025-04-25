# server.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import socket
import threading
import logging
import time
import ctypes
from io import BytesIO
from PIL import ImageGrab, ImageDraw
import tkinter as tk
from tkinter import ttk, messagebox
import keyboard
import mouse

# --- Logging DEBUG en el mismo directorio del script ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
LOG_FILE   = os.path.join(SCRIPT_DIR, "remote_server_debug.log")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    filename=LOG_FILE,
    filemode="w"
)
logger = logging.getLogger("RemoteServer")
logger.debug("=== Iniciando servidor (log en %s) ===", LOG_FILE)

DEFAULT_HOST   = "0.0.0.0"
DEFAULT_PORT   = 9999
FRAME_INTERVAL = 0.2    # segundos entre cuadros
HEADER_LEN     = 4      # 4 bytes big-endian para longitud

class RemoteServer:
    def __init__(self, host, port):
        self.host        = host
        self.stream_port = port
        self.ctrl_port   = port + 1
        self.stream_sock = None
        self.ctrl_sock   = None
        self.stream_conn = None
        self.ctrl_conn   = None
        self.running     = False
        logger.debug("Servidor init host=%s, stream_port=%d, ctrl_port=%d",
                     host, self.stream_port, self.ctrl_port)

    def start(self):
        logger.debug("Iniciando sockets")
        try:
            # socket de vídeo
            self.stream_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.stream_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.stream_sock.bind((self.host, self.stream_port))
            self.stream_sock.listen(1)
            logger.info("Stream escuchando en %s:%d", self.host, self.stream_port)

            # socket de control
            self.ctrl_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ctrl_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.ctrl_sock.bind((self.host, self.ctrl_port))
            self.ctrl_sock.listen(1)
            logger.info("Control escuchando en %s:%d", self.host, self.ctrl_port)

            self.running = True
            threading.Thread(target=self._accept, daemon=True).start()
            return True
        except Exception:
            logger.exception("Error al iniciar servidor")
            return False

    def _accept(self):
        logger.debug("Esperando conexión de stream...")
        self.stream_conn, addr_s = self.stream_sock.accept()
        logger.info("Stream conectado desde %s", addr_s)

        logger.debug("Esperando conexión de control...")
        self.ctrl_conn, addr_c = self.ctrl_sock.accept()
        logger.info("Control conectado desde %s", addr_c)

        threading.Thread(target=self._stream_loop, daemon=True).start()
        threading.Thread(target=self._control_loop, daemon=True).start()

    def _stream_loop(self):
        logger.debug("Iniciando bucle de streaming")
        self.stream_conn.settimeout(0.1)
        try:
            while self.running:
                # capturar pantalla
                img = ImageGrab.grab().convert("RGB")

                # dibujar cursor
                pt = ctypes.wintypes.POINT()
                ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
                draw = ImageDraw.Draw(img)
                s = 10
                draw.line((pt.x-s, pt.y, pt.x+s, pt.y), fill="red", width=2)
                draw.line((pt.x, pt.y-s, pt.x, pt.y+s), fill="red", width=2)

                # serializar JPEG
                buf    = BytesIO()
                img.save(buf, format="JPEG", quality=60)
                data   = buf.getvalue()
                header = len(data).to_bytes(HEADER_LEN, "big")

                try:
                    self.stream_conn.sendall(header + data)
                    logger.debug("Enviado frame de %d bytes", len(data))
                except Exception:
                    logger.exception("Error enviando frame, cerrando conexión de stream")
                    break

                time.sleep(FRAME_INTERVAL)

        except Exception:
            logger.exception("Error en bucle de streaming")
        finally:
            try: self.stream_conn.close()
            except: pass
            logger.debug("Stream loop finalizado")

    def _control_loop(self):
        logger.debug("Iniciando bucle de control")
        self.ctrl_conn.settimeout(0.1)
        try:
            while self.running:
                try:
                    data = self.ctrl_conn.recv(1024)
                except Exception:
                    continue
                if not data:
                    continue

                for line in data.decode(errors="ignore").splitlines():
                    cmd = line.strip()
                    if not cmd:
                        continue
                    logger.debug("Recibido comando: %s", cmd)
                    if cmd == "DISCONNECT":
                        logger.info("Cliente solicitó desconexión")
                        self.running = False
                        return
                    self._handle_cmd(cmd)

        except Exception:
            logger.exception("Error en bucle de control")
        finally:
            try: self.ctrl_conn.close()
            except: pass
            logger.debug("Control loop finalizado")

    def _handle_cmd(self, cmd):
        parts = cmd.split(":")
        if parts[0] == "MOUSE" and len(parts) == 4:
            _, action, xs, ys = parts
            x, y = int(xs), int(ys)
            logger.debug("Procesando MOUSE %s en %d,%d", action, x, y)
            try:
                # mover al punto
                mouse.move(x, y)
                # luego acción
                if action == "CLICK":    mouse.click()
                elif action == "DBLCLICK": mouse.double_click()
                elif action == "DOWN":     mouse.press()
                elif action == "UP":       mouse.release()
            except Exception:
                logger.exception("Error ejecutando comando de mouse")

        elif parts[0] == "KEYBOARD" and len(parts) >= 2:
            key = cmd.split(":", 1)[1]
            logger.debug("Procesando KEYBOARD %s", key)
            try:
                if key.startswith("SPECIAL:"):
                    keyboard.press_and_release(key.split("SPECIAL:")[1])
                else:
                    keyboard.write(key)
            except Exception:
                logger.exception("Error ejecutando comando de teclado")

        else:
            logger.warning("Comando inválido: %s", cmd)

    def stop(self):
        logger.debug("Deteniendo servidor")
        self.running = False
        for s in (self.stream_conn, self.ctrl_conn, self.stream_sock, self.ctrl_sock):
            try: s.close()
            except: pass
        logger.info("Servidor detenido")


def main():
    root = tk.Tk()
    root.title("Servidor de Control Remoto")

    frm = ttk.Frame(root, padding=10)
    frm.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frm, text="Host:").grid(row=0, column=0, sticky=tk.W, pady=5)
    host_e = ttk.Entry(frm); host_e.insert(0, DEFAULT_HOST); host_e.grid(row=0, column=1)

    ttk.Label(frm, text="Puerto:").grid(row=1, column=0, sticky=tk.W, pady=5)
    port_e = ttk.Entry(frm); port_e.insert(0, str(DEFAULT_PORT)); port_e.grid(row=1, column=1)

    status = ttk.Label(frm, text="Detenido", foreground="red")
    status.grid(row=2, column=0, columnspan=2, pady=10)

    server = RemoteServer(host_e.get(), int(port_e.get()))

    def start_srv():
        server.host        = host_e.get().strip()
        server.stream_port = int(port_e.get())
        server.ctrl_port   = server.stream_port + 1
        if server.start():
            status.config(text="Ejecutando", foreground="green")
        else:
            messagebox.showerror("Error", "No se pudo iniciar el servidor")

    def stop_srv():
        server.stop()
        status.config(text="Detenido", foreground="red")

    ttk.Button(frm, text="Iniciar", command=start_srv).grid(row=3, column=0, padx=5)
    ttk.Button(frm, text="Detener", command=stop_srv).grid(row=3, column=1, padx=5)

    root.protocol("WM_DELETE_WINDOW", lambda: (stop_srv(), root.destroy()))
    root.mainloop()


if __name__ == "__main__":
    main()
