import socket
import threading


class BroadcastServer:

    def __init__(self, host="127.0.0.1", port=9000):

        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.clients_lock = threading.Lock()


        
    
    def start(self):
        '''Start the broadcast server, and start listening for connections'''

        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # rebinding to same port if reconnecting
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)

        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"[SERVER] Listening on {self.host}:{self.port}")

        try:
            self.accept_loop()
        except KeyboardInterrupt:
            print("\n[SERVER] Keyboard interrupt received")
            self.shutdown()


    def accept_loop(self):
        '''Accept incoming client connection'''

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"[SERVER] Client connected: {client_address}")

            with self.clients_lock:
                self.clients.append(client_socket)

            thread = threading.Thread(
                target=self.handle_client,
                args=(client_socket, client_address),
                daemon=True,
            )
            thread.start()

    def handle_client(self, client_socket, client_address):
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break 

                message = data.decode().strip()
                print(f"[{client_address}] {message}")

                self.broadcast(message, sender_socket=client_socket)

        except ConnectionError:
            pass
        finally:
            print(f"[SERVER] Client disconnected: {client_address}")
            self.remove_client(client_socket)
            client_socket.close()


    def broadcast(self, message, sender_socket):
        data = (message + "\n").encode()

        with self.clients_lock:
            for client in list(self.clients):
                if client is sender_socket:
                    continue
                try:
                    client.sendall(data)
                except BrokenPipeError:
                    self.remove_client(client)

    def remove_client(self, client_socket):
        with self.clients_lock:
            if client_socket in self.clients:
                self.clients.remove(client_socket)

    def shutdown(self):
        print("[SERVER] Shutting down")

        with self.clients_lock:
            for client in self.clients:
                client.close()
            self.clients.clear()

        if self.server_socket:
            self.server_socket.close()
