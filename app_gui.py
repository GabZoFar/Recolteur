import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt6.QtCore import QThread, pyqtSignal
import app  as recolteur # Import your existing app.py file

class Worker(QThread):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        recolteur.main(self)  # Pass the worker instance to main
        self.finished.emit()

    def stop(self):
        self.running = False

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.worker = None

    def initUI(self):
        self.setWindowTitle('Récolteur')
        self.setGeometry(100, 100, 200, 100)

        layout = QVBoxLayout()

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_main)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.stop_main)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)

        self.status_label = QLabel('', self)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def start_main(self):
        self.worker = Worker()
        self.worker.finished.connect(self.on_finished)
        self.worker.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_main(self):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()
            self.on_finished()
            self.status_label.setText("Fin de la récolte...")

    def on_finished(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())