from ImageDelayWindow import ImageDelayWindow


class SecretCodesHandler:
    def __init__(self, program_window):
        self.program_window = program_window

        self.MAX_KEYS_TO_REMEMBER = 4
        self.recent_pressed_keys = []
        self.OPEN_QUESTIONNAIRE_WINDOW_CODE = ["Q", "U", "E", "S"]
        self.OPEN_EXCEL_ROW_INFO = ["E", "X", "C", "E"]
        self.CHANGE_DELAY_WINDOW = ["T", "I", "M", "E"]

    def write_key(self, key_number):
        try:
            key = chr(key_number)
        except:
            return
        self.recent_pressed_keys.append(key)
        if len(self.recent_pressed_keys) > self.MAX_KEYS_TO_REMEMBER:
            del self.recent_pressed_keys[0]
            print(str(self.recent_pressed_keys))

        self._check_code()

    def _check_code(self):
        match self.recent_pressed_keys:
            case self.OPEN_QUESTIONNAIRE_WINDOW_CODE:
                self.program_window.openWindowToFillUp()
            case self.OPEN_EXCEL_ROW_INFO:
                self.program_window.openExcelInfoBox()
            case self.CHANGE_DELAY_WINDOW:
                self.program_window.openImageDelayWindow()