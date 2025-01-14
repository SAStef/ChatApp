import socket as s
from threading import Thread, Lock
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QTimer
import signal
import sys
from os import path

class MainServer():
    def __init__(self, ):
        
        self.listen_port = 1338
        self.TCP_server = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.TCP_server.bind(('',self.listen_port))
        self.TCP_server.listen(5)
        print(f'Lytter på port {self.listen_port} ...')

        self.is_running = True

        self.clients = []
        self.lock = Lock()

    def run(self, ):
        try:
            while self.is_running:
                client_socket, client_address = self.TCP_server.accept()
                
                print(f'Bruger tilsluttet via TCP {client_address}')

                with self.lock:
                    self.clients.append(client_socket)

                t = Thread(target=self.handle_client, args=(client_socket, client_address))
                t.start()

        except Exception as e:
            print(f'Fejl: {e}')

    def handle_client(self, client_socket, client_address):
        try:
            while self.is_running:
                client_data = client_socket.recv(2048)
                if not client_data:
                    print(f'Forbindelse afbrudt med {client_address}')
                    break

                print(f'Binær besked: {client_data}, Datatype: {type(client_data)}')
                decoded_message = client_data.decode('utf-8')
                print(f'Fra {client_address[0]}: {decoded_message}')

                self.return_file(client_socket)
                # self.broadcast_message(client_data, client_socket)

        except Exception as e:
            print(f'Fejl: {e}')

    def return_file(self, sender_socket):
        filename = "Datanet.pdf"
        if not path.exists(filename):
            print(f'File {filename} does not exist')
        
        length = path.getsize(filename)
        print(f'File length in bytes: {length}')

        file_header = f"FILE: {filename}\nLENGTH: {length}\n"
        sender_socket.send(file_header.encode('UTF-8'))

        try:
            with open(filename, 'rb') as f:
                while chunk := f.read(2048):
                    sender_socket.send(chunk)
            print(f'File {filename} sent to client')
            
        except Exception as e:
            print(f'Fejl i return_file: {e}')
        




    # def broadcast_message(self, message, sender_socket):
    #     with self.lock:
    #         for client in self.clients:
    #             if client != sender_socket:
    #                 try:
    #                     client.sendall(message)
    #                 except Exception as e:
    #                     print(f'Fejl ved broadcastbesked: {e}')



if __name__ == "__main__":
    server = MainServer()
   
    # signal.signal(signal.SIGINT, lambda _, __: signal_handler(server))

    try:
        server.run()
    except KeyboardInterrupt:
        print("\nAfslutter server...")
        server.running = False
        sys.exit(0)                                # Dræber hele serverprocessen
