import requests
import os
import shutil
import pickle

from .dir_manager import DirManager


class ScraperDirManager(DirManager):
    """
    Manages all the downloads from the various strategies in the scraper unit
    """

    def dl_list_of_links(self, links, content_type, name, output_tmp_dir_path):
        """
        Downloads a list of links
        """
        for link in links:
            self.new_rand_id()
            self.dl_via_link(link, content_type, name, output_tmp_dir_path)

    def dl_via_link(self, link, content_type, name, output_tmp_dir_path):
        """
        Downloads audio, image, and video content
        """
        valid = ['audio', 'image', 'video']
        if content_type not in valid:
            raise ValueError(f"Invalid content type: {content_type}")

        # determine the file extension
        fs_extension = ''
        if content_type == 'audio':
            fs_extension = '.mp3'
        elif content_type == 'image':
            fs_extension = '.jpg'
        elif content_type == 'video':
            fs_extension = '.mp4'

        response = requests.get(link)
        if response.status_code == 200:
            with open(f"{output_tmp_dir_path}/{self.rand_hash}_{name}{fs_extension}", "wb") as f:
                f.write(response.content)
        else:
            ProcessLookupError(f"Failed to download contents. Response code:{response.status_code}")

    def dl_list_of_text(self, text_list, name, output_tmp_dir_path):
        for text in text_list:
            self.new_rand_id()
            self.dl_text(text, name, output_tmp_dir_path)

    def dl_text(self, text, name, output_tmp_dir_path):
        """
        Writes the string text into a file
        """
        with open(f"{output_tmp_dir_path}/{self.rand_hash}_{name}.txt", "w") as f:
            f.write(text)

    def save_cache(self, a1, a2):
        pass

    def load_cache(self, a1, a2):
        pass





