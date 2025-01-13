import socket as s
from threading import Thread, Lock
import sys
import os
from os import path

class MainSender():
    def __init__(self, ):
        self.TCP_klient = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.TCP_klient.connect(("127.0.0.1", 1338))

        send_message = "HELLO"

        self.TCP_klient.send(send_message.encode('utf-8'))
        self.reciever = Reciever(self.TCP_klient)
        
        # TCP_klient.close()

class Reciever():
    def __init__(self, serversock):
        self.serversock = serversock
        is_running = True

        while is_running:
            serverdata = serversock.recv(2048)
            if not serverdata:
                serversock.close()
                break

            # Kontrol om beskeden er en fil
            decoded_data = serverdata.decode('UTF-8')
            if decoded_data.startswith('FILE:'):
                self.receive_file(decoded_data)
            else:
                print(f'Serverdata UTF-8 decoded\n{decoded_data}')

    def receive_file(self, file_header):
        header_lines = file_header.split("\n")
        file_name = header_lines[0].split(":")[1].strip()
        file_length = int(header_lines[1].split(":")[1].strip())

        download_dir = "./Downloads"
        if not path.exists(download_dir):
            os.makedirs(download_dir)

        file_path = path.join(download_dir, file_name)
        print(f'Modtager fil: {file_name} på {file_length} bytes...')

        with open(file_path, 'wb') as f:
            bytes_received = 0
            while bytes_received < file_length:
                buffer = self.serversock.recv(2048)
                if not buffer:
                    break
                f.write(buffer)
                bytes_received += len(buffer)
        
        print(f'Fil gemt med stien: {file_path}')


send = MainSender()

if __name__ == "__main__":
    server = MainSender()
   
    # signal.signal(signal.SIGINT, lambda _, __: signal_handler(server))

    try:
        server.run()
    except KeyboardInterrupt:
        print("\nAfslutter SENDER...")
        server.running = False
        sys.exit(0)                                # Dræber hele serverprocessen
