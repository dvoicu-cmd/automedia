from context import src
from context import lib
from src.publisher.platform_strategies.yt_upload import YtUpload
from lib.central_connector.db_nas_connection import DbNasConnection
import time


def test_2fa():
    print("calling yt")
    yt = YtUpload("dannnytests@gmail.com", "3hngBguof0", "")
    print("SUCCESS Logged in headless")

def days():
    days_ls = YtUpload.ls_days_ahead(5)
    print(days_ls)


def test_upload():
    start_time = time.time()

    db = DbNasConnection()
    record = db.read_account_by_name("UrOpinionBruh")[0]
    print(record)

    print("Calling yt")
    yt = YtUpload(record[2], record[3], record[4])
    print("Successfully created obj and logged in")

    yt.set_account(record[1])
    yt.enable_thumbnail("/home/dv/Thumb.jpg")
    yt.set_title("Real posting")
    yt.set_tags("Not,okay,delete,soon")
    yt.set_description("2mls of water will do the trick")
    yt.toggle_paid_promotions()

    print("exec upload")
    yt.exec_upload("/Users/dvoicu/mnt/GoofyTestFiles/Edging my Brain AAUUGHeurysm-MnX2XOjdcWg.mp4")
    print("success on upload")
    yt.quit()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed Time: {elapsed_time}s")


days()
