import os
import sys

from lib.manage_formula.manage_formula import ManageFormula
from lib.cli_interface.page.input_pages import InputPage
from lib.cli_interface.page.picker_pages import PickerPage
from lib.cli_interface.page.display_page import DisplayPage


class PublisherFormulas:
    def __init__(self):
        pass

    def create_formula(self, formula_method: str, *args):
        match formula_method:
            case "yt":
                self.yt_formula()
            case _:
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

        DisplayPage().prompt(f"Successfully created new formula: {service_name}")


    @staticmethod
    def local_formula():
        f = ManageFormula()
        service_name = InputPage("Input the name of the service").prompt()
        number_records = InputPage("Input the number of media files to pull per service call.").prompt()
        account_id = InputPage("Input the account id to pull media files from").prompt()
        dir_name = InputPage("Input a name for the directory to export to.").prompt()

        f.ap(f"""
# init objs
lp = LocalPublish()
db_nas = DbNasConnection()
# set the destination to be just outside the project
cwd = os.getcwd()
cd_to_desired_root(cwd, "automedia")
os.chdir('..')
outside_dir_path = os.getcwd()
output_dir = outside_dir_path+"/automedia_exports"
specific_target_dir = output_dir+"{dir_name}"

# make the exports directory if it does not exist
try:
    os.mkdir(output_dir)
except FileExistsError:
    pass
    
# make the export dir for this service if it does not exist
try:
    os.mkdir(specific_target_dir)
except FileExistsError:
    pass
    
# Change back.
os.chdir(cwd)

# Start pulling records
i = 0

for i in range({number_records}):
    # get the record
    record = db_nas.read_rand_content_file({account_id})
    if record is None:
        break  # break out the loop if you have an empty record.
    # get the file path for the content file
    lp.set_src_path(record[1])
    # exec publish
    lp.exec_upload(specific_target_dir)
    # archive
    db_nas.update_to_archived('content_files', record[0])

        """)

        f.save_generated_script(service_name)

        DisplayPage().prompt(f"Successfully created new formula: {service_name}")
        pass
