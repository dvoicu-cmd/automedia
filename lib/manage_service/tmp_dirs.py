import tempfile
import os


class TmpDir:
    """
    Wrapper class to python's temp file module for encapsulating the creating of directories.
    """
    def __init__(self):
        # Create a temporary directory
        temp_dir = tempfile.TemporaryDirectory()

        # Use the temporary directory
        temp_file_path = os.path.join(temp_dir.name, 'temp_file.txt')
        with open(temp_file_path, 'w') as temp_file:
            temp_file.write('This is a temporary file.')

        # Do your work with the temporary file...

        # Delete the temporary directory and its contents when done
        temp_dir.cleanup()

    def done(self):
        pass
