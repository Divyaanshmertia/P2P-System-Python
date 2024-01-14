import tkinter as tk
from node import Node
from network import Network
from user_interface import UserInterface
import threading
import os

if __name__ == "__main__":
    # Create three peer nodes with their respective addresses and ports
    node1 = Node("127.0.0.1", 12345)
    node2 = Node("127.0.0.1", 12346)
    node3 = Node("127.0.0.1", 12347)

    # Initialize the nodes with their initial neighbors
    node1.initialize_node([("127.0.0.1", 12346), ("127.0.0.1", 12347)])
    node2.initialize_node([("127.0.0.1", 12345), ("127.0.0.1", 12347)])
    node3.initialize_node([("127.0.0.1", 12345), ("127.0.0.1", 12346)])

    # Create network instances for each node
    network1 = Network(node1)
    network2 = Network(node2)
    network3 = Network(node3)

    # Set the network instances for each node
    node1.network = network1
    node2.network = network2
    node3.network = network3

    # Start the servers for each node in separate threads
    server_thread1 = threading.Thread(target=node1.start_server)
    server_thread2 = threading.Thread(target=node2.start_server)
    server_thread3 = threading.Thread(target=node3.start_server)

    server_thread1.start()
    server_thread2.start()
    server_thread3.start()

    # Create user interfaces for each node
    ui1 = UserInterface(node1, network1)
    ui2 = UserInterface(node2, network2)
    ui3 = UserInterface(node3, network3)

    # Start the user interfaces
    ui1.run()
    ui2.run()
    ui3.run()
