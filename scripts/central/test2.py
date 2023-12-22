from db_nas_connection import DbNasConnection

def main():
    create_media_pool()
    create_media()
    #create_media()
    #create_junktion_entry()
    #update_to_archived_on_media_files()
    #update_to_archived_on_accounts()
    #update_to_archived_on_invalid_table()
    #update_to_archived_on_invalid_id()
    #update_to_unarchive()
    #create_content_file()

    return
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
    print(db.read_specific_media_file_by_name("He who goes out there"))

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

    #db.create_account("","", "", "yt_shorts",
    #                  "")

def create_media():
    db = DbNasConnection()
    db.create_media_file("/Users/dvoicu/mnt/Goofy Aughhh Test Files/aughhh.txt","text","He who goes out there2122","a small description of what to put in here", "OpenAI api calls")

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