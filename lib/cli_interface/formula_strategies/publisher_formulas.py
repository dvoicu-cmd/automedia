from .formulas_interface import InterfaceFormulas

from lib.manage_formula.manage_formula import ManageFormula
from lib.cli_interface.page.input_pages import InputPage
from lib.cli_interface.page.picker_pages import PickerPage


class PublisherFormulas(InterfaceFormulas):

    def create_formula(self, formula_method: str, attr_map={}):
        if formula_method == "yt_formula":
            self.yt_formula(attr_map=attr_map)
        if formula_method == "yt_schedule":
            self.yt_schedule(attr_map=attr_map)
        if formula_method == "local_formula":
            self.local_formula(attr_map=attr_map)

    # -------------------------------------- Formulas --------------------------------------

    @staticmethod
    def yt_formula(attr_map={}):
        f = ManageFormula()
        f.set_properties_type("publisher", "yt_formula")

        service_name = InterfaceFormulas().formula_name(f, attr_map)

        yt_account_name = InputPage("Input the name of the account you want to set up a YT publisher for").prompt(default_value=attr_map.get("name"))
        f.spa("name", yt_account_name)

        brand_account = InputPage("Input the specific brand account to select for your upload").prompt(default_value=attr_map.get("brand_account"))
        f.spa("brand_account", brand_account)

        f.ap(f"""
        
db = DbNasConnection()
manager = PublisherDirManager()

# 0 -> id, 1 -> username, 2 -> email, 3 -> password, 4 -> auth_secrete, 5 -> platform, 6 -> description
acc_record = db.read_account_by_name('{yt_account_name}')
acc_record = acc_record[0]  # read_account_by_name returns a tuple of tuples. why, idk

# 0 -> id, 1 -> file location, 2 -> title, 3 -> description, 4 -> to archive, rest of the attributes are not important...
content_record = db.read_rand_content_file(acc_record[0])  # Reads the content.

# var to see if the execution fails.
exec_fail = False

# Set up uploader
yt = None
try:
    yt = YtUpload(acc_record[2], acc_record[3], acc_record[4])
except:
    exec_fail = True
    pass

# Input select the specific brand account to upload to.
target_brand_account = "{brand_account}"
        
        """)

        f.ap("""

# Organize and set up the files.
file_path = content_record[1]  # Expected directory with video, title, description and thumbnail.

# Get abs file path then set the properties from the read record
title = f"{db.nas_root()}/{file_path}/title.txt"
description = f"{db.nas_root()}/{file_path}/desc.txt"
thumbnail = f"{db.nas_root()}/{file_path}/thumbnail.jpg"
video = f"{db.nas_root()}/{file_path}/video.mp4"
short = f"{db.nas_root()}/{file_path}/short.mp4"

yt.set_account(target_brand_account)  # Target brand account
yt.set_title(TextUtils.read_txt(title))
yt.set_description(TextUtils.read_txt(description))
yt.enable_thumbnail(thumbnail)  # Attempt to set up the thumbnail (if verified)
    
# try to upload short video (if there is one)
try:
    print("Starting exec upload short")
    yt.exec_upload(short)
    print("Finished upload short")
except Exception as e:
    print(e)
    pass

# exec
try:
    print("Starting exec main video")
    yt.exec_upload(video)
    print("Finished upload main video")
except Exception as e:
    print("Error")
    print(e)
    exec_fail = True
    pass

yt.quit()  # quit the driver to save memory. Like this is super important.

# Set to archive
if not exec_fail:
    db.update_to_archived('content_files', content_record[0])
        
        """)

        f.save_generated_script(service_name)

    @staticmethod
    def yt_schedule(attr_map={}):
        f = ManageFormula()
        f.set_properties_type("publisher", "yt_schedule")
        service_name = InterfaceFormulas().formula_name(f, attr_map)

        # Account information
        yt_account_name = InterfaceFormulas.formula_input("yt_account_name",
                                                          "Input the name of the account you want to set up a YT publisher for",
                                                          f, attr_map)
        f.spa("yt_account_name", yt_account_name)

        # The brand account to upload videos to on youtube studio.
        brand_account = InputPage("Input the specific brand account to select for your upload").prompt(default_value=attr_map.get("brand_account"))
        f.spa("brand_account", brand_account)

        # Number of videos to schedule
        number_videos = InterfaceFormulas.formula_input("number_videos",
                                                        "Input the number of videos you wish to schedule an upload. This will schedule a video per day.",
                                                        f, attr_map)
        f.spa("number_videos", number_videos)

        # Specific time to schedule
        time_to_schedule = InterfaceFormulas. formula_input("time_to_schedule",
                                                            "Input the time for an upload to be scheduled. \nAccepted format: TT:TT AA, ex: 12:30 AM, 6:00 PM",
                                                            f, attr_map)
        f.spa("time_to_schedule", time_to_schedule)

        f.ap(f"""
        
db = DbNasConnection()
manager = PublisherDirManager()

# Set up the scheduling
time_to_schedule = "{time_to_schedule}"  # Time
if not YtUpload.is_valid_time_format(time_to_schedule):
    raise SyntaxError("Invalid Schedule Time")
dates_list = YtUpload.ls_days_ahead({number_videos})  # list of dates ahead given the specified number of videos.

# Read the google account information.
# 0 -> id, 1 -> username, 2 -> email, 3 -> password, 4 -> auth_secrete, 5 -> platform, 6 -> description
acc_record = db.read_account_by_name('{yt_account_name}')
acc_record = acc_record[0]  # read_account_by_name returns a tuple of tuples. why, idk


# Set up uploader
yt = None
try:
    yt = YtUpload(acc_record[2], acc_record[3], acc_record[4])
except:
    # You don't want to continue if you fail to set up the youtube webdriver
    raise ChildProcessError("YT Upload failed to be set up")

# var to see if execution fails.
exec_fail = False

# Start scheduling
for date in dates_list:
    # 0 -> id, 1 -> file location, 2 -> title, 3 -> description, 4 -> to archive, rest of the attributes are not important...
    content_record = db.read_rand_content_file(acc_record[0])  # Reads the content.

    # Input select the specific brand account to upload to.
    target_brand_account = "{brand_account}"    
        """)

        f.ap("""

    # Organize and set up the files.
    file_path = content_record[1]  # Expected directory with video, title, description and thumbnail.

    # Get abs file path then set the properties from the read record
    title = f"{db.nas_root()}/{file_path}/title.txt"
    description = f"{db.nas_root()}/{file_path}/desc.txt"
    thumbnail = f"{db.nas_root()}/{file_path}/thumbnail.jpg"
    video = f"{db.nas_root()}/{file_path}/video.mp4"
    short = f"{db.nas_root()}/{file_path}/short.mp4"

    yt.set_account(target_brand_account)  # Target brand account
    yt.set_title(TextUtils.read_txt(title))
    yt.set_description(TextUtils.read_txt(description))
    yt.enable_schedule(time_to_schedule, date)
    yt.enable_thumbnail(thumbnail)  # Attempt to set up the thumbnail (if verified)
    
    try:
        print("Starting exec upload short")
        yt.exec_upload(short)
        print("Finished upload short")
    except Exception as e:
        if not isinstance(e, ValueError):
            print("Error for uploading short not value error. Exiting Early")
            print(e)
            break
        else:
            print(e)
            pass

    # exec
    try:
        print("Starting exec main video")
        yt.exec_upload(video)
        print("Finished upload main video")
    except Exception as e:
        print("Error was raised")
        print(e)
        exec_fail = True
        pass
        
    # Set to archive
    if not exec_fail:
        db.update_to_archived('content_files', content_record[0])
    else:
        break  # If something is actually wrong, stop the needless work.

yt.quit()  # quit the driver to save memory after scheduling. Like this is super important.

        """)

        f.save_generated_script(service_name)

        pass

    @staticmethod
    def local_formula(attr_map={}):
        f = ManageFormula()
        f.set_properties_type("publisher", "local_formula")

        formula_name = InterfaceFormulas.formula_name(f, attr_map)

        number_records = InputPage("Input the number of media files to pull per service call.").prompt(default_value=attr_map.get("number_records"))
        f.spa("number_records", number_records)

        account_id = InputPage("Input the account id to pull media files from").prompt(default_value=attr_map.get("account_id"))
        f.spa("account_id", account_id)

        dir_name = InputPage("Input a name for the directory to export to.").prompt(default_value=attr_map.get("dir_name"))
        f.spa("dir_name", dir_name)


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
specific_target_dir = output_dir+"/{dir_name}"

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
    path = ""+db_nas.nas_root()+"/"+record[1]
    lp.set_src_path(path)
    # exec publish
    lp.exec_upload(specific_target_dir)
    # archive
    db_nas.update_to_archived('content_files', record[0])

        """)

        f.save_generated_script(formula_name)

