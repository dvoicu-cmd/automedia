import shutil

from .upload import Upload


class LocalPublish(Upload):
    """
    Publishes a copy of the content files locally to a specified location
    """
    def __init__(self):
        self.src_path = '/'

    def set_src_path(self, src_path):
        self.src_path = src_path

    def exec_upload(self, file_path_dst):
        try:
            shutil.copytree(self.src_path, file_path_dst)
        except FileExistsError:  # If the dir already exists, just move instead the files.
            shutil.move(self.src_path, file_path_dst)
