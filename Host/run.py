import threading
from src.server import app as flask_app  
from PyQt5.QtWidgets import QApplication
from src.app import App 


def run_server():
    flask_app.run(host='0.0.0.0', port=5000, debug=False)

def run_app():
    app = QApplication([])
    ex = App()
    app.exec_()

if __name__ == '__main__':
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
    
    run_app()
