import cv2
import random
import numpy as np
from src.creator.canvas import *
from src.creator.thumbnail.thumbnail_text import ThumbnailText
import pdb


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

    def place_text(self, t: ThumbnailText, random_bg=False, y_spacing=55):
        """
        Places text given the params from text object
        :param t:
        :param random_bg: option to turn on sporadic background highlights. ie: randomly apply background highlights.
        :param y_spacing: optional variable to increase the y-axis spacing on the thumbnails of text.
        :return:
        """
        lines = t.text_content.split('\n')

        # If you want to apply sporadic background highlights, have the random_bg variable turned on.
        apply_bg = True

        j = 0
        for i, line in enumerate(lines):

            # extra spacing for y to
            j = j + y_spacing

            if random_bg:
                apply_bg = random.choice([True, False])

            if t.has_bg and apply_bg:
                # https://aiphile.blogspot.com/2021/08/draw-transparent-shape-text-with.html
                # Copy img
                overlay = self.image.copy()

                # Get text size
                (t_w, t_h), _ = cv2.getTextSize(line, t.font, t.font_scale, t.font_thickness)

                # get the text pos of the word
                x = t.position[0]
                y = t.position[1] + i*(t.font_scale*20) + j

                # get the padding of the text
                x_pad = t.bg_padding[0]
                y_pad = t.bg_padding[1]

                # Draw in the rectangle
                cv2.rectangle(overlay, (x-x_pad, y+y_pad), (x+t_w+x_pad, y-t_h-y_pad), t.bg_color, -1)

                # Overlay the rectangle onto the img
                new_img = cv2.addWeighted(overlay, t.bg_opacity, self.image, 1 - t.bg_opacity, 0)

                # Put in the text
                cv2.putText(new_img, line, (t.position[0], t.position[1] + i*(t.font_scale*20) + j), t.font, t.font_scale, t.font_color, t.font_thickness)

                self.image = new_img
            else:
                # Just place the text
                cv2.putText(self.image, line, (t.position[0], t.position[1] + i*(t.font_scale*20) + j), t.font, t.font_scale, t.font_color, t.font_thickness)

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

