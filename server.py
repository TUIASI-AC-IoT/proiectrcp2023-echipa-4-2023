# server.py
import socket
import threading
import time

class Server:

    def __init__(self, ip="127.0.0.1", port=5000):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.s.bind((ip, port))
        self.s.listen(5)
        self.clients = []
        self.server_on = False
        self.count = 0

    def timer(self, conn, addr):
        while True:
            time.sleep(1)
            self.count += 1
            if self.count >= 10:
                conn.close()

            timer_message = f"Timer for client {addr}: {self.count} seconds"
            self.gui_manager.update_chat_box(timer_message + '\n')

    def comm_thread(self, conn, addr):
        conn.send(b"Introduce your login credentials")
        name = str(conn.recv(1024), encoding='ascii')
        password = str(conn.recv(1024), encoding='ascii')
        if self.gui_manager.check_user(name, password):
            conn.send(b'ok')
            timer_thread = threading.Thread(target=self.timer, args=(conn, addr))
            timer_thread.start()

            while True:
                data = conn.recv(1024)
                self.count = 0
                message = str(addr) + ' Sent ' + str(data, encoding="ascii")
                self.gui_manager.update_chat_box(message + '\n')
                conn.sendall(bytes(message, encoding="ascii"))

            self.gui_manager.update_chat_box(f"The client {addr} has closed the connection\n")
            conn.close()
        else:
            self.gui_manager.update_chat_box(f"Wrong login credential from {addr}\n")
            conn.close()

    def start_server(self):
        self.gui_manager.update_chat_box('Asteapta conexiuni (oprire s cu Ctrl‐C)\n')
        while not self.server_on:
            try:
                conn, addr = self.s.accept()
                self.clients.append(conn)
            except:
                break
            self.gui_manager.update_chat_box(f'S‐a conectat clientul {addr}\n')
            try:
                threading.Thread(target=self.comm_thread, args=(conn, addr)).start()
            except self.server_on:
                conn.close()
                print("Eroare la pornirea thread‐ului")

    def quit_server(self):
        self.server_on = True
        for client in self.clients:
            client.close()
        self.gui_manager.destroy_gui()
        self.s.close()

    def set_gui_manager(self, gui_manager):
        self.gui_manager = gui_manager

    def run(self):
        server_thread = threading.Thread(target=self.start_server)
        server_thread.start()
