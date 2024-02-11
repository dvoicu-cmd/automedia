import cv2
from src.creator.canvas import *
from src.creator.thumbnail.thumbnail_text import ThumbnailText


class MakeThumbnail:
    def __init__(self, canvas: CanvasInit):
        self.image = cv2.imread(canvas.canvas_path())

    def place_img(self, img_path, resize: tuple, position: tuple):
        """
        Places an image
        :param img_path:
        :param resize:
        :param position:
        :return:
        """
        additional_image = cv2.imread(img_path)  # Load the img
        additional_image = cv2.resize(additional_image, resize)  # Resize the img

        height, width, _ = additional_image.shape
        x2, y2 = position[0] + width, position[1] + height

        self.image[position[0]:x2, position[1]:y2] = additional_image  # attach image

    def place_text(self, t: ThumbnailText):
        """
        Places text given the params from text object
        :param t:
        :return:
        """
        cv2.putText(self.image, t.text_content, t.position, t.font, t.font_scale, t.font_color, t.thickness)

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

