import tkinter as tk
from tkinter import messagebox
from src.blockchain import Blockchain, Block
import datetime as dt

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Data Storage")
        self.root.geometry("400x300")

        self.blockchain = Blockchain()

        self.create_data_frame = tk.Frame(self.root, padx=10, pady=10, bg="#f0f0f0")
        self.create_data_frame.pack(padx=10, pady=10, fill=tk.X)

        self.create_data_label = tk.Label(self.create_data_frame, text="Enter data to store:", bg="#f0f0f0")
        self.create_data_label.pack()

        self.create_data_entry = tk.Entry(self.create_data_frame, width=50)
        self.create_data_entry.pack(pady=5)

        self.create_data_button = tk.Button(self.create_data_frame, text="Encrypt and Store", command=self.store_data)
        self.create_data_button.pack(pady=5)

        self.decrypt_data_frame = tk.Frame(self.root, padx=10, pady=10, bg="#f0f0f0")
        self.decrypt_data_frame.pack(padx=10, pady=10, fill=tk.X)

        self.decrypt_key_label = tk.Label(self.decrypt_data_frame, text="Enter key to decrypt:", bg="#f0f0f0")
        self.decrypt_key_label.pack()

        self.decrypt_key_entry = tk.Entry(self.decrypt_data_frame, width=50)
        self.decrypt_key_entry.pack(pady=5)

        self.decrypt_data_button = tk.Button(self.decrypt_data_frame, text="Decrypt Data", command=self.decrypt_data)
        self.decrypt_data_button.pack(pady=5)

        self.result_label = tk.Label(self.root, text="", wraplength=400, bg="#f0f0f0")
        self.result_label.pack(padx=10, pady=10)

    def store_data(self):
        data = self.create_data_entry.get()
        if data:
            encrypted_data = self.blockchain.encrypt_data(data)
            self.blockchain.add_block(Block(len(self.blockchain.chain), dt.datetime.now(), encrypted_data, self.blockchain.chain[-1].hash))
            messagebox.showinfo("Success", "Data has been encrypted and stored!")
        else:
            messagebox.showerror("Error", "Please enter some data.")

    def decrypt_data(self):
        key = self.decrypt_key_entry.get()
        if not key:
            messagebox.showerror("Error", "Please enter a key.")
            return
        
        block_hash = self.blockchain.chain[-1].hash 
        block = self.blockchain.get_data_by_hash(block_hash)
        if block:
            decrypted_data = self.blockchain.decrypt_data(block.data)
            if decrypted_data:
                self.result_label.config(text=f"Decrypted Data: {decrypted_data}")
            else:
                messagebox.showerror("Error", "Invalid key or data.")
        else:
            messagebox.showerror("Error", "No data found for the given block hash.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
