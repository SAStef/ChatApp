import socket as s
import os

class MainSender():
    def __init__(self):
        self.TCP_client = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.TCP_client.connect(("127.0.0.1", 1338))
        send_message = "HELLO"
        self.TCP_client.send(send_message.encode('utf-8'))
        self.reciever = Reciever(self.TCP_client)

class Reciever():
    def __init__(self, serversock):
        self.serversock = serversock
        self.is_running = True

        while self.is_running:
            serverdata = self.serversock.recv(2048)
            if not serverdata:
                self.serversock.close()
                break

            # Tjek om det er en filheader
            decoded_data = serverdata.decode("utf-8")
            if decoded_data.startswith("FILE:"):
                self.receive_file(decoded_data)
            else:
                print(f'Serverdata UTF-8 decoded:\n{decoded_data}')

    def receive_file(self, file_header):
        # Ekstraher filnavn og længde fra header
        header_lines = file_header.split("\n")
        file_name = header_lines[0].split(":")[1].strip()
        file_length = int(header_lines[1].split(":")[1].strip())

        # Opret downloads-mappe, hvis den ikke findes
        download_dir = "./downloads"
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        file_path = os.path.join(download_dir, file_name)

        print(f"Modtager fil: {file_name} ({file_length} bytes)...")
        with open(file_path, 'wb') as f:
            bytes_received = 0
            while bytes_received < file_length:
                chunk = self.serversock.recv(2048)
                if not chunk:
                    break
                f.write(chunk)
                bytes_received += len(chunk)

        print(f"Fil gemt til: {file_path}")

if __name__ == "__main__":
    send = MainSender()