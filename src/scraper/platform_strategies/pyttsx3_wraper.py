import pyttsx3
from src.scraper.downloader import DownloadManager


class TTS:
    def __init__(self, rate, volume, gender):
        self.engine = pyttsx3.init()
        self.dl = DownloadManager()

        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)  # [0,1] range

    def dl_text(self, text, file_name):
        self.engine.save_to_file(text, f'{self.dl.dl_root()}/audio/{self.dl.get_rand_id()}_{file_name}.mp3')
        self.engine.runAndWait()
