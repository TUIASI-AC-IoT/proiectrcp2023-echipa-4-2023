import socket
import threading

class Broker:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []

    def start(self):

        self.socket.bind((self.host, self.port))
        self.socket.listen(5)  # Waiting for conections

        print(f"Server is listening at {self.host}:{self.port}")
        while True:
            try:
                connection, address = self.socket.accept()
                print(f"Connection accepted from {address}")
            except KeyboardInterrupt:
                print("Server shutting down..")
                break

            try:
                thread = threading.Thread(target=self.handle_client, args=(connection, address))
                thread.start()
            except Exception as e:
                print(f"Failed to start thread: {e}")

    def handle_client(self, connection, address):

        self.clients.append((connection, address))
