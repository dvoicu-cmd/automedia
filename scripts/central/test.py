from db_nas_connection import DbNasConnection
import unittest

# constants
# platforms:
TIKTOK = "tiktok"
YOUTUBE_SHORT = "yt_shorts"
YOUTUBE_VIDEO = "yt_videos"
REELS = "instagram_reels"
    
# media types:
VIDEO = "video"
AUDIO = "audio"
TEXT = "text"
IMAGE = "image"

# db connection
db_nas_conn = DbNasConnection()


# TEST CASES #
class DbNasConnectionTESTS(unittest.TestCase):
    # assertEqual()
    # assertTrue()
    # assertFalse()
    # assertRaises()

    @staticmethod
    def test_create_account():
        """
        tests if a record for a media file is created
        """
        email = "danny@com.com"
        username = "deepfri"
        platform = YOUTUBE_SHORT
        password = "HeheheHa"
        db_nas_conn.create_account(email, username, platform, password)

# Some of the tests gotta check the database yourself to see if the test ran.
# Better to run tests individually
if __name__ == '__main__':
    unittest.main()