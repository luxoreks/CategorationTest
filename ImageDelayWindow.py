from PyQt5 import QtCore
from PyQt5.QtCore import QRegExp,  Qt
from PyQt5.QtGui import QFont, QRegExpValidator
from PyQt5.QtWidgets import *

from constants.questionnaire_settings import BACKGROUND_COLOR


class ImageDelayWindow(QWidget):
    def __init__(self, program_window):
        super().__init__()

        self.setWindowTitle("Czas pomiędzy obrazkami")
        #self.setParent(program_window)
        self.program_window = program_window

        self.resize(600, 350)
        self.center()

        #self.bgColor = "#212d3e"
        #self.setStyleSheet("background-color: " + self.bgColor +"; border: 10px solid black")
        self.setObjectName("ImageDelayWindow")
        self.setStyleSheet("#ImageDelayWindow {background-color:" + BACKGROUND_COLOR + "; border: 10px solid #212d3e;}")
        # 7b859c

        main_layout = QGridLayout()
        self.setLayout(main_layout)

#f"Obecny czas do odczekania: {self.program_window.answers_handler.delay_before_next_image}"
        info_label = QLabel(f"Obecny czas między obraskami: {str(int(self.program_window.answers_handler.delay_before_next_image/1000))} s")
        info_label.setStyleSheet("font-size: 20px")
        info_label.setAlignment(Qt.AlignCenter)
        new_time_label = QLabel("Nowy czas [s]: ")

        self.new_time_textbox = QLineEdit()
        reg_ex = QRegExp("[1-9]")
        self.new_time_textbox.setValidator(QRegExpValidator(reg_ex))
        self.new_time_textbox.setText(str(int(self.program_window.answers_handler.delay_before_next_image/1000)))

        ok_button = QPushButton("Zatwierdź")
        ok_button.clicked.connect(self.ok_button_click)

        main_layout.addWidget(info_label, 0, 0, 1, 2)
        main_layout.addWidget(new_time_label, 1, 0)
        main_layout.addWidget(self.new_time_textbox, 1, 1)
        main_layout.addWidget(ok_button, 2, 1)


        #self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def ok_button_click(self):
        self.close()

    def open_image_delay_window(self):
        self.show()

    def closeEvent(self, event):
        self.program_window.answers_handler.delay_before_next_image = int(self.new_time_textbox.text())*1000
        event.accept()  # Allow the window to close normally

