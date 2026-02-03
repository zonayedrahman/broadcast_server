import socket
import threading
import sys


class BroadcastClient:

    def __init__(self, host="127.0.0.1", port=9000):
        self.host = host
        self.port = port
        self.socket = None
        self.running = True


    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

        print(f"[CLIENT] Connected to {self.host}:{self.port}")

        receive_thread = threading.Thread(
            target=self.receive_loop,
            daemon=True,
        )
        receive_thread.start()

        self.send_loop()

    
    def send_loop(self):
        try:
            while self.running:
                message = input()
                if not message:
                    continue

                self.socket.sendall(message.encode())
        except (KeyboardInterrupt, EOFError):
            print("\n[CLIENT] Disconnecting")
        finally:
            self.shutdown()


    
    def receive_loop(self):
        try:
            while self.running:
                data = self.socket.recv(1024)
                if not data:
                    print("[CLIENT] Server disconnected")
                    break

                print(data.decode().strip())
        except ConnectionError:
            pass
        finally:
            self.running = False

    def shutdown(self):
        self.running = False
        try:
            self.socket.close()
        except Exception:
            pass
        sys.exit(0)

if __name__ == "__main__":
    client = BroadcastClient()
    client.connect()