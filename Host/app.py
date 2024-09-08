from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from src.blockchain import Blockchain
from cryptography.fernet import Fernet
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import requests
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.server_url = 'http://localhost:5000'
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.setStyleSheet("""
    QWidget {
        background-color: #2e2e2e;
        color: #e0e0e0;
        font-family: 'Sans-serif';
    }
    QLabel {
        color: #e0e0e0;
    }
    QLineEdit {
        border: 1px solid #6c4f7c;
        border-radius: 4px;
        padding: 5px;
        background-color: #3c3c3c;
        color: #e0e0e0;
    }
    QPushButton {
        background-color: #5e35b1;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 10px;
        font-size: 16px;
    }
    QPushButton:disabled {
        background-color: #7c4d9d;
    }
""")

        self.create_data_label = QLabel("Enter data to store:")
        layout.addWidget(self.create_data_label)

        self.create_data_entry = QLineEdit()
        layout.addWidget(self.create_data_entry)

        self.create_data_button = QPushButton("Generate Key and Encrypt Data")
        self.create_data_button.clicked.connect(self.generate_key_and_store_data)
        layout.addWidget(self.create_data_button)

        self.key_label = QLabel("Encryption Key:")
        layout.addWidget(self.key_label)

        self.key_display = QLineEdit()
        self.key_display.setReadOnly(True)
        layout.addWidget(self.key_display)

        self.block_hash_label = QLabel("Block Hash for Retrieval:")
        layout.addWidget(self.block_hash_label)

        self.block_hash_display = QLineEdit()
        self.block_hash_display.setReadOnly(True)
        layout.addWidget(self.block_hash_display)

        # Recuperação de Dados
        self.retrieve_key_label = QLabel("Enter encryption key to retrieve data:")
        layout.addWidget(self.retrieve_key_label)

        self.retrieve_key_entry = QLineEdit()
        layout.addWidget(self.retrieve_key_entry)

        self.retrieve_block_hash_label = QLabel("Enter block hash to retrieve data:")
        layout.addWidget(self.retrieve_block_hash_label)

        self.retrieve_block_hash_entry = QLineEdit()
        layout.addWidget(self.retrieve_block_hash_entry)

        self.retrieve_data_button = QPushButton("Retrieve Data")
        self.retrieve_data_button.clicked.connect(self.retrieve_data)
        layout.addWidget(self.retrieve_data_button)

        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

        self.setLayout(layout)
        self.setWindowTitle('Secure Data Storage')
        self.setGeometry(100, 100, 400, 300)
        self.show()

    def generate_key_and_store_data(self):
        data = self.create_data_entry.text()
        if data:
            key = Fernet.generate_key()
            blockchain_key = key.decode()

            response = requests.post(f'{self.server_url}/add_data', json={
                'data': data,
                'key': blockchain_key
            })

            if response.status_code == 200:
                block_hash = response.json().get('block_hash')
                self.key_display.setText(blockchain_key)
                self.block_hash_display.setText(block_hash)
                QMessageBox.information(self, "Key Generated", "Your key has been generated. Copy it and store it securely.")
            else:
                QMessageBox.critical(self, "Error", response.json().get('error', 'An error occurred.'))
        else:
            QMessageBox.critical(self, "Error", "Please enter some data.")

    def retrieve_data(self):
        key = self.retrieve_key_entry.text().encode()
        block_hash = self.retrieve_block_hash_entry.text()
        response = requests.get(f'{self.server_url}/get_data/{block_hash}', params={'key': key})

        if response.status_code == 200:
            data = response.json().get('data')
            self.result_label.setText(f"Decrypted Data: {data}")
        else:
            self.result_label.setText(response.json().get('error', 'Failed to retrieve data.'))

if __name__ == '__main__':
    app = QApplication([])
    ex = App()
    app.exec_()
