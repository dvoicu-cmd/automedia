from db_nas_connection import DbNasConnection

def main():
    make_junktion_entry()

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

def make_content_file():
    db = DbNasConnection()
    db.create_content("/location \here/Yeah","Big Man Doinks", "LIKE AND SUBSCRIBE HAHAHAHAHA")

def make_junktion_entry():
    db = DbNasConnection()
    db.create_junction_entry("j_accounts__content_files","1","1")
    # db.create_junction_entry("j_accounts__content_files","1","2") # This should be an error if there is no content file with id 2
    db.create_junction_entry("j_accounts__media_files","1","1")
    db.create_junction_entry("j_aunts__media_files33", "1", "1")



main()