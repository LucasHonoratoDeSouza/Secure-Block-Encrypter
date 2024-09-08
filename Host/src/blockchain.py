import pickle
import hashlib
from cryptography.fernet import Fernet
import datetime as dt
import os

class Blockchain:
    def __init__(self):
        self.chain = []
        self.key = Fernet.generate_key()
        self.load_from_file("blockchain_data.pkl")

    def add_data(self, data, key):
        encrypted_data = self.encrypt_data(data, key)
        block = Block(len(self.chain), dt.datetime.now(), encrypted_data, self.chain[-1].hash if self.chain else '0')
        self.chain.append(block)
        return block.hash

    def encrypt_data(self, data, key):
        fernet = Fernet(key)
        return fernet.encrypt(data.encode())

    def decrypt_data(self, encrypted_data, key):
        fernet = Fernet(key)
        return fernet.decrypt(encrypted_data).decode()

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump((self.chain, self.key), file)

    def load_from_file(self, filename):
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                self.chain, self.key = pickle.load(file)
        else:
            self.chain = []
            self.key = Fernet.generate_key()
            self.save_to_file(filename)

    def get_data_by_hash(self, block_hash):
        for block in self.chain:
            if block.hash == block_hash:
                return block
        return None

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.data = data
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.index).encode("utf-8") +
                   str(self.timestamp).encode("utf-8") +
                   str(self.data).encode("utf-8") +
                   str(self.previous_hash).encode("utf-8"))
        return sha.hexdigest()
