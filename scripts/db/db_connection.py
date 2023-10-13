"""
Python class used to interface with the sql and the network filesystem ports on the central storage server.

'db_connection.py'
"""

import mariadb
import configparser
import os

from scripts.db.write_media_strategy.db_write_media import DbWriteMedia


class DbConnection:
    # defines the mariadb connection and cursor.
    conn = None
    curr = None

    # dictionary that contains the credentials to log into the database.
    credentials = None

    # defines the selected account id to reference from db.
    account_id = None

    ### --Constructor-- ###

    def __init__(self):
        """
        Constructor method
        """
        # first load the db credentials
        try:
            self.credentials = self.__load_connection_config()
        except:
            print("WARNING: no cred.cfg file found in db directory.")
            print("Call writeConnectionConfig() to create one")

    # --Read methods-- #

    def find_account_id(self, email, username):
        """
        finds the account id given an email and username

        Args:
            email ([type]): [description]
            username ([type]): [description]
        """
        print("Pulls the account id")

    # --Write methods-- #

    def write_connection_config(self, hostIp, port, user, password, database):
        """
        Writes a cred.cfg file that configures how to connect to the database and applies that connection to current connection obj.

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
        self.credentials = self.__load_connection_config()

    def write_media(self, content, content_type):
        """
        Writes the media content into db and nfs on storage server

        Args:
            content ([type]): [the content to be written]
            content_type ([type]): [media type of the account in form:'video','audio','text','image']
        """
        self.__make_connection()

        operation = DbWriteMedia()
        # for now we will hard code the location (To be added to config file)
        operation.execute(content, self.conn, self.curr, self.account_id, content_type, "/Users/dvoicu/Desktop/Local Editing Projects/bottomtextmedia/project-automatic/scripts/db/")

        self.__close_connection()

    def write_account(self, email, platform, username, password):
        """
        Writes a new account record in the accounts table.
        NOTE: this function will not check the format of the platform input, ensure data integrity please.
        Args:
            email ([string]): [email of the account]
            platform ([string]): [platform of the account in form: 'tiktok','yt_shorts','instagram_reels','yt_videos']
            username ([string]): [username of the account]
            password ([string]): [password of the account]
        """
        # Open connections
        self.__make_connection()
        # Write query
        table = 'accounts'
        query = f'INSERT INTO {table} (email, platform, username, password) VALUES (\'{email}\', \'{platform}\', \'{username}\', \'{password}\');'
        query.format(table, email, platform, username, password)
        # Execute the query
        self.curr.execute(query)
        # Close connection
        self.__close_connection()

    # --private methods-- #

    def __make_connection(self):
        """
        private method to init db cursor and connection
        """
        # Make connection with credentials, then set up autocommit and db cursor
        cred = self.credentials
        self.conn = mariadb.connect(host=cred.get('ip'),
                                    port=int(cred.get('port')),
                                    user=cred.get('user'),
                                    password=cred.get('password'),
                                    database=cred.get('database')
                                    )
        self.conn.autocommit = True
        self.curr = self.conn.cursor()

    def __close_connection(self):
        """
        private method to close db connection
        """
        # Close the connection
        self.curr.close()
        self.conn.close()

    @staticmethod
    def __load_connection_config():
        """
        Reads the cred.cfg in the current directory to authentication to database
        Returns:
            (dict): [values for database authentication]
        """
        # Load credentials here
        config = configparser.ConfigParser()

        # Attempt file read
        file = config.read('cred.cfg')

        if not file:
            raise Exception('Failed to read config file')

        # Parse and then output
        output_dict = {
            "ip": config['CREDENTIALS']['ip'],
            "port": config['CREDENTIALS']['port'],
            "user": config['CREDENTIALS']['user'],
            "password": config['CREDENTIALS']['password'],
            "database": config['CREDENTIALS']['database']
        }

        return output_dict
