"""
Python class used to interface with the sql and the network filesystem ports on the central storage server.
(ie: The DB and NAS Server)
"""

import mariadb
import configparser
import os


class DbNasConnection:
    # defines the mariadb connection and cursor.
    conn = None
    curr = None

    # dictionary that contains the credentials to log into the database.
    credentials = None

    # defines the selected account id to reference from db.
    account_id = None

    # ------------ Constructor ------------ #

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

    # ------------------------ CRUD MODEL ------------------------ #

    # ------------ Create Methods ------------ #

    # TODO implement
    def create_scrapes(self, account_id, content, content_type):
        """
        Writes the media content into db and nfs on the storage server

        Args:
            account_id (int): The account id for the scraped items
            content (str): The content to be written
            content_type (str): Media type of the account in form:'video','audio','text','image'
        """
        self.__make_connection()
        print("sql code to write media")
        self.__close_connection()
        return

    # TODO implement
    def create_produced_content(self, account_id, title):
        """
        Writes the produced content from the creator into db and nfs on the storage server
        Args:
            account_id (int): The account id for the created content
            title
        """
        return

    def create_account(self, email, username, platform, password):
        """
        Writes a new account record in the accounts table.
        NOTE: This function will not check the format of the platform input, ensure data integrity please.
        Args:
            email (str): Email of the account
            username (str): Username of the account
            platform (str): Platform of the account in form: 'tiktok','yt_shorts','instagram_reels','yt_videos'
            password (str): Password of the account
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

    # ------------ Read Methods ------------ #

    # TODO implement
    def read_account_id(self, email, username):
        """
        Finds the account id given an email and username.
        Args:
            email (str): The string email address for the account
            username (str): The string username of the account
        """
        self.__make_connection()
        print("sql code to find account")
        self.__close_connection()
        return

    # --- Produced Videos from Creator --- #
    # TODO implement
    def read_rand_video(self, account_id):
        """
        Reads and returns the record of a random produced video of a specific account.
        Return:
            The record of the produced video
        """
        return

    # TODO implement
    def read_specific_video(self, account_id, video_id):
        """
        Reads and returns the record of a specific produced video for a specific account.
        Return:
            The record of the produced video
        """
        return

    # --- Scraped Media from Scraper --- #

    # TODO implement
    def read_rand_scrape(self, account_id, scrape_type):
        """
        Reads and returns the record of a random scraped video of a specific account and type
        Args:
            account_id (int): The specific account id.
            scrape_type (str): The type of content the scraped media is (audio, video, text, image).
        """
        return

    # TODO implement
    def read_specific_scrape(self, account_id, scrape_id):
        """
        Reads and returns the record of a specific scraped video of a specific account
        Args:
            account_id (int): The specific account id.
            scrape_id (int): The specific
        """
        return

    # ------------ Update Methods ------------ #

    def update_account_targets(self, account_id, new_targets):
        """
        Updates the scrape targets of a specific account.

        Args:
            account_id (int): The specific account id.
            new_targets (str): A string list of targets.
        """
        return

    # TODO implement
    def update_produced_to_archived(self, account_id, media_id):
        """
        Sets a specific produced video record's archive property to 1
        Arg:
            account_id (int): The account id for the content
            media_id (int): The media id for the content
        """
        return

    # TODO implement
    def update_scrape_to_archived(self, account_id, scrape_id):
        """
        Sets a specific scrape item record's archive property to 1
        Arg:
            account_id (int): The account id for the content
            scrape_id (int): The scrape id for the content
        """
        return

    # ------------ Delete Methods ------------ #

    # TODO implement
    def delete_account(self, account_id):
        """
        NUCLEAR BE SURE ABOUT CALLING THIS FUNCTION.
        removes the account record and all associated record with the account id

        Args:
            account_id (int): The account id.
        """
        return

    # TODO implement
    def delete_media(self, account_id, media_id):
        """
        Deletes the specific
        """
        return

    # ------------ Auxiliary Methods ------------ #

    def make_connection_config(self, host_ip, port, user, password, database):
        """
        Writes a cred.cfg file that configures how to connect to the database
        and applies that connection to current connection obj.

        Args:
            host_ip (string): The host ip for the database.
            port (string): The port for the sql service.
            user (string): The username of the database authentication account.
            password (string): The password of the database authentication account.
            database (string): The name of the database being accessed.
        """
        config = configparser.ConfigParser()
        config['CREDENTIALS'] = {}
        creds = config['CREDENTIALS']
        creds['ip'] = host_ip
        creds['port'] = port
        creds['user'] = user
        creds['password'] = password
        creds['database'] = database
        with open('cred.cfg', 'w') as configfile:
            config.write(configfile)
        self.credentials = self.__load_connection_config()

    # ------------ Private Methods ------------ #

    # ------ Connection methods ------ #
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
            A dictionary containing the values for database authentication
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
