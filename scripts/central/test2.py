from db_nas_connection import DbNasConnection
import datetime

def main():

    delete_account()

    return

def delete_account():
    db = DbNasConnection()
    db.create_account("TheAccount", "myMail@co.com", "This is the password", "yt_shorts",
                      "The final test account",)
    db.create_content("/Users/dvoicu/mnt/Goofy Aughhh Test Files/When2HrOfSleep.mp4",
                      "2hr sleep", "LIKE COMMENT SUBSCRIBE HE HE HE HA", "TheAccount")
    db.create_content("/Users/dvoicu/mnt/Goofy Aughhh Test Files/Lyra IV.png",
                      "Far away land", "Follow my twitch", "TheAccount")
    db.create_media_pool("The asdf movie theft", "Stole asdf movie items")
    db.create_media_file("/Users/dvoicu/mnt/Goofy Aughhh Test Files/aughhh.txt", "text", "Hi",
                         "Stolen from tom", "The asdf movie theft")

    account = db.read_account_by_name("TheAccount")
    media_pool = db.read_media_pool_by_name("The asdf movie theft")

    db.create_link_account_to_media_pool(account[0][0], media_pool[0][0])

    db.create_account("TheOTHER", "myMail@HEHEHEHA.net", "This is the beginning of the song",
                      "yt_videos", "Men")

    db.create_content("/Users/dvoicu/mnt/Goofy Aughhh Test Files/Aughhhhh.png", "Spider",
                      "Spider but human", "TheOTHER")

    # db.delete_account(account[0][0])

    return



def delete_content_file():
    db = DbNasConnection()
    db.delete_content_file(2)

def delete_media_pool_empty():
    db = DbNasConnection()
    db.delete_media_pool(1)

    return

def delete_media_pool():
    db = DbNasConnection()

    db.create_media_pool("Cool Things", "Wow that was really cool")
    db.create_media_file("/Users/dvoicu/mnt/Goofy Aughhh Test Files/bard_db_lecture.txt","text",
                           "A lecture in databases","A lecture","Cool Things")
    db.create_media_file("/Users/dvoicu/mnt/Goofy Aughhh Test Files/Lyra IV.png","image",
                          "Lyra 42", "A far far far away planet","Cool Things")

    record_pool = db.read_media_pool_by_name("Cool Things")

    media_id = 5

    db.create_link_account_to_media_pool(1, media_id)

    db.delete_media_pool(record_pool[0][0])

def delete_media_file():
    db = DbNasConnection()
    # db.create_media_pool("Lectures", "He who goes there must learn")
    # db.create_media_file("/Users/dvoicu/mnt/Goofy Aughhh Test Files/bard_db_lecture.txt","text",
    #                      "A lecture in databases","A lecture","Lectures")
    record = db.read_specific_media_file("/Users/dvoicu/mnt/active/media_pools/Lectures/bard_db_lecture.txt")
    # print(record)
    db.delete_media_file(record[0])


def test_archive_media():
    db = DbNasConnection()
    db.create_media_pool("deep_fried_memes","A collection of deep fried memes")
    db.create_media_file("/Users/dvoicu/mnt/Goofy Aughhh Test Files/When2HrOfSleep.mp4","video",
                         "WhenThat24HoursOfSleepKicksIn","A Man Has Fallen","deep_fried_memes")
    db.create_media_file("/Users/dvoicu/mnt/Goofy Aughhh Test Files/aughhh.txt","text",
                         "Hi My Name is Auggh Text","Goofy Text","deep_fried_memes")
    record1 = db.read_specific_media_file("/active/media_pools/deep_fried_memes/When2HrOfSleep.mp4")
    record2 = db.read_specific_media_file("/active/media_pools/deep_fried_memes/aughhh.txt")
    db.update_to_archived("media_files", record1[0])
    db.update_to_archived("media_files", record2[0])
    # db.delete_all_archived_media_files()


