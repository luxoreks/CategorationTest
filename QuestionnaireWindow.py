from PyQt5 import QtCore
from PyQt5.QtCore import QRegExp,  Qt
from PyQt5.QtGui import QFont, QRegExpValidator
from PyQt5.QtWidgets import *

from MissingDataErrorBox import MissingDataErrorBox
from constants.questionnaire_settings import BUTTON_COLOR, BUTTON_TEXT, BUTTON_TEXT_COLOR, BUTTON_TEXT_SIZE, MALE_SEX, \
    FEMALE_SEX, DEFAULT_SEX_TEXT, COMBOBOX_BG_COLOR, SEX_LABEL, AGE_LABEL, LABELS_TEXT_SIZE, LABELS_TEXT_COLOR, \
    BACKGROUND_COLOR, MAIN_TEXT, FONT, AGE_BG_COLOR, AGE_LINEEDIT_TEXT_SIZE, DRIVER_LIC_TEXT, DRIV_LIC_BG_COLOR, \
    COMBOBOX_TEXT_SIZE, DRIV_LIC_TEXT_SIZE, MAIN_TEXT_SIZE, DEFAULT_DRIV_LIC_TEXT, DRIV_LIC_TRUE, DRIV_LIC_FALSE, \
    WINDOW_NAME


class QuestionnaireWindow(QFrame):
    def __init__(self, mainWindow):
        super().__init__()

        self.setWindowTitle(WINDOW_NAME)
        self.testWindow = mainWindow
        mainWindow.questionnaire_window_exist = True

        self.resize(600, 350)
        self.center()

        #self.bgColor = "#212d3e"
        #self.setStyleSheet("background-color: " + self.bgColor +"; border: 10px solid black")
        self.setObjectName("QuestionaryWindow")
        self.setStyleSheet("#QuestionaryWindow {background-color:" + BACKGROUND_COLOR + "; border: 10px solid #212d3e;}")
        # 7b859c

        questionaryLayout = QGridLayout()

        self.setLayout(questionaryLayout)

        labelMain = QLabel()
        labelMain.setText(MAIN_TEXT)
        labelMain.setFont(QFont(FONT))
        labelMain.setAlignment(QtCore.Qt.AlignCenter)
        labelMain.setStyleSheet("font-size: " + MAIN_TEXT_SIZE + "; color: #212d3e; font-weight: bold;") #d9deec - text color
        #labelMain.setMaximumSize(QSize(500, 200))
        questionaryLayout.addWidget(labelMain, 0, 0, 1, 3)

        labeslStylesheet = "color: " + LABELS_TEXT_COLOR + "; font-size: " + LABELS_TEXT_SIZE
        ageLabel = QLabel()
        ageLabel.setText(AGE_LABEL)
        ageLabel.setStyleSheet(labeslStylesheet)
        questionaryLayout.addWidget(ageLabel, 1, 0, alignment=Qt.AlignmentFlag.AlignRight)

        self.ageTextBox = QLineEdit()
        reg_ex = QRegExp("[1-9][0-9]")
        self.ageTextBox.setValidator(QRegExpValidator(reg_ex))
        self.ageTextBox.setStyleSheet("background-color: " + AGE_BG_COLOR + "; font-size: " + AGE_LINEEDIT_TEXT_SIZE)
        questionaryLayout.addWidget(self.ageTextBox, 1, 1)

        sexLabel = QLabel()
        sexLabel.setText(SEX_LABEL)
        sexLabel.setStyleSheet(labeslStylesheet)
        questionaryLayout.addWidget(sexLabel, 2, 0, alignment=Qt.AlignmentFlag.AlignRight)

        self.sexDropBox = QComboBox()
        self.sexDropBox.setStyleSheet("background-color: " + COMBOBOX_BG_COLOR + "; font-size: " + COMBOBOX_TEXT_SIZE)
        self.sexDropBox.addItems([DEFAULT_SEX_TEXT, MALE_SEX, FEMALE_SEX])
        questionaryLayout.addWidget(self.sexDropBox, 2, 1)

        driver_lic_label = QLabel()
        driver_lic_label.setText(DRIVER_LIC_TEXT)
        driver_lic_label.setStyleSheet(labeslStylesheet)
        questionaryLayout.addWidget(driver_lic_label, 3, 0)

        self.driv_lic_combobox = QComboBox()
        self.driv_lic_combobox.setStyleSheet("background-color: " + DRIV_LIC_BG_COLOR + "; font: " + DRIV_LIC_TEXT_SIZE)
        self.driv_lic_combobox.addItems([DEFAULT_DRIV_LIC_TEXT, DRIV_LIC_TRUE, DRIV_LIC_FALSE])
        questionaryLayout.addWidget(self.driv_lic_combobox)

        button = QPushButton()
        button.setText(BUTTON_TEXT)
        button.setStyleSheet("background-color: " + BUTTON_COLOR +"; color: " + BUTTON_TEXT_COLOR + "; padding: 10px; font: " + BUTTON_TEXT_SIZE )
        button.clicked.connect(self.button_clicked)
        questionaryLayout.addWidget(button, 4, 2)

        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

    def button_clicked(self):
        #app = QApplication(sys.argv)
        # app.setStyle("fusion")
        if self.is_data_missing():
            # errorBox = QMessageBox(self)
            # errorBox.setBaseSize(QSize(600, 600))
            # errorBox.setStyleSheet("background-color: white")
            # errorBox.setText("Uzupełnij dane")
            # errorBox.setIcon(QMessageBox.Warning)
            # errorBox.setWindowTitle("Brak danych")
            # errorBox.exec_()
           MissingDataErrorBox(self).show_window()
        else:
            self.testWindow.current_person.age = int(self.ageTextBox.text())
            self.testWindow.current_person.sex = self.sexDropBox.currentText()
            self.testWindow.current_person.has_driver_license = "Tak" if self.driv_lic_combobox.currentText() == DRIV_LIC_TRUE else "Nie"
            self.close()

    def is_data_missing(self):
        return (self.ageTextBox.text() == "" or self.sexDropBox.currentText() == DEFAULT_SEX_TEXT or self.driv_lic_combobox.currentText() == DEFAULT_DRIV_LIC_TEXT)

    def closeEvent(self, event):
        # Ensure that when the window is closed, the flag is set to False
        self.testWindow.questionnaire_window_exist = False
        event.accept()  # Allow the window to close normally

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())