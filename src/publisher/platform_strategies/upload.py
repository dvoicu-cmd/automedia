from abc import ABC, abstractmethod


class Upload(ABC):
    @abstractmethod
    def exec_upload(self, file_path):
        """
        executes the upload for a specific file path
        :param file_path:
        :return:
        """
        pass