def test_archive_content():
    db = DbNasConnection()
    db.create_account("iphon","wowifon@gmail.com","thumbsUp","tiktok","burner account")
    db.create_content("/Users/dvoicu/mnt/Goofy Aughhh Test Files/AUUGHHH Tik Tok Sound Effect.mp3",
                      "funny.mp4","A short and funny sound for all the viewers to see. Like and subscribe",
                      "iphon")
    db.create_content("/Users/dvoicu/mnt/Goofy Aughhh Test Files/Aughhhhh.png",
                      "spiderman dies", "He really did not want that",
                      "iphon")
    id_account = db.read_account_by_name("iphon")

    record_content = db.read_rand_content_file(id_account[0][0])
    db.update_to_archived("content_files", record_content[0])

    db.delete_all_archived_content_files()



# --------- NAS Integration ---------
def config_parser_test():
    db = DbNasConnection()
    print(db.make_connection_config("10.10.2.3","3306","test_user","password","test","/Users/dvoicu/mnt"))


# --------- UPDATE ---------
def update_to_unarchive():
    db = DbNasConnection()
    print(db.update_to_unarchived('media_files',2))


def update_to_archived_on_media_files():
    db = DbNasConnection()
    print(db.update_to_archived('media_files', 2))

def update_to_archived_on_accounts():
    db = DbNasConnection()
    print(db.update_to_archived('accounts', 1))

def update_to_archived_on_invalid_table():
    db = DbNasConnection()
    print(db.update_to_archived('heheheha',0))

def update_to_archived_on_invalid_id():
    db = DbNasConnection()
    print(db.update_to_archived('media_files',0))

# --------- READ ---------
def read_specific_media_file_by_name():
    db = DbNasConnection()
    print(db.read_specific_media_file("He who goes out there"))

def read_all_media_files_of_pool():
    db = DbNasConnection()
    print(db.read_all_media_files_of_pool(2))

def read_rand_media_file_of_pool():
    db = DbNasConnection()
    print(db.read_rand_media_file_of_pool(2))

def read_media_pool_by_name():
    db = DbNasConnection()
    print(db.read_media_pool_by_name("OpenAI api calls"))

def read_media_pools_of_account():
    db = DbNasConnection()
    print(db.read_media_pools_of_account(1))

def read_specific_content():
    db = DbNasConnection()
    print(db.read_specific_content_file(2,2))

def read_rand_content():
    db = DbNasConnection()
    print(db.read_rand_content_file(2))

def read_account_by_username():
    db = DbNasConnection()
    print(db.read_account_by_username("dvocCreates"))


def read_account_by_id():
    db = DbNasConnection()
    print(db.read_account_by_id(1))


# --------- CREATE ---------

def create_account():
    """
    Test for making an account
    """
    db = DbNasConnection()
    db.create_account("dvocCreates","dvoc@test.com", "Do you know the way?", "yt_shorts",
                      "THIS is a long description of what will be created here on this database of a thing")

def create_media_pool():
    db = DbNasConnection()
    #db.create_media_pool("OpenAI api calls", "Text files from open AI")
    db.create_media_pool("OpenAI api calls","Text data from redit apis")

def create_content_file():
    db = DbNasConnection()
    db.create_content("/Users/dvoicu/mnt/Goofy Aughhh Test Files/Aughhhhh.png","The title of this content", "breef disc", "dvocCreatesPART2")

def create_junktion_entry():
    db = DbNasConnection()
    # db.create_junction_entry("j_accounts__content_files","1","1")
    # db.create_junction_entry("j_accounts__content_files","1","2") # This should be an error if there is no content file with id 2
    # db.create_junction_entry("j_accounts__media_files","1","1")
    # db.create_junction_entry("j_aunts__media_files33", "1", "1")
    #db.create_junction_entry("j_accounts__content_files","2","3")
    #db.create_junction_entry("j_accounts__media_pools","1","1")
    db.create_junction_entry("j_media_pools__media_files",2,2)




main()