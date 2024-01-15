from context import src

from src.publisher.platform_strategies.yt_upload import YtUpload

def test_login():
    yt = YtUpload("dvmedia00@gmail.com", "") # you thought
    yt.select_account("arghhh")
    yt.exec_upload("/Users/dvoicu/When2HrOfSleep.mp4")


test_login()
