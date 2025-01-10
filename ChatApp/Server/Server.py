import socket as s
from threading import Thread
import signal
from ChatSession import ChatSession, signal_handler

class MainServer:
    def __init__(self):
        self.listen_port = 1337
        self.TCP_server = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.TCP_server.bind(('', self.listen_port))
        self.TCP_server.listen(5)
        self.chat_session = ChatSession(self) 
        print(f'Lytter på port {self.listen_port}...')
        self.running = True

    def run(self):
        try:
            while self.running:
               
                client_socket, client_address = self.TCP_server.accept()
                print(f"Bruger tilsluttet via TCP: {client_address}")

               
                connect_thread = Thread(target=self.handleClient, args=(client_socket,))
                connect_thread.start()

        except Exception as e:
            print(f"Python error: {e}")

        finally:
            self.TCP_server.close()

    def handleClient(self, client_socket):
        try:
            while self.running:
                client_data = client_socket.recv(2048)
                if not client_data: 
                    print('Bruger har forladt chatten')
                    break
                print(f"Modtaget: {client_data.decode('utf-8')}")
        except Exception:
            print(f"Fejl på klientsiden")
        finally:
            client_socket.close()

if __name__ == "__main__":
    server = MainServer()
   
    signal.signal(signal.SIGINT, lambda _, __: signal_handler(server))

    try:
        server.run()
    except KeyboardInterrupt:
        print("\nAfslutter server...")
