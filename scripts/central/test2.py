from db_nas_connection import DbNasConnection

def main():
    make_media_pool()

def make_account():
    """
    Test for making an account
    """
    db = DbNasConnection()
    db.create_account("dvocCreatesPART2","dvoc@test.com", "Do you know the way?", "yt_shorts",
                      "THIS is a long description of what will be created here on this database of a thing")

    db.create_account("","", "", "yt_shorts",
                      "")

def make_media():
    db = DbNasConnection()
    db.create_media_file("/location","text","He who goes out there","a small description of what to put in here")

def make_media_pool():
    db = DbNasConnection()
    db.create_media_pool("OpenAI api calls", "Text files from open AI")


main()