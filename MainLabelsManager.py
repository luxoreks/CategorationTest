from constants.main_settings import APP_BACKGROUND_COLOR, \
    ANSWERS_LABELS_BG_COLOR, CORRECT_ANSWER_BG_COLOR, WRONG_ANSWER_BG_COLOR
from constants.text import TOP_TUTORIAL_LABEL_TEXT, BOTTOM_TUTORIAL_TEXT_LEFT, BOTTOM_TUTORIAL_TEXT_RIGHT, \
    TOP_MAIN_TEST_LABEL_TEXT, BOTTOM_MAIN_TEST_TEXT_LEFT, BOTTOM_MAIN_TEST_TEXT_RIGHT


class MainLabelsManager:
    def __init__(self):
        self.TUTORIAL_TEXT = 1
        self.MAIN_TEST_TEXT = 2

        self.DEFAULT_TEXT_COLOR = 12
        self.HIGHLIGHT_TEXT = 13

        self.current_label_color = ANSWERS_LABELS_BG_COLOR

    def setLabelsText(self, program_window, text_type):
        if text_type == self.TUTORIAL_TEXT:
            self._change_main_page_labels_text(program_window, TOP_TUTORIAL_LABEL_TEXT, BOTTOM_TUTORIAL_TEXT_LEFT, BOTTOM_TUTORIAL_TEXT_RIGHT)
        else:
            self._change_main_page_labels_text(program_window, TOP_MAIN_TEST_LABEL_TEXT, BOTTOM_MAIN_TEST_TEXT_LEFT, BOTTOM_MAIN_TEST_TEXT_RIGHT)

    def change_bottom_label_text_color(self, widget_label, mode,is_answer_correct = True):
        stylesheet = widget_label.styleSheet()
        new_stylesheet = ""
        match mode:
            case self.HIGHLIGHT_TEXT:
                new_bg_color = CORRECT_ANSWER_BG_COLOR if is_answer_correct else WRONG_ANSWER_BG_COLOR
                new_stylesheet = stylesheet.replace(f"background-color: {self.current_label_color};",
                                                    f"background-color: {new_bg_color};")
                self.current_label_color = new_bg_color
                # new_stylesheet = stylesheet.replace(f"color: {BOTTOM_LABELS_TEXT_COLOR};",f"color: {SELECTED_ANSWER_TEXT_COLOR};")
            case self.DEFAULT_TEXT_COLOR:
                new_stylesheet = stylesheet.replace(f"background-color: {self.current_label_color};",
                                                    f"background-color: {ANSWERS_LABELS_BG_COLOR};")
                self.current_label_color = ANSWERS_LABELS_BG_COLOR
        # new_stylesheet = stylesheet.replace(f"color: {SELECTED_ANSWER_TEXT_COLOR};", f"color: {BOTTOM_LABELS_TEXT_COLOR};")
        widget_label.setStyleSheet(new_stylesheet)

    def _change_main_page_labels_text(self, program_window, top_label_text, bottom_left_label_text,
                                      bottom_right_label_text):
        program_window.top_label.setText(top_label_text)
        program_window.bottom_left_label.setText(bottom_left_label_text)
        program_window.bottom_right_label.setText(bottom_right_label_text)