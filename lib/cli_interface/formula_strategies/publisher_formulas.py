import os
import sys

from lib.manage_formula.manage_formula import ManageFormula
from lib.cli_interface.page.input_pages import InputPage
from lib.cli_interface.page.picker_pages import PickerPage


class PublisherFormulas:
    def __init__(self):
        pass

    @staticmethod
    def yt_formula():
        f = ManageFormula()

        service_name = InputPage("Input the name of the service").prompt()
        name = InputPage("Input the name of the account you want to set up a YT publisher for").prompt()

        f.ap(f"""
        
db = DbNasConnection()
manager = PublisherDirManager()
exec_fail = False

# 0 -> id, 1 -> username, 2 -> email, 3 -> password, 4 -> auth_secrete, 5 -> platform, 6 -> description
acc_record = db.read_account_by_name('{name}')
acc_record = acc_record[0] # read_account_by_name returns a tuple of tuples. why, idk

# 0 -> id, 1 -> file location, 2 -> title, 3 -> description, 4 -> to archive, rest of the attributes are not important...
content_record = db.read_rand_content_file(acc_record[0])  # Reads the content.

# Set up uploader
yt = None
try:
    yt = YtUpload(acc_record[2], acc_record[3], acc_record[4])
except:
    exec_fail = True
    pass

yt.set_account(acc_record[1])
yt.set_title(content_record[2])
yt.set_description(content_record[3])

# organize files
file_path = content_record[1]  # Expected directory with video and thumbnail.
        
        """)

        f.ap("""
        
# set thumbnail (if verified)
try:
    yt.enable_thumbnail(f"{db.nas_root()}/{file_path}/thumbnail.jpg")
except:
    pass
    
# try to upload short video (if there is one)
try:
    yt.exec_upload(f"{db.nas_root()}/{file_path}/short.mp4")
except:
    pass

# exec
try:
    yt.exec_upload(f"{db.nas_root()}/{file_path}/video.mp4")
except:
    exec_fail = True
    pass

yt.quit() # quit the driver to save memory. Like this is super important.

# Set to archive
if not exec_fail:
    db.update_to_archived('content_files', content_record[0])
        
        """)

        f.save_generated_script(service_name)
        print(200)
