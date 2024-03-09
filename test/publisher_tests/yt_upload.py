from context import src
from src.publisher.platform_strategies.yt_upload import YtUpload

def test_2fa():
    print("calling yt")
    yt = YtUpload("dvmedia00@gmail.com", "d", "")

# def test_upload():
#     yt = YtUpload("dvmedia00@gmail.com", "XXm7E81IVk")
#     yt.select_account("deepfried")
#     yt.enable_thumbnail("/Users/dvoicu/mnt/Goofy Aughhh Test Files copy/Aughhhhh.png")
#     yt.set_title("Real posting")
#     yt.set_tags("Not,okay,delete,soon")
#     yt.set_description("2mls of water will do the trick")
#     yt.toggle_paid_promotions()
#     yt.exec_upload("/Users/dvoicu/When2HrOfSleep.mp4")


test_2fa()
