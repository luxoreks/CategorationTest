from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from constants.text import *
from constants.main_settings import *

def create_start_page_layout(program_window):
    layout1 = QGridLayout()
    title_label = QLabel(INSTRUCTION_TITLE_LABEL)
    title_label.setStyleSheet("font: " + START_INSTRUCTION_TITLE_TEXT_SIZE + "; color: " + START_INSTRUCTION_TITLE_TEXT_COLOR + "; font-weight: bold;")
    title_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
    # title_label.setMaximumSize(QSize(3000, 50))

    instruction_text_label = QLabel(TUTORIAL_TEXT)
    instruction_text_label.setStyleSheet("font: " + START_INSTRUCTION_TEXT_SIZE + "; color: " + START_INSTRUCTION_TEXT_COLOR)
    instruction_text_label.setWordWrap(True)
    # instruction_text_label.setMaximumSize(QSize(3000, 200))
    instruction_text_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    button = QPushButton("Ok")
    button.setMaximumSize(QSize(200, 50))
    button.setStyleSheet("font-size: " + START_INSTRUCTION_BUTTON_TEXT_SIZE + "; color: " + START_INSTRUCTION_BUTTON_TEXT_COLOR + "; background-color: " + OK_BUTTON_BG_COLOR )

    layout1.addWidget(title_label, 0, 0, 1, 2)
    layout1.addWidget(instruction_text_label, 1, 0, 1, 2)
    layout1.addWidget(button, 2, 1)
    layout1.setContentsMargins(200, 200, 200, 200)

    layout1.setRowStretch(0, 1)
    layout1.setRowStretch(1, 7)
    layout1.setRowStretch(2, 2)

    button.clicked.connect(program_window.instruction_button_click)

    return layout1

def create_main_test_page_layout(program_window):
    return _create_main_test_layout(program_window, TOP_MAIN_TEST_LABEL_TEXT, BOTTOM_MAIN_TEST_TEXT_LEFT, BOTTOM_MAIN_TEST_TEXT_RIGHT)

def crete_end_page_layout(program_window):
    end_page_layout = QVBoxLayout()
    end_message_label = QLabel(END_MESSAGE)
    end_message_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
    end_message_label.setStyleSheet("color: " + END_PAGE_TEXT_COLOR + "; font: " + END_PAGE_TEXT_SIZE)

    end_page_layout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
    end_page_layout.addWidget(end_message_label)

    return end_page_layout

def _create_main_test_layout(program_window, top_label_text, bottom_left_label_text, bottom_right_label_text):
    main_test_layout = QGridLayout()
    program_window.top_label = QLabel(top_label_text)
    program_window.top_label.setStyleSheet("background-color: " + APP_BACKGROUND_COLOR + "; font: " + TOP_LABEL_TEXT_SIZE + f"; color: {TOP_LABEL_TEXT_COLOR};")
    program_window.top_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
    main_test_layout.addWidget(program_window.top_label, 0, 0, 1, 4)

    _create_image_frame(program_window)
    main_test_layout.addWidget(program_window.image_frame, 1, 1, 1, 2, alignment=Qt.AlignCenter)

    program_window.bottom_left_label = QLabel(bottom_left_label_text)
    program_window.bottom_left_label.setStyleSheet("background-color: " + ANSWERS_LABELS_BG_COLOR + "; font: " + BOTTOM_LABELS_TEXT_SIZE + f"; color: {BOTTOM_LABELS_TEXT_COLOR}; border: 2px solid black;")
    program_window.bottom_left_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
    program_window.bottom_left_label.setMinimumSize(QSize(400, 100))
    main_test_layout.addWidget(program_window.bottom_left_label, 2, 0, 1, 2, alignment=Qt.AlignCenter)

    program_window.bottom_right_label = QLabel(bottom_right_label_text)
    program_window.bottom_right_label.setStyleSheet("background-color: " + ANSWERS_LABELS_BG_COLOR + "; font: " + BOTTOM_LABELS_TEXT_SIZE + f"; color: {BOTTOM_LABELS_TEXT_COLOR}; border: 2px solid black;")
    program_window.bottom_right_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
    program_window.bottom_right_label.setMinimumSize(QSize(400, 100))
    main_test_layout.addWidget(program_window.bottom_right_label, 2, 2, 1, 2, alignment=Qt.AlignCenter)

    return main_test_layout

def _create_image_frame(program_window):
    program_window.image_frame = QFrame(program_window)
    program_window.image_frame.setStyleSheet("border: 3px solid black;")  # Add a black border
    program_window.image_frame.setFixedSize(600, 600)  # Set the frame size (adjust as needed)

    # Create a QLabel to display the image
    program_window.image_label = QLabel(program_window.image_frame)
    program_window.image_label.setAlignment(Qt.AlignCenter)

    # Load and scale the image
    _set_image(program_window)

def _set_image(program_window):
    """Scale the image while maintaining aspect ratio"""
    program_window.update_frame_size()
    program_window.update_image()
