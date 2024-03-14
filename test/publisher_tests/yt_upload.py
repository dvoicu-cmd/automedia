from context import src
from src.publisher.platform_strategies.yt_upload import YtUpload

def test_2fa():
    print("calling yt")
    yt = YtUpload("redditreadcreators@gmail.com", "qR1kYbTD7R", "ybq3joz5rckh4bvybe4fpgloqffgsyf2")
    print("SUCCESS Logged in headless")

def test_upload():
    print("Calling yt")
    yt = YtUpload("dvmedia00@gmail.com", "1Z078abFsD", "7orz4ydvf4ckslx3xvaiat2hmph6bib5", max_try=50)
    print("Successfully created obj and logged in")

    yt.select_account("deepfried")
    yt.enable_thumbnail("/Users/dvoicu/mnt/GoofyTestFiles/Aughhhhh.png")
    yt.set_title("Real posting")
    yt.set_tags("Not,okay,delete,soon")
    yt.set_description("2mls of water will do the trick")
    yt.toggle_paid_promotions()

    print("exec upload")
    yt.exec_upload('/Users/dvoicu/mnt/GoofyTestFiles/Edging my Brain AAUUGHeurysm-MnX2XOjdcWg.mp4')
    print("success on upload")
    yt.quit()


test_upload()
