from WatchUI.IBasics.Basics import Basics
import cv2 as cv
import pytesseract
import os


class Tesseract(Basics):
    def create_image_to_string(self, path: str, oem: str, psm: str, language: str, path_to_tesseract: str):
        self.check_image_exists(path)

        old_img = cv.imread(path)
        pytesseract.pytesseract.tesseract_cmd = self.check_tess_path(path_to_tesseract)
        custom_oem_psm_config = r'--oem ' + oem + ' --psm ' + psm
        text = pytesseract.image_to_string(old_img, config=custom_oem_psm_config, lang=language)
        return text

    def create_image_area_on_text(self, path: str, *coordinates, oem: str, psm: str, language: str, path_to_tesseract: str):
        string_list = []
        old_img = cv.imread(path)
        len_coordinates = len(coordinates)

        self.check_if_args_has_ok_numbers(*coordinates, need_numbers=4)
        if len_coordinates / 4 == 1:
            crop_img = old_img[int(coordinates[1]): int(coordinates[3]),
                       int(coordinates[0]): int(coordinates[2])]
            pytesseract.pytesseract.tesseract_cmd = self.check_tess_path(path_to_tesseract)
            custom_oem_psm_config = r'--oem ' + oem + ' --psm ' + psm
            text = pytesseract.image_to_string(crop_img, config=custom_oem_psm_config, lang=language)
            text = os.linesep.join([s for s in text.splitlines() if s])                                 # delete blank line space
            return text
        else:
            num_coordinates = len_coordinates / 4
            a = 0
            i = 0
            while i < num_coordinates:
                x1 = coordinates[0 + a]
                y1 = coordinates[1 + a]
                x2 = coordinates[2 + a]
                y2 = coordinates[3 + a]
                crop_img = old_img[int(y1): int(y2), int(x1): int(x2)]
                pytesseract.pytesseract.tesseract_cmd = self.check_tess_path(path_to_tesseract)
                custom_oem_psm_config = r'--oem ' + oem + ' --psm ' + psm
                text = pytesseract.image_to_string(crop_img, config=custom_oem_psm_config, lang=language)
                string_list.append(text)
                i += 1
                a += 4
            return string_list
