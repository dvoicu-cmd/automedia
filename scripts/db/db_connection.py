"""
Python class used to interface with the sql and the network filesystem ports on the central storage server.

'db_connection.py'
"""

import mariadb
import configparser
import os

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
        try:
            self.credentials = self.__loadConnectionConfig()
        except:
            print("no cred.cfg file found. Call writeConnectionConfig() to create one")
            print("credentials set to None")
        
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
    
    def writeConnectionConfig(self, hostIp, port, user, password, database):
        """
        Writes a cred.cfg file that configures how to connect to the database.

        Args:
            hostIp ([string]): [description]
            port ([string]): [description]
            user ([string]): [description]
            password ([string]): [description]
            database ([string]): [description]
        """
        config = configparser.ConfigParser()
        config['CREDENTIALS'] = {}
        creds = config['CREDENTIALS']
        creds['ip'] = hostIp
        creds['port'] = port
        creds['user'] = user
        creds['password'] = password
        creds['database'] = database
        with open('cred.cfg', 'w') as configfile:
            config.write(configfile)
        
    
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
    
    def makeConnection(self):
        """
        private method to init db connection
        """
        #Make connection with credentials
        cred = self.credentials
        self.connection = mariadb.connect(host=cred.get('ip'), port=int(cred.get('port')), user=cred.get('user'), password=cred.get('password'), database=cred.get('database'))
        print(self.connection)
        
    def closeConnection(self):
        """
        private method to close db connection
        """
        #Close the connection
        self.connection.close()
        print("connection closed")
        
    def __saveToNFS(self, url, account_id):
        """
        downloads and writes the media content to the nfs server

        Args:
            url ([string]): [the url for the content to download]
            account_id ([int]): [account that the media content is assoicated with]
        """
        # First 
        print("writes to network file system")
        
    def __loadConnectionConfig(self):
        """
        Reads the cred.cfg in the current directory to authentication to database
        Returns:
            (dict): [values for database authentication]
        """
        #Load credentials here
        config = configparser.ConfigParser()
        
        #Attempt file read
        try:
            config.read('cred.cfg')
        except:
            raise Exception("No config file found")
        
        #Parse and then output
        creds = config['CREDENTIALS']
        
        outputDict = {
            "ip":creds['ip'],
            "port":creds['port'],
            "user":creds['user'],
            "password":creds['password'],
            "database":creds['database']   
        }
        
        return outputDict
    