"""
Python class used to interface with the sql and the network filesystem ports on the central storage server.

'dbConnection.py'
"""

import mariadb

class dbConnection:
    
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
        
    
    # defines the mariadb connection.
    connection = None
    
    # dictionary that contains the credentials to log into the database.
    credentials = None
    
    # defines the selected account id to reference from db.
    account = None
    
    ### --Constructor-- ###
    
    def __init__(self):
        """
        Constructor method
        """
        #first load the db credentials
        self.credentials = self.__loadCredentials()
        
        print("db")
        
    ### --Read methods-- ###
    
    def findAccountId(self, email, username):
        """
        finds the account id given an email and username

        Args:
            email ([type]): [description]
            username ([type]): [description]
        """
        print("Pulls the account id")
        
    ### --Write methods-- ###
    
    def writeMedia(self, content, type):
        """
        Writes the media content into db and nfs on storage server

        Args:
            content ([type]): [the content to be written]
            type ([type]): [media type of the account in form:'video','audio','text','image']
        """
        print("writes the presented data to database sever")
        
    def writeAccount(self, email, platform, username, password):
        """
        Writes a new account record in the accounts table

        Args:
            email ([string]): [email of the account]
            platform ([string]): [platform of the account in form: 'tiktok','yt_shorts','instagram_reels','yt_videos']
            username ([string]): [username of the account]
            password ([string]): [password of the account]
        """
        print("written")
    
    ### --private methods-- ###
    
    def __makeConnection(self):
        """
        private method to init db connection
        """
        #Make connection with credentials
        self.connection = mariadb.connect(self.credentials)
        
    def __closeConnection(self):
        """
        private method to close db connection
        """
        #Close the connection
        self.connection.close()
        
    def __saveToNFS(self, url, account_id):
        """
        downloads and writes the media content to the nfs server

        Args:
            url ([string]): [the url for the content to download]
            account_id ([int]): [account that the media content is assoicated with]
        """
        # First 
        print("writes to network file system")
        
    def __loadCredentials(self):
        """
        Reads the cred.cfg in the current directory to establish authentication to database
        Returns:
            (dict): [values for database authentication]
        """
        #Load credentials here
        return {}