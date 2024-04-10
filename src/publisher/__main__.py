import os
from context import src
from context import lib
from src import *
from lib import *
from context import cd_to_desired_root


def main():
    pg.verify_cfg()
    v1 = pg.main_menu("Publisher")
    if v1 == 'custom':
        # CUSTOM PUBLISHER FORMULA CREATION
        PublisherFormulas().yt_formula()

    if v1 == 'manual':

        v2 = PickerPage(["Random Content File", "Specific Content File"]).prompt("Manually Publishing a Content File.\nSelect an option.")
        if v2 == 0:  # random content file
            account_id = InputPage("Publishing Random Content File.\nInput the account id").prompt()
            # init objs
            lp = LocalPublish()
            db_nas = DbNasConnection()

            # get the record
            record = db_nas.read_rand_content_file(account_id)

            # get the file path for the content file
            lp.set_src_path(record[1])

            # set the destination to be just outside the project
            cwd = os.getcwd()
            cd_to_desired_root(cwd, "automedia")
            os.chdir('..')
            output_dir = os.getcwd()
            os.chdir(cwd)

            # exec publish
            lp.exec_upload(output_dir)

            # archive
            db_nas.update_to_archived('content_files', record[0])

            print(200)


        if v2 == 1:  # specific content file
            account_id = InputPage("Publishing Specific Content File.\nInput the account id").prompt()
            # init objs
            lp = LocalPublish()
            db_nas = DbNasConnection()

            # get the record
            try:
                record_all = db_nas.read_all_content_files_of_account(account_id)
            except Exception as e:
                raise e

            # format the string
            records_str = ''
            for record in record_all:
                records_str = records_str + record + "\n"

            publish_id = InputPage(records_str+"\n\nAbove are all associated content files.\nInput the id of the one you wish to publish locally.").prompt()

            record = None
            try:
                record = db_nas.read_specific_content_file_by_id(publish_id)
            except Exception as e:
                raise e


            # get the file path for the content file
            lp.set_src_path(record[1])

            # set the destination to be just outside the project
            cwd = os.getcwd()
            cd_to_desired_root(cwd, "automedia")
            os.chdir('..')
            output_dir = os.getcwd()
            os.chdir(cwd)

            # exec publish
            lp.exec_upload(output_dir)

            # archive
            db_nas.update_to_archived('content_files', record[0])

            print(200)


if __name__ == '__main__':
    main()
