from functools import partial
import time
from PyQt5.QtCore import QTimer

from ExcelWriter import ExcelWriter
from ProgramState import ProgramState
from constants.text import TEXT_TO_EXCEL_LEFT_ANSWER, TEXT_TO_EXCEL_RIGHT_ANSWER, TEXT_TO_EXCEL_FILLER_ANSWER


class AnswerHandler:
    def __init__(self, program_window):
        self.DEFAULT_TEXT_COLOR = 12
        self.HIGHLIGHT_TEXT = 13

        self.Z_KEY_NATIVE_CODE = 44
        self.M_KEY_NATIVE_CODE = 50
        self.R_KEY_NATIVE_CODE = 19

        self.LEFT_CTRL_NATIVE_CODE = 29
        self.RIGHT_CTRL_NATIVE_CODE = 285

        self.LEFT_ANSWER_KEY = self.LEFT_CTRL_NATIVE_CODE
        self.RIGHT_ANSWER_KEY = self.RIGHT_CTRL_NATIVE_CODE

        self.LEFT_ANSWER = TEXT_TO_EXCEL_LEFT_ANSWER
        self.RIGHT_ANSWER = TEXT_TO_EXCEL_RIGHT_ANSWER

        self.delay_before_next_image = 4000 #4 seconds

        self.excel_writer = program_window.excel_writer
        self.program_window = program_window
        self.human_answers = []
        self.reaction_time = []
        self.correct_answers = []
        self.previous_time = time.time()

    def process_answer(self, program_window, keyboard_key, program_state):
        print(f"proces answer: {str(program_state)}")
        match program_state:
            case ProgramState.TUTORIAL_PAGE:
                if self._is_answer_key(keyboard_key):
                    correct_answer = program_window.current_image.answer
                    widget = self._get_layout_widget(program_window, keyboard_key)
                    human_answer = self.LEFT_ANSWER if keyboard_key == self.LEFT_ANSWER_KEY else self.RIGHT_ANSWER
                    is_answer_correct = self._is_answer_correct(human_answer, correct_answer)
                    self.simulate_answer_registration(program_window, widget, is_answer_correct)
            case ProgramState.MAIN_TEST_PAGE:
                if self._is_answer_key(keyboard_key):
                    correct_answer = program_window.current_image.answer
                    self.correct_answers.append(correct_answer)
                    widget = self._get_layout_widget(program_window, keyboard_key)
                    human_answer = self.LEFT_ANSWER if keyboard_key == self.LEFT_ANSWER_KEY else self.RIGHT_ANSWER
                    is_answer_correct = self._is_answer_correct(human_answer, correct_answer)
                    self.register_answer(program_window, widget, human_answer, is_answer_correct)
            case ProgramState.END_PAGE:
                if keyboard_key == self.R_KEY_NATIVE_CODE:
                    program_window.reset_test()
                    self._set_variables_to_default()

    def _is_answer_correct(self, human_answer, correct_answer):
        if correct_answer == TEXT_TO_EXCEL_FILLER_ANSWER:
            return True
        else:
            return human_answer == correct_answer

    def register_answer(self, program_window, widget, human_answer, is_answer_correct):
        program_window.key_pressed = True
        self._measure_time()
        QTimer.singleShot(self.delay_before_next_image, partial(self._continue_test, program_window, widget))
        program_window.highlight_chosen_answer(widget, is_answer_correct)
        self.human_answers.append(human_answer)

    def simulate_answer_registration(self, program_window, widget, is_answer_correct):
        program_window.key_pressed = True
        self.previous_time = time.time()
        QTimer.singleShot(self.delay_before_next_image, partial(self._go_to_main_test, program_window, widget))
        program_window.highlight_chosen_answer(widget, is_answer_correct)

    def _get_layout_widget(self, program_window, keyboard_key):
        widget_pos = -1
        match keyboard_key:
            case self.LEFT_ANSWER_KEY:
                widget_pos = 0
            case self.RIGHT_ANSWER_KEY:
                widget_pos = 2
            case _:
                pass
        widget = program_window.main_test_page_layout.itemAtPosition(2, widget_pos).widget()
        return widget

    def _is_answer_key(self, keyboard_key):
        return keyboard_key == self.LEFT_ANSWER_KEY or keyboard_key == self.RIGHT_ANSWER_KEY


    def _measure_time(self):
        current_time = time.time()
        diff = current_time - self.previous_time
        self.previous_time = current_time
        self.reaction_time.append(diff)
        #print(str(self.reaction_time)) #########################

    def _go_to_main_test(self, program_window, widget):
        program_window.main_labels_manager.change_bottom_label_text_color(widget, self.DEFAULT_TEXT_COLOR)
        program_window.change_image()
        program_window.next_state()

    def _continue_test(self, program_window, widget):
        program_window.key_pressed = False
        program_window.main_labels_manager.change_bottom_label_text_color(widget, self.DEFAULT_TEXT_COLOR)
        if program_window.image_provider.isNextImageAvaiable():
            program_window.change_image()
        else:
            correct_reaction_time = [x - int(self.program_window.answers_handler.delay_before_next_image/1000) for x in self.reaction_time]
            self.excel_writer.save_data_to_excel(self.correct_answers, self.human_answers, correct_reaction_time, program_window.current_person)
            program_window.next_state()

    def _set_variables_to_default(self):
        self.human_answers = []
        self.reaction_time = []
        self.correct_answers = []
