import cv2
import numpy as np
from src.creator.canvas import *
from src.creator.thumbnail.thumbnail_text import ThumbnailText


class MakeThumbnail:
    def __init__(self, canvas: CanvasInit):
        self.image = cv2.imread(canvas.canvas_path())

    def place_img(self, img_path, resize: tuple, position: tuple):
        """
        Places an image
        :param img_path: The absolute path of the image you want to place
        :param resize: The tuple with (x,y). Where x -> the number of pixels that are horizontally scaling, y -> the number of pixels that are vertically scaling.
        :param position: The position to place the image relative to the top left corner of it. With the tuple (x,y) being the x and y position respectively.
        :return:
        """
        additional_image = cv2.imread(img_path)  # Load the img
        additional_image = cv2.resize(additional_image, resize)  # Resize the img

        height, width, _ = additional_image.shape
        x2, y2 = position[0] + width, position[1] + height

        self.image[position[1]:y2, position[0]:x2] = additional_image

    def place_text(self, t: ThumbnailText):
        """
        Places text given the params from text object
        :param t:
        :return:
        """
        lines = t.text_content.split('\n')
        for i, line in enumerate(lines):
            cv2.putText(self.image, line, (t.position[0], t.position[1] + i*(t.font_scale*20)), t.font, t.font_scale, t.font_color, t.thickness)

    @staticmethod
    def create_img_circle(img_path, radius):
        """
        Crops an image to a circle
        :param img_path:
        :param radius:
        :return:
        """
        # idk, stolen from stack over flow:
        # https://stackoverflow.com/questions/61516526/how-to-use-opencv-to-crop-circular-image

        # Load image
        image = cv2.imread(img_path)
        hh, ww = image.shape[:2]

        # Define circles
        xc = hh // 2
        yc = ww // 2

        # Define masks
        mask = np.zeros_like(image)
        mask = cv2.circle(mask, (xc, yc), radius, (255, 255, 255), -1)

        result = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        result[:, :, 3] = mask[:, :, 0]

        tmp = f"{img_path}_circle_crop.jpg"
        cv2.imwrite(tmp, result)

    def blur_current_img(self):
        """
        Blurs the current image
        :return:
        """
        self.image = cv2.GaussianBlur(self.image, (5, 5), 0)

    def write(self, mb_size: int, file_dir_path: str, file_name: str):
        """
        Writes the final image to a desired size.
        :param mb_size:
        :param file_dir_path:
        :param file_name:
        :return:
        """
        byte_size_target = 1024 * 1024 * mb_size

        for quality in range(100, 0, -1):
            _, encoded_image = cv2.imencode('.jpg', self.image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
            encoded_image_size = len(encoded_image)

            if encoded_image_size <= byte_size_target:
                decoded_image = cv2.imdecode(encoded_image, 1)
                cv2.imwrite(f"{file_dir_path}/{file_name}.jpg", decoded_image)
                break
            else:
                continue

