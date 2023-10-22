"""
The parent class hosting
"""
from scripts.db.write_media_strategy.strategies.scrape_video import ScrapeVideo
from scripts.db.write_media_strategy.strategies.video_upload import VideoUpload


class DbWriteMedia():
    # content_type_selected = ["video_upload", "scrape_video", "scrape_audio", "scrape_image", "scrape_text"]


    def __init__(self):
        """
        Constructor method
        """

    def execute(self, conn, curr, account_id, content, content_type, location):
        writer = None
        match content_type:
            case "video_upload":
                writer = VideoUpload()
            case "scrape_video":
                writer = ScrapeVideo()
            case "scrape_audio":
                print("")
                # writer = ScrapeAudio()
            case "scrape_image":
                print("")
                # writer = ScrapeImage()
            case "scrape_text":
                print("")
                # writer = ScrapeText()
            case _:
                raise Exception("improper content_type format")
        writer.set(conn, curr, account_id, location)
        writer.write_to_nfs(content)