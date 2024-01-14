import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
class UserInterface:
    def __init__(self, node, network):
        self.node = node
        self.network = network
        self.root = tk.Tk()
        self.root.title("P2P File Sharing App")

        ip_label = tk.Label(self.root, text=f"Node IP: {self.node.address}")
        ip_label.pack(pady=5)
        port_label = tk.Label(self.root, text=f"Node Port: {self.node.port}")
        port_label.pack(pady=5)

        label = tk.Label(self.root, text="P2P File Sharing App")
        label.pack(pady=10)

        add_file_button = tk.Button(self.root, text="Add Files", command=self.add_files)
        add_file_button.pack()

        search_button = tk.Button(self.root, text="Search Files", command=self.search_files)
        search_button.pack()

        transfer_button = tk.Button(self.root, text="Initiate File Transfer", command=self.initiate_file_transfer)
        transfer_button.pack()

        self.file_listbox = tk.Listbox(self.root)
        self.file_listbox.pack()

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack()

        self.transfer_status_label = tk.Label(self.root, text="")
        self.transfer_status_label.pack()

    def add_files(self):
        file_path = filedialog.askopenfilename()

        if file_path:
            filename = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)

            self.node.add_file(filename)

            self.update_file_list()

            messagebox.showinfo("File Addition", "File added successfully.")


    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        for filename in self.node.files:
            self.file_listbox.insert(tk.END, filename)

    def search_files(self):
        search_criteria = simpledialog.askstring("File Search", "Enter the file name to search:")
        if search_criteria:
            results = self.node.search_files(search_criteria)
            if results:
                self.result_label.config(text="\n".join(results))
            else:
                self.result_label.config(text="No matching files found.")

    def initiate_file_transfer(self):
        selected_file = simpledialog.askstring("File Transfer", "Enter the filename to transfer:")
        if selected_file:
            target_node_input = simpledialog.askstring("Target Node", "Enter the target node (IP:Port):")
            if target_node_input:
                target_ip, target_port = target_node_input.split(':')

                target_node = (target_ip, int(target_port))

                response = self.node.initiate_file_transfer(target_node, selected_file, target_ip, int(target_port))
                if response:
                    if response["status"] == "success":
                        self.transfer_status_label.config(text=response["message"])
                    else:
                        self.transfer_status_label.config(text=f"Error: {response['message']}")


    def run(self):
        self.root.mainloop()
