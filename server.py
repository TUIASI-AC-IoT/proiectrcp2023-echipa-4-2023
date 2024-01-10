# server.py
import socket
import threading
import time

import encoder
from decoder import decoder
from encoder import *
from database import Database


class Server:

    def __init__(self, ip=socket.gethostbyname(socket.gethostname()), port=1883):
        print(ip)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.s.bind((ip, port))
        self.s.listen(5)
        self.clients = []
        self.server_on = False
        self.inactivity_timer = 0
        self.keep_alive_count = 0
        self.decoder = decoder()
        self.db = Database()
        self.user_sesion = []
        self.qos1 = []
        self.qos2 = []
        self.topics = []
        # self.encode=encoder()

    def keep_alive_timer(self, conn, addr, keep_alive):
        while True:
            time.sleep(1)
            self.keep_alive_count += 1
            if self.keep_alive_count == keep_alive:
                conn.send(generate_pingresp())
                self.keep_alive_count = 0

    def comm_thread(self, conn, addr):
        val = conn.recv(1024)
        print("This is the connect packet", val)
        username, password, keep_alive = (decoder.decode_connect(val))
        if self.db.check_user(username, password):
            conn.send(generate_connack_packet())
            timer_thread = threading.Thread(target=self.keep_alive_timer, args=(conn, addr, keep_alive))
            timer_thread.start()
            data = conn.recv(1024)
            print("This is the publish packet", data)

            topic, qos = decoder.decode_publish_packet(data)
            conn.send(generate_suback_packet(63276,qos))
            self.topics.append(topic)
            print("Qos is =", qos)
            print(keep_alive)
            if qos == 0:
                while True:
                    data = conn.recv(1024)
                    time.sleep(1)
                    self.keep_alive_count = 0
                    print(data)
                    self.user_sesion.append(data)
                    if data != b'\xc0\x00' and self.keep_alive_count == keep_alive - 1:
                        print("Last Will")

            if qos == 1:
                while True:
                    data = conn.recv(1024)
                    print(data)
                    time.sleep(1)
                    self.keep_alive_count = 0
                    self.qos1.append(data)
                    self.user_sesion.append(data)
                    if data != b'\xc0\x00' and self.keep_alive_count == keep_alive:
                        self.gui_manager.update_chat_box(data + '\n')
                        print("Last Will")
                        conn.close()
                    if data != b'\xc0\x00':
                        conn.send(generate_puback())
            if qos == 2:
                while True:
                    data = conn.recv(1024)
                    print(data)
                    time.sleep(1)
                    self.keep_alive_count = 0
                    self.qos2.append(data)
                    self.user_sesion.append(data)
                    if self.keep_alive_count == 60 and data != b'\xc0\x00':
                        print("Last Will")
                        conn.close()
                    conn.send(generate_pubrec_packet(456))
                    time.sleep(1)
                    data = conn.recv(1024)
                    conn.send(generate_pubcomp_packet(789))

        else:
            self.gui_manager.update_chat_box(f"Wrong login credential from {addr}\n")

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

    def print_qos_messages(self):
        self.gui_manager.update_chat_box(f"This are the qos 1 messages: {self.qos1}\n")
        self.gui_manager.update_chat_box(f"This are the qos 2 messages: {self.qos2}\n")

    def visualize_mesages(self):
        self.gui_manager.update_chat_box(f"This are the last 10 mesajes publicated:{self.user_sesion[-10:]}\n")

    def visualize_topics(self):
        self.gui_manager.update_chat_box(f"This are the topics that the clients subscribed:{self.topics}\n")

    def set_gui_manager(self, gui_manager):
        self.gui_manager = gui_manager

    def run(self):
        server_thread = threading.Thread(target=self.start_server)
        server_thread.start()
