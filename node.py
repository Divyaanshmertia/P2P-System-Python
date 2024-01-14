import json
import socket
import threading
import os

class Node:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.file_directory = "C:\\Users\\divya\\Documents\\902PM\\Assignment-1"  
        self.network = None
        self.files = {}
        self.neighbours = []

    def add_file(self, filename):
        self.files[filename] = os.path.getsize(os.path.join(self.file_directory, filename))

    def remove_file(self, filename):
        if filename in self.files:
            del self.files[filename]

    def add_neighbour(self, neighbour):
        self.neighbours.append(neighbour)

    def remove_neighbour(self, neighbour):
        if neighbour in self.neighbours:
            self.neighbours.remove(neighbour)

    def initialize_node(self, initial_neighbours):
        for neighbour in initial_neighbours:
            self.add_neighbour(neighbour)

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.address, self.port))
        server.listen(5)
        print(f"Node is listening on {self.address}:{self.port}")

        while True:
            client_socket, addr = server.accept()
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

            file_path = os.path.join(self.file_directory, filename)

            if client_socket:
                with open(file_path, "wb") as file:
                    while True:
                        chunk = client_socket.recv(1024)
                        if not chunk:
                            break
                        file.write(chunk)
            else:
                print("client_socket is not valid.")

            response = {"status": "received", "message": f"File '{filename}' received on {self.address}:{self.port}"}
            self.network.send_message(client_socket, response)

            self.add_file(filename)

            print(f"Received file '{filename}' from {client_socket.getpeername()} and saved to {file_path}")

        except Exception as e:
            print(f"Error handling file transfer: {str(e)}")

    def initiate_file_transfer(self, target_node, filename, target_ip, target_port):
        try:
            if target_node not in self.neighbours:
                return {"status": "error", "message": "Target node is not a neighbor."}

            file_path = os.path.join(self.file_directory, filename)
            if not os.path.isfile(file_path):
                return {"status": "error", "message": f"File '{filename}' not found on this node."}

            self.network.send_file(target_ip, target_port, file_path)

            return {"status": "success", "message": f"File '{filename}' transferred to {target_node}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
