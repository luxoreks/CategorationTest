from PyQt5.QtGui import QPixmap

from constants.text import TEXT_TO_EXCEL_LEFT_ANSWER, TEXT_TO_EXCEL_RIGHT_ANSWER, TEXT_TO_EXCEL_FILLER_ANSWER


class ImageProvider:
    def __init__(self):
        self.total_images = 13
        self.current_image_index = 0

        self.images_names = ["Prawo_Przyklad.png",
                             "Lewo_3.png",
                             "Lewo_1.png",
                             "Prawo_2.png",
                             "Filler_B1.png",
                             "Prawo_4.png",
                             "Lewo_2.png",
                             "Prawo_1.png",
                             "Filler_B2.png",
                             "Lewo_4.png",
                             "Prawo_3.png"]

    def get_first_image(self):
        self.current_image_index = 0
        image = Image(self.images_names[0])
        self.current_image_index += 1

        return image

    def get_next_image(self):
        image = Image(self.images_names[self.current_image_index])
        print(image.answer)
        self.current_image_index += 1
        return image

    def isNextImageAvaiable(self):
        return not (self.current_image_index >= len(self.images_names))

class Image:
    def __init__(self, file_name):
        self.LEFT_ANSWER = "Lewo"
        self.RIGHT_ANSWER = "Prawo"

        self.file_name = file_name
        self.image_pixmap = QPixmap("images/" + file_name)
        self.answer = ""

        match file_name.split("_")[0]:
            case self.LEFT_ANSWER:
                self.answer = TEXT_TO_EXCEL_RIGHT_ANSWER
            case self.RIGHT_ANSWER:
                self.answer = TEXT_TO_EXCEL_LEFT_ANSWER
            case _:
                # for "Filler" answers
                self.answer = TEXT_TO_EXCEL_FILLER_ANSWER
