import sys
import traceback

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

from AnswerHandler import AnswerHandler
from ExcelInfoBox import ExcelInfoBox
from ExcelWriter import ExcelWriter
from ImageDelayWindow import ImageDelayWindow
from ImageProvider import *
from MainLabelsManager import MainLabelsManager
from MissingDataErrorBox import MissingDataErrorBox
from Person import Person
from ProgramState import ProgramState
from QuestionnaireWindow import QuestionnaireWindow
from SecretCodesHandler import SecretCodesHandler
from constants.main_settings import APP_BACKGROUND_COLOR
from constants.text import APP_NAME
from setup_functions import create_start_page_layout, create_main_test_page_layout, crete_end_page_layout


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        #self.setObjectName("MainWindow")
        #self.setStyleSheet("#MainWindow {background-color: " + "#212d3e}")
        self.setStyleSheet("background-color: " + APP_BACKGROUND_COLOR)
        self.setWindowIcon(QtGui.QIcon('cat.jpg')) ######################################

        self.LEFT_ANSWER = TEXT_TO_EXCEL_LEFT_ANSWER
        self.RIGHT_ANSWER = TEXT_TO_EXCEL_RIGHT_ANSWER

        # constants to function "change_bottom_label_text_color()"
        self.DEFAULT_TEXT_COLOR = 12
        self.HIGHLIGHT_TEXT = 13

        self.image_provider = ImageProvider()
        self.main_labels_manager = MainLabelsManager()
        self.excel_writer = ExcelWriter()
        self.answers_handler = AnswerHandler(self)
        self.program_state = ProgramState()
        self.current_person = Person()
        self.current_ID = ExcelWriter().get_last_person_ID() + 1
        self.current_person.ID = self.current_ID
        self.secret_codes_handler = SecretCodesHandler(self)
        self.key_pressed = False
        self.questionnaire_window_exist = False
        self.page_index = 0
        self.recent_pressed_keys = []
        self.current_image = self.image_provider.get_first_image()

        self.stack = QStackedWidget(self)

        # Create two different layouts
        self.startPage = QWidget()
        self.mainTestPage = QWidget()
        self.endPage = QWidget()

        # Start page Layout
        start_page_layout = create_start_page_layout(self)
        self.startPage.setLayout(start_page_layout)

        # main test page Layout
        self.main_test_page_layout = create_main_test_page_layout(self)
        self.mainTestPage.setLayout(self.main_test_page_layout)
        self.main_labels_manager.setLabelsText(self, self.main_labels_manager.TUTORIAL_TEXT)

        # end page layout
        self.end_page_layout = crete_end_page_layout(self)
        self.endPage.setLayout(self.end_page_layout)

        # Add pages to stacked widget
        self.stack.addWidget(self.startPage)
        self.stack.addWidget(self.mainTestPage)
        self.stack.addWidget(self.endPage)

        # Set the main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)

        self.openWindowToFillUp()
        self.showMaximized()
        #self.setWindowFlags(Qt.FramelessWindowHint)

    def instruction_button_click(self):
        if self.questionnaire_window_exist or self.questionaryToFillUp.is_data_missing():
            MissingDataErrorBox(self.questionaryToFillUp).show_window()
        else:
            self.next_state()

    def next_state(self):
        self.page_index += 1
        match self.page_index:
            case 0:
                self.program_state.change_state(ProgramState.START_PAGE)
                self.switch_layout(0)
            case 1:
                self.program_state.change_state(ProgramState.TUTORIAL_PAGE)
                self.main_labels_manager.setLabelsText(self, self.main_labels_manager.TUTORIAL_TEXT)
                print(f"next_state: {self.image_provider.current_image_index}")
                self.switch_layout(1)
            case 2:
                self.program_state.change_state(ProgramState.MAIN_TEST_PAGE)
                self.main_labels_manager.setLabelsText(self, self.main_labels_manager.MAIN_TEST_TEXT)
            case 3:
                self.program_state.change_state(ProgramState.END_PAGE)
                self.switch_layout(2)
            case _:
                self.reset_layout()

    def switch_layout(self, index):
        # self.stack.setCurrentWidget(self.page2)  # Switch to the second page
        self.stack.setCurrentIndex(index)

    def reset_layout(self):
        self.page_index = 0
        self.program_state.change_state(ProgramState.START_PAGE)
        self.switch_layout(0)

    def resizeEvent(self, event):
        self.update_frame_size()  # Update frame size dynamically
        super().resizeEvent(event)

    def update_frame_size(self):
        """Set frame size as a percentage of window size"""
        shorter_length = self.height() if self.width() > self.height() else self.width()
        width = int(shorter_length * 0.6*1.35)  # 60% of window width
        height = int(shorter_length * 0.6)  # 60% of window height
        self.image_frame.setFixedSize(width, height)
        self.update_image()

    def update_image(self):
        scaled_pixmap = self.current_image.image_pixmap.scaled(self.image_frame.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setFixedSize(self.image_frame.size())

    def keyPressEvent(self, e):
        self.secret_codes_handler.write_key(e.key())

        if not self.key_pressed:
            self.answers_handler.process_answer(self, e.nativeScanCode(), self.program_state.get_current_state())

    def highlight_chosen_answer(self, widget, is_answer_correct):
        if isinstance(widget, QLabel):
            self.main_labels_manager.change_bottom_label_text_color(widget, self.HIGHLIGHT_TEXT, is_answer_correct)

    def change_image(self):
        self.current_image = self.image_provider.get_next_image()
        self.update_image()
        self.key_pressed = False

    def reset_test(self):
        self.current_person = Person()
        self.current_ID += 1
        self.current_person.ID = self.current_ID
        self.reset_layout()
        self._set_variables_to_default()

    def openWindowToFillUp(self):
        if(not self.questionnaire_window_exist):
            self.questionaryToFillUp = QuestionnaireWindow(self)
            self.questionaryToFillUp.show()

    def openExcelInfoBox(self):
        ExcelInfoBox(self).show_window()

    def openImageDelayWindow(self):
        self.window_box = ImageDelayWindow(self)
        self.window_box.open_image_delay_window()
        #window_box.show()

    def _set_variables_to_default(self):
        self.key_pressed = False
        self.questionnaire_window_exist = False
        self.openWindowToFillUp()
        self.page_index = 0
        self.current_image = self.image_provider.get_first_image()
        self.update_image()

def exception_handler(exc_type, exc_value, exc_traceback):
    """
    Custom exception handler that displays a QMessageBox for unhandled exceptions.
    """

    error_details = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print("Unhandled Exception:", error_details)  # Log full traceback to console

    # Extract last traceback entry (where the error occurred)
    last_trace = traceback.extract_tb(exc_traceback)[-1]
    file_name, line_number, function_name, _ = last_trace

    # Create a detailed error message
    error_message = (
        f"An unexpected error occurred!\n\n"
        f"File: {file_name}\n"
        f"Line: {line_number}\n"
        f"Function: {function_name}\n\n"
        f"Error: {exc_value}"
    )

    # Show the error message in a QMessageBox
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setWindowTitle("Application Error")
    msg_box.setText("An unexpected error occurred!")
    msg_box.setInformativeText(error_message)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
    msg_box.exec_()

    sys.exit(1)

app = QApplication([])
sys.excepthook = exception_handler
window = MainWindow()
window.show()
app.exec_()
