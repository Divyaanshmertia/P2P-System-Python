import socket
import os
import json
import threading  

class Network:
    def __init__(self, node):
        self.node = node
        self.server_socket = None
        self.connected_sockets = []

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.node.address, self.node.port))
        self.server_socket.listen(5)
        print(f"Node is listening on {self.node.address}:{self.node.port}")

        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Accepted connection from {addr}")
            client_handler = threading.Thread(target=self.handle_connection, args=(client_socket,))
            client_handler.start()

    def handle_connection(self, client_socket):
        try:
            print(f"Accepted connection from {client_socket.getpeername()}")
            request_data = client_socket.recv(1024).decode()
            request = json.loads(request_data)

            if request["type"] == "file_transfer":
                file_transfer_thread = threading.Thread(target=self.handle_file_transfer, args=(client_socket, request))
                file_transfer_thread.start()
            else:
                pass

        except Exception as e:
            print(f"An error occurred: {str(e)}")

        finally:
            client_socket.close()

    def handle_file_transfer(self, client_socket, request):
        try:
            filename = "received" + request["filename"] 
            file_path = os.path.join(self.node.file_directory, filename)
            with open(file_path, "rb") as file:
                file_content = file.read()

            print(f"File content of '{filename}':\n{file_content.decode()}")
            if client_socket:
                with open(file_path, "wb") as file:
                    while True:
                        chunk = client_socket.recv(1024)
                        if not chunk:
                            break
                        file.write(chunk)
            else:
                print("client_socket is not valid.")

            response = {"status": "received", "message": f"File '{filename}' received on {self.node.address}:{self.node.port}"}
            
            if client_socket.fileno() != -1:
                client_socket.send(json.dumps(response).encode())
            else:
                print("Socket is already closed.")

            print(f"Received file '{filename}' from {client_socket.getpeername()} and saved to {file_path}")

        except Exception as e:
            print(f"Error handling file transfer: {str(e)}")

    def send_file(self, target_address, target_port, file_path):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as transfer_socket:
                transfer_socket.connect((target_address, target_port))

                request = {"type": "file_transfer", "filename": os.path.basename(file_path)}

                transfer_socket.send(json.dumps(request).encode())

                with open(file_path, "rb") as file:
                    try:
                        file_data = file.read()
                        total_sent = 0
                        while total_sent < len(file_data):
                            sent = transfer_socket.send(file_data[total_sent:])
                            if sent == 0:
                                raise RuntimeError("Socket connection broken")
                            total_sent += sent
                    except Exception as e:
                        print(f"Error while sending data: {str(e)}")


        except Exception as e:
            print(f"Error sending file to {target_address}:{target_port}: {str(e)}")


    def receive_message(self, socket):
        try:
            data = socket.recv(1024).decode()
            return json.loads(data)
        except Exception as e:
            print(f"Error receiving message: {str(e)}")
            return None
