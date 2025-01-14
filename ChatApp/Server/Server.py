import socket as s
from threading import Thread, Lock
import signal
import sys
from ChatSession import ChatSession, signal_handler
import os
from os import path

class MainServer:
    def __init__(self):
        self.listen_port = 1337
        self.TCP_server = s.socket(s.AF_INET, s.SOCK_STREAM)

        self.TCP_server.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)

        self.TCP_server.bind(('', self.listen_port))
        self.TCP_server.listen(5)
        self.chat_session = ChatSession(self) 
        print(f'Lytter på port {self.listen_port}...')
        self.running = True

        self.clients = []
        self.lock = Lock()

    def run(self):
        try:
            while self.running:
               
                client_socket, client_address = self.TCP_server.accept()
                print(f"Bruger tilsluttet via TCP: {client_address}")

                with self.lock:
                    self.clients.append(client_socket)

                connect_thread = Thread(target=self.handleClient, args=(client_socket, client_address))
                connect_thread.start()

        except Exception as e:
            print(f"Python error: {e}")

        finally:
            self.stop()
            # self.TCP_server.close()

    def handleClient(self, client_socket, client_address):
        try:
            while self.running:
                client_data = client_socket.recv(2048)
                if not client_data: 
                    print(f'{client_address[0]} har forladt chatten')
                    break
                
                decoded_message = client_data.decode('utf-8')

                if decoded_message.startswith('FILE:'):
                    self.send_file(decoded_message, client_socket)
                else:
                    self.BroadcastMessage(decoded_message, client_socket)
                    print(f"Fra: {client_address[0]}: {decoded_message}")

        except Exception:
            print(f"Fejl på klientsiden")

        finally:
            with self.lock:
                if client_socket in self.clients:
                    self.clients.remove(client_socket)
            client_socket.close()

    def BroadcastMessage(self, message, sender_socket):
        with self.lock:
            for client in self.clients:
                if client != sender_socket:
                    try:
                        client.sendall(message.encode('utf-8'))
                    except Exception as e:
                        print(f"Fejl ved udsendelse til klienten: {e}")
                        self.clients.remove(client)

    def send_file(self, file_header, client_socket):
        header_lines = file_header.split("\n")
        file_name = header_lines[0].split(":")[1].strip()
        file_length = int(header_lines[1].split(":")[1].strip())

        temp_dir = "./tmp"
        if not path.exists(temp_dir):
            os.makedirs(temp_dir)

        file_path = path.join(temp_dir, file_name)
        print(f'Gemmer midlertidig fil "{file_name}" inden videre transmission...')

        with open(file_path, 'wb') as f:
            bytes_recieved = 0
            while bytes_recieved < file_length:
                buffer = client_socket.recv(2048)
                if not buffer:
                    break
                f.write(buffer)
                bytes_recieved += len(buffer)
        
        # Now broadcasting this temporary file
        new_file_header = f'FILE: {file_name}\nLENGTH: {file_length}\n'

        with self.lock:
            for client in self.clients:
                if client != client_socket:
                    try:
                        client.send(new_file_header.encode('utf-8'))
                        with open(file_path, 'rb') as f:
                            while buffer := f.read(2048):
                                client.send(buffer)
                        print(f'File {file_name} has been broadcasted to the group chat')
                    
                    except Exception as e:
                        print(f"Fejl ved udsendelse til klienten: {e}")
                        self.clients.remove(client)

    def stop(self, ):
        print(f'Lukker serveren via MainServer.stop()...')
        self.running = False

        with self.lock:
            for client in self.clients:
                client.close()
            
        self.clients.clear()
        self.TCP_server.close()

if __name__ == "__main__":
    server = MainServer()
   
    signal.signal(signal.SIGINT, lambda _, __: signal_handler(server))

    try:
        server.run()
    except KeyboardInterrupt:
        print("\nAfslutter server...")
        server.running = False
        sys.exit(0)                                # Dræber hele serverprocessen
