from context import src
from src.scraper.downloader import DownloadManager

dm = DownloadManager()
dm.dl_text("HE HE HE HA", "funny")
dm.dl_via_link("https://packaged-media.redd.it/594wwbq4jvcc1/pb/m2-res_480p.mp4?m=DASHPlaylist.mpd&v=1&e=1705528800&s=4a05e75bb29d0e7359280c47eed3743911971761#t=0",
               "video", "matpat goes nuts")
print(dm.select_dir('text'))
dm.clear_all()