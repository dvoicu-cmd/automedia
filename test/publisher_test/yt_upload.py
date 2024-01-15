from context import src

from src.publisher.platform_strategies.yt_upload import YtUpload
import pdb

def test_login():
    yt = YtUpload("dvmedia00@gmail.com", "")
    yt.select_account("heeheehaw")
    yt.enable_thumbnail("/Users/dvoicu/mnt/Goofy Aughhh Test Files copy/Lyra IV.png")
    yt.set_title("Fake")
    yt.set_tags("Not,okay,delete,soon")
    yt.set_description("2mls of water will do the trick")
    yt.toggle_paid_promotions()
    yt.exec_upload("/Users/dvoicu/When2HrOfSleep.mp4")
    pdb.set_trace()


test_login()
