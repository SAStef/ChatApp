import os
from PyQt6.QtCore import QThread, pyqtSignal

class ReceiveFilesThread(QThread):
    def __init__(self, client_socket, file_name, data_chunk_length):
        super().__init__()
        self.client_socket = client_socket
        self.file_name = file_name
        self.data_chunk_length = data_chunk_length

    def run(self):
        try:
            download_dir = "./Downloads"
            os.makedirs(download_dir, exist_ok=True)
            file_path = os.path.join(download_dir, self.file_name)

            with open(file_path, 'wb') as f:
                bytes_received = 0
                while bytes_received < self.data_chunk_length:
                    remaining_bytes = self.data_chunk_length - bytes_received
                    
                    buffer = self.client_socket.recv(min(2048, remaining_bytes))
                    
                    if not buffer:
                        raise ConnectionError("Connection closed before file transfer completed.")

                    f.write(buffer)
                    bytes_received += len(buffer)

                    print(f"Buffer (binary): {buffer} | Bytes remaining: {remaining_bytes} | Total bytes received: {bytes_received}")
                    print(f"Received {bytes_received}/{self.data_chunk_length} bytes")

                print(f"File saved to: {file_path}")

        except Exception as e:
            print(f"Error in file transfer: {e}")
        
        finally:
            self.client_socket.close()

class ReceiverThread(QThread):
    message_received = pyqtSignal(str)
    file_received = pyqtSignal(bytes, str)
    
    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket
        self.running = True
        
    def run(self):
        counter = 0
        while self.running:
            try:
                serverData = self.client_socket.recv(2048)
                
                if not serverData:
                    self.client_socket.close()
                    break

                if serverData.startswith(b'FILE:'):
                    header_data = serverData
                    while b"\n\n" not in header_data:
                        header_data += self.client_socket.recv(2048)
                    
                    header_lines = header_data.decode('utf-8').strip().split("\n")
                    file_name = header_lines[0].split(":")[1].strip()
                    data_chunk_length = int(header_lines[1].split(":")[1].strip())

                    file_thread = ReceiveFilesThread(self.client_socket, file_name, data_chunk_length)
                    file_thread.start()

                else:
                    decoded_data = serverData.decode('utf-8', errors='ignore')
                    self.message_received.emit(decoded_data)

            except Exception as e:
                if self.running:
                    print(f'Error in ReceiverThread: {e}')
                    counter += 1
                if counter > 20:
                    break
