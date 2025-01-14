import socket as s
from threading import Thread, Lock
from os import path

class MainServer():
    def __init__(self):
        self.listen_port = 1338
        self.TCP_server = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.TCP_server.bind(('', self.listen_port))
        self.TCP_server.listen(5)
        print(f'Lytter på port {self.listen_port} ...')

        self.is_running = True
        self.clients = []
        self.lock = Lock()

    def run(self):
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
        except Exception as e:
            print(f'Fejl: {e}')

    def return_file(self, sender_socket):
        filename = "Datanet.pdf"  # Sørg for, at filen findes i samme mappe som serveren
        if not path.exists(filename):
            print(f"Fil {filename} ikke fundet.")
            return

        length = path.getsize(filename)
        print(f'File length in bytes: {length}')

        # Send header
        file_header = f"FILE:{filename}\nLENGTH:{length}\n"
        sender_socket.send(file_header.encode('utf-8'))

        # Send filens data
        try:
            with open(filename, 'rb') as f:
                while chunk := f.read(2048):  # Læs filen i bidder af 2048 bytes
                    sender_socket.send(chunk)
            print(f"Fil {filename} sendt til klient.")
        except Exception as e:
            print(f'Fejl i return_file: {e}')

if __name__ == "__main__":
    server = MainServer()
    try:
        server.run()
    except KeyboardInterrupt:
        print("\nAfslutter server...")
        server.is_running = False