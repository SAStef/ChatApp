import socket as s
from threading import Thread
import signal
import sys

class MainServer():
    def __init__(self, ):
        self.listen_port = 1337
        self.TCP_server = s.socket(s.AF_INET, s.SOCK_STREAM)
        # s.AF_INET                indikerer IPv4
        # s.SOCK_STREAM            indikerer TCP
        self.TCP_server.bind(('', self.listen_port))
        self.TCP_server.listen(5)
        print(f'Lytter på port {self.listen_port}...')

        self.running = True

    def run(self, ):
        try:
            while self.running:
                # Accepterer en indgående TCP forbindelse
                self.client_socket, self.client_address = self.TCP_server.accept()
                print(f"Bruger tilsluttet via TCP: {self.client_address}")

                # Starter en ny tråd til at håndtere forbindelse med klienten

                connect_thread = Thread(target=self.handleClient, args=(self.client_socket,))
                connect_thread.start()

        except Exception as e:
            print(f"Python error: {e}")

        finally:
            self.TCP_server.close()

    def handleClient(self, client_socket):
        try:
            while self.running:
                client_data = client_socket.recv(2048)
                if not client_data:                        # Hvis brugeren terminerer TCP forbindelsen
                    print(f'Bruger {self.client_address} har forladt chatten')
                    break
                print(f"Modtaget: {client_data.decode('utf-8')}")
        except Exception as e:
            print(f"Fejl på klientsiden")

class ChatSession():
    def __init__(self, p):
        self.parent = p

def signal_handler():
    print("\nServeren lukkes ned...")
    server.running = False
    sys.exit(0)

if __name__ == "__main__":
    server = MainServer()
    
    try:
        server.run()
    except KeyboardInterrupt:
        signal()