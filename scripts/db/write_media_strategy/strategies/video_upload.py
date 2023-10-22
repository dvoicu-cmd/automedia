

class VideoUpload:
    conn = None
    curr = None
    location = None
    account_id = None

    def __init__(self):
        """
        Constructor method
        """
        print("")

    def set(self, conn, curr, account_id, location):
        """
        Sets the db connection, cursor, and write location for the file
        Args:
            conn ([mariadb connection]): the mariadb connection
            curr ([mariadb cursor]): the cursor for the mariadb connection
            location ([string]): the file path to write to.
            account_id ([int]): the associated account id for the content.
        """
        self.conn = conn
        self.curr = curr
        self.location = location
        self.account_id = account_id

    def write_to_nfs(self, content):
        """
        The specific implementation for uploading the content to the database
        """
        
        print("")
