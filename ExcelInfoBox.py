from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMessageBox


class ExcelInfoBox:
    def __init__(self, parent):
        self.errorBox = QMessageBox(parent)
        self.errorBox.setBaseSize(QSize(600, 600))
        self.errorBox.setStyleSheet("background-color: white")

        self.errorBox.setText("Excel wyniki, pusty wiersz: " + str(parent.excel_writer.get_summary_results_row() + 1) + "\n"+
                              "Excel dane, pusty wiersz: " + str(parent.excel_writer.get_data_row() + 1))
        #self.errorBox.setText(parent.excel_writer.get_data_row())
        #self.errorBox.setIcon(QMessageBox.Ok)
        self.errorBox.setWindowTitle("Excel index")


    def show_window(self):
        self.errorBox.exec_()