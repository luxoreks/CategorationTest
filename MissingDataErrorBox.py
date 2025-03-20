from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMessageBox


class MissingDataErrorBox:
    def __init__(self, parent):
        self.errorBox = QMessageBox(parent)
        self.errorBox.setBaseSize(QSize(600, 600))
        self.errorBox.setStyleSheet("background-color: white")
        self.errorBox.setText("Uzupełnij dane")
        self.errorBox.setIcon(QMessageBox.Warning)
        self.errorBox.setWindowTitle("Brak danych")


    def show_window(self):
        self.errorBox.exec_()