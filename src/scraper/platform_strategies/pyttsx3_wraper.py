import pyttsx3
from lib.manage_directory_structure.scraper_dir_manager import ScraperDirManager


class TTS:
    def __init__(self, rate, volume):
        """

        :param rate:
        :param volume:
        """
        self.engine = pyttsx3.init()
        self.dl = ScraperDirManager()

        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)  # [0,1] range

    def dl_text(self, text, file_name, path_dir_output=''):
        """
        Works only on linux distros.
        :param text:
        :param file_name:
        :param path_dir_output:
        :return:
        """
        self.engine.save_to_file(text, f'{path_dir_output}/audio/{self.dl.get_rand_id()}_{file_name}.mp3')
        self.engine.runAndWait()
