from WatchUI.IBasics.Basics import Basics
import time
import cv2 as cv
from skimage.metrics import structural_similarity
import imutils


class Image(Basics):
    def create_compare_images(self, path1: str, path2: str, save_folder: str, ssim: float, image_format: str) -> None:
        save_folder = self.check_dir(save_folder)
        ssim = self.check_ssim(ssim)
        img_format = self.check_image_format(image_format)
        self.check_image_exists(path1)
        self.check_image_exists(path2)

        # Compare image
        img1 = cv.imread(path1, 1)
        img2 = cv.imread(path2, 1)

        # convert to grey
        gray_img1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
        gray_img2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)

        # SSIM diff Img
        (score, diff) = structural_similarity(gray_img1, gray_img2, full=True)
        diff = (diff * 255).astype("uint8")

        # Threshold diff Img
        thresh = cv.threshold(diff, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
        cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # Create frame in diff area
        for c in cnts:
            (x, y, w, h) = cv.boundingRect(c)
            cv.rectangle(img1, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 2)

        time_ = str(time.time())
        url = save_folder + "/Img" + time_ + img_format
        # Show image
        if float(score) < ssim:
            cv.imwrite(url, img2)
            self.set_log_message(work_object="Image", type_of_messages="Error", path_to_image=url)
        else:
            img_diff = cv.hconcat([img1, img2])
            cv.imwrite(url, img_diff)
            self.set_log_message(work_object="Image", type_of_messages="Info", path_to_image=url)

    def create_compare_screen_without_areas(self, path1: str, path2: str, *args, save_folder: str, ssim: float, image_format: str) -> None:
        save_folder = self.check_dir(save_folder)
        mySsim = self.check_ssim(ssim)
        img_format = self.check_image_format(image_format)

        lt = len(args)
        img1 = cv.imread(path1, 1)
        img2 = cv.imread(path2, 1)

        self.check_if_args_has_ok_numbers(*args, need_numbers=4)

        x = lt / 4
        i = 0
        a = 0
        while i < x:
            color = (0, 0, 0)
            x1 = int(args[0 + a])
            y1 = int(args[1 + a])
            x2 = int(args[2 + a])
            y2 = int(args[3 + a])

            cv.rectangle(img1, (x1, y1), (x2, y2), color, -1)
            cv.rectangle(img2, (x1, y1), (x2, y2), color, -1)
            a += 4
            i += 1

            # convert to grey
            gray_img1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
            gray_img2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)

            # SSIM diff Img
            (score, diff) = structural_similarity(
                gray_img1, gray_img2, full=True
            )
            diff = (diff * 255).astype("uint8")

            # Threshold diff Img
            thresh = cv.threshold(
                diff, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU
            )[1]
            cnts = cv.findContours(
                thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE
            )
            cnts = imutils.grab_contours(cnts)

            # Create frame in diff area
            for c in cnts:
                (x, y, w, h) = cv.boundingRect(c)
                cv.rectangle(img1, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Show image
            time_ = str(time.time())
            url = save_folder + "/Img" + time_ + img_format
            if float(score) < mySsim:
                cv.imwrite(url, img2)
                self.set_log_message(work_object="Image", type_of_messages="Error", path_to_image=url)
            else:
                img_diff = cv.hconcat([img1, img2])
                cv.imwrite(url, img_diff)
                self.set_log_message(work_object="Image", type_of_messages="Info", path_to_image=url)

    def create_crop_image(self, path: str, x1: int, y1: int, x2: int, y2: int, save_folder: str, image_format: str):
        self.check_image_exists(path)
        save_folder = self.check_dir(save_folder)
        img_save_format = self.check_image_format(image_format)

        img = cv.imread(path, 1)
        crop_img = img[int(x1):int(x2), int(y1):int(y2)]  # Crop from {x, y, w, h } => {0, 0, 300, 400}

        # Save image
        url = save_folder + "/Img" + str(time.time()) + img_save_format
        cv.imwrite(url, crop_img)
        self.set_log_message(work_object="Image", type_of_messages="Info", path_to_image=url)

    def create_rotate_image(self, path: str, screen_name: str, save_folder: str, rotate: int, image_format: str) -> None:
        save_folder = self.check_dir(save_folder)
        img_format = self.check_image_format(image_format)
        self.check_image_exists(path)

        img = cv.imread(path)
        if int(rotate) == 0:
            rotate_image = cv.rotate(img, cv.ROTATE_90_CLOCKWISE)
            cv.imwrite(save_folder + '/' + screen_name + img_format, rotate_image)
        elif int(rotate) == 1:
            rotate_image = cv.rotate(img, cv.ROTATE_90_COUNTERCLOCKWISE)
            cv.imwrite(save_folder + '/' + screen_name + img_format, rotate_image)
        elif int(rotate) == 2:
            rotate_image = cv.rotate(img, cv.ROTATE_180)
            cv.imwrite(save_folder + '/' + screen_name + img_format, rotate_image)
        else:
            raise AssertionError("You try to setup volume:" + str(rotate) +
                                 " which never exists. Please read documentations and try 0,1 or 2.")