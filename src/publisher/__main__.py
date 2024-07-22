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
        v2 = PickerPage(["YT Formula", "Local Formula", "Back"]).prompt("Select a formula to use")
        try:
            if v2 == 0:
                PublisherFormulas().yt_formula()
            if v2 == 1:
                PublisherFormulas().local_formula()
            if v2 == 2:
                pass
        except Exception as e:
            if isinstance(e, InputCancelled):
                InputPage("").print_cancelled_input()
            else:
                DisplayPage().prompt(pg.str_exception(e))

    if v1 == 'manual':

        v2 = PickerPage(["Random Content Files",
                         "Multiple Content Files",
                         "Specific Content File",
                         ]).prompt("Manually Publishing a Content File.\nSelect an option.")
        if v2 == 0:  # random content files
            try:
                account_id = InputPage("Publishing Random Content File.\nInput the account id").prompt()
                num_media_exports = InputPage("Input the number of media files to export").prompt()

                # init objs
                lp = LocalPublish()
                db_nas = DbNasConnection()
                # set the destination to be just outside the project
                output_dir = export_dir()

                i = 0
                triggered_exception = False
                stored_exception = ""
                for i in range(num_media_exports):
                    # get the record
                    try:
                        record = db_nas.read_rand_content_file(account_id)
                    except Exception as e:
                        triggered_exception = True
                        stored_exception = e
                        return
                    # get the file path for the content file
                    lp.set_src_path(record[1])
                    # exec publish
                    lp.exec_upload(output_dir)
                    # archive
                    db_nas.update_to_archived('content_files', record[0])

                # Display success
                if triggered_exception:
                    DisplayPage().prompt(
                        f"Published {i} content file(s) locally. \n\n"
                        f"An exception occurred while executing: {pg.str_exception(stored_exception)}"
                    )
                else:
                    DisplayPage().prompt(f"Published {i} content file(s) locally")

            except Exception as e:
                if isinstance(e, InputCancelled):
                    InputPage("").print_cancelled_input()
                else:
                    DisplayPage().prompt(pg.str_exception(e))

        if v2 == 1:  # specific content file
            try:
                account_id = InputPage("Publishing Specific Content File.\nInput the account id").prompt()
                # init objs
                lp = LocalPublish()
                db_nas = DbNasConnection()

                # get all records
                record_all = db_nas.read_all_content_files_of_account(account_id)

                # format the string
                records_str = ''
                for record in record_all:
                    records_str = records_str + record + "\n"

                publish_id = InputPage(records_str+"\n\nAbove are all associated content files.\nInput the id of the one you wish to publish locally.").prompt()

                record = db_nas.read_specific_content_file_by_id(publish_id)


                # get the file path for the content file
                lp.set_src_path(record[1])

                # Get output dir
                output_dir = export_dir()

                # exec publish
                lp.exec_upload(output_dir)

                # archive
                db_nas.update_to_archived('content_files', record[0])

                DisplayPage().prompt("Published new content locally")

            except Exception as e:
                if isinstance(e, InputCancelled):
                    InputPage("").print_cancelled_input()
                else:
                    DisplayPage().prompt(pg.str_exception(e))


def export_dir():
    """
    Helper function for creating and returning the path of the local publishing exporting directory.
    :return: Str path of the exporting directory.
    """
    # set the destination to be just outside the project
    cwd = os.getcwd()
    cd_to_desired_root(cwd, "automedia")
    os.chdir('..')
    outside_dir_path = os.getcwd()
    output_dir = f"{outside_dir_path}/automedia_exports"

    # make the exports directory if it does not exist
    try:
        os.mkdir(output_dir)
    except FileExistsError:
        pass

    # Change back.
    os.chdir(cwd)
    return output_dir

if __name__ == '__main__':
    main()
