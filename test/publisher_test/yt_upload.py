from context import src

from src.publisher.platform_strategies.yt_upload import YtUpload

def test_login():
    yt = YtUpload("dvmedia00@gmail.com", "", "/usr/bin/google-chrome")


test_login()
