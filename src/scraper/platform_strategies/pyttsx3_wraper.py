import pyttsx3
from src.scraper.downloader import DownloadManager


class TTS:
    def __init__(self, rate, volume, gender):
        """

        :param rate:
        :param volume:
        :param gender:
        """
        self.engine = pyttsx3.init()
        self.dl = DownloadManager()

        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)  # [0,1] range

    def dl_text(self, text, file_name):
        """
        Works only on linux distros.
        :param text:
        :param file_name:
        :return:
        """
        self.engine.save_to_file(text, f'{self.dl.dl_root()}/audio/{self.dl.get_rand_id()}_{file_name}.mp3')
        self.engine.runAndWait()

    def say_text(self, text):
        voices = self.engine.getProperty('voices')
        for voice in voices:
            self.engine.setProperty('voice', voice.id)
            self.engine.say('The quick brown fox jumped over the lazy dog.')
        self.engine.runAndWait()

        self.engine.say(text, "say_text")
        self.engine.runAndWait()
