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

    # ------------ Constructor ------------ #

    def __init__(self):
        """
        Constructor method
        """
        # first load the db credentials
        try:
            self.credentials = self.__load_connection_config()
        except FileNotFoundError:
            print("WARNING: no cred.cfg file found in db directory.")
            print("Call make_connection_config() to create one")

    # ------------------------ CRUD MODEL ------------------------ #

    # ------------ Create Methods ------------ #
    def create_account(self, username, email, password, platform, description):
        """
        Writes a new account record in the accounts table.
        NOTE: This function will not check the format of the platform input, ensure data integrity please.
        Args:
            email (str): Email of the account
            username (str): Username of the account
            platform (str): Platform of the account in form: 'tiktok','yt_shorts','instagram_reels','yt_videos'
            password (str): Password of the account
            description (str): A long description of the account and what kind of content it posts
        """
        # Open connections
        self.__make_connection()
        # Write query
        table = 'accounts'

        acceptable_platforms = ['tiktok', 'yt_shorts', 'instagram_reels', 'yt_videos']
        if platform not in acceptable_platforms:
            raise ValueError("Invalid platform. To ensure data integrity use one of the following:"
                             " 'tiktok', 'yt_shorts', 'instagram_reels', 'yt_videos'")


        query = (f'INSERT INTO {table} (username, email, password, platform, description) '
                 f'VALUES (\'{username}\', \'{email}\', \'{password}\', \'{platform}\', \'{description}\');')

        query.format(table, email, platform, username, password, description)
        # Execute the query
        self.curr.execute(query)
        # Close connection
        self.__close_connection()

    def create_media_file(self, file_location, media_type, title, description):
        """
        Writes the media content into db and nfs on the storage server

        Args:
            file_location (str): The location in the files system where the is content to be written.
            media_type (str): The type of media.
                Expected types include: 'text', 'audio', 'image', 'video'.
                text files: '.txt', 'rtf'
                audio files: '.mp3', '.wav'
                image files: '.png', '.jpeg'
                video files: '.mp4'
            title (str): title of the media file
            description (str): description of media file
        """
        self.__make_connection()

        # Write query
        table = 'media_files'

        acceptable_media_types = ['text', 'audio', 'image', 'video']
        if media_type not in acceptable_media_types:
            raise ValueError("Invalid media_type. To ensure data integrity use one of the following:"
                             " 'text', 'audio', 'image', 'video'")

        # For now, maybe just hard code the location of the media in mnt on the nas.
        query = (f'INSERT INTO {table} (file_location, media_type, title, description, to_archive) '
                 f'VALUES (\'{file_location}\', \'{media_type}\', \'{title}\', \'{description}\', 0);')

        query.format(table, file_location, media_type, title, description)
        # Execute the query
        self.curr.execute(query)

        self.__close_connection()
        return

    def create_media_pool(self, media_pool_name, description):
        """
        Creates a media pool record
        media_pool_name (str): The name of the media pool
        description (str): A simple description on what is contained in the pool.
        """
        # Make connection to database
        self.__make_connection()

        # Write query
        table = 'media_pools'

        query = (f'INSERT INTO {table} (media_pool_name, description) '
                 f'VALUES (\'{media_pool_name}\', \'{description}\');')

        query.format(table, media_pool_name, description)

        # Execute the query
        self.curr.execute(query)

        # Close the connection to database
        self.__close_connection()

        return

    def create_content(self, file_location, title, description):
        """
        Writes the produced content from the creator into db and nfs on the storage server
        Args:
            file_location (str): the location of the content file on the nas
            title (str): The title of the content
            description (str): The description for the content
        """
        # Make connection to database
        self.__make_connection()

        # Write query
        table = 'content_files'

        query = (f'INSERT INTO {table} (file_location, title, description, to_archive) '
                 f'VALUES (\'{file_location}\', \'{title}\', \'{description}\', 0);')

        query.format(table, file_location, title, description)

        # Execute the query
        self.curr.execute(query)

        # Close the connection to database
        self.__close_connection()

        return

    # --- Create Junction Record Methods --- #
    def create_junction_entry(self, junction_table, id1, id2):
        """
        Creates a record in the specified junction table.
        Junction tables in this database are formatted as follows: j_<id1 table>__<id2 table>
        As of writing, the known tables in the database are:
        - j_account__media_pool: Makes the links to accounts and what media pools they use.
        - j_accounts__media_files: Makes a record on what media files have been used by a specific account
        - j_media_pool__media_files: Makes the link to a media pool and specific media files associated with the pool.
        - j_accounts__content_files: Makes a record on what content file has been uploaded for a specific account.
        Args:
            junction_table (str) : The string that identifies the junction table to insert entry into
            id1 (int): id of the first row in the junction table
            id2 (int): id of the second row in the junction table
        """
        # Make connection to database
        self.__make_connection()

        # Write query

        # First check if the inputted table exists
        query = 'SHOW TABLES;'
        self.curr.execute(query)
        list_of_tables = self.curr.fetchall()
        list_of_table_names = [table[0] for table in list_of_tables if table[0].startswith('j_')]  # wtf is this gpt?

        # Check if you inputted a valid table
        if junction_table not in list_of_table_names:
            print("Existing junction tables:")
            print(list_of_table_names)
            raise ValueError("Inputted junction tables does not exists in db")

        # The input is valid, now get the two specific column names we need to insert a value.
        query = f"DESC {junction_table}"
        self.curr.execute(query)
        columns = self.curr.fetchall()
        column_names = [column[0] for column in columns]

        # With the column names, now write the query with the specified columns.
        query = (f'INSERT INTO {junction_table} ({column_names[1]}, {column_names[2]})'
                 f'VALUES (\'{id1}\', \'{id2}\');')

        query.format(junction_table, id1, id2)

        # Execute the query
        self.curr.execute(query)

        # Close the connection to database
        self.__close_connection()

        return

    # ------------ Read Methods ------------ #

    def read_account_by_id(self, account_id):
        """
        Returns the record for an account given the id
        Args:
            account_id (int) : the account id
        Returns:
            A tuple containing the record for the account
        """
        self.__make_connection()

        # Write the query
        table = "accounts"
        query = f"SELECT * FROM {table} WHERE account_id=1;"

        # Get the record
        self.curr.execute(query)
        record = self.curr.fetchone()

        self.__close_connection()
        return record

    def read_account_by_name(self, username):
        """
        Returns the record(s) for an account (or accounts) given a username
        Args:
            username (str): the username for the account
        Returns:
            A tuple or array of tuples containing the record(s) for an account (or accounts).
        """
        self.__make_connection()

        # Write query
        table = "accounts"
        query = f"SELECT * FROM {table} WHERE username=\'{username}\';"

        # Get the record
        self.curr.execute(query)
        record = self.curr.fetchall()  # Or records

        self.__close_connection()
        return record

    def read_rand_content_file(self, account_id):
        """
        Reads and returns the record of a random content file for a specific account.
        Args:
            account_id (int): The account id
        Return:
            A random tuple record of a produced video related to the account.
        """
        self.__make_connection()

        query = (f"SELECT * FROM content_files "
                 f"JOIN j_accounts__content_files jt ON content_files.content_id = jt.content_id "
                 f"WHERE jt.account_id = {account_id} AND content_files.to_archive = 0 "
                 f"ORDER BY RAND() "
                 f"LIMIT 1; ")

        self.curr.execute(query)
        record = self.curr.fetchone()

        self.__close_connection()

        return record

    def read_specific_content_file(self, account_id, content_id):
        """
        Reads and returns the record of the specific content for a specific account.
        Args:
            account_id (int): The account id as listed in the db.
            content_id (int): The content id as listed in the db.
        Return:
            The record of the produced video.
        """
        self.__make_connection()

        query = (f"SELECT * FROM content_files "
                 f"JOIN j_accounts__content_files jt ON content_files.content_id = jt.content_id "
                 f"WHERE jt.account_id = {account_id} AND jt.content_id = {content_id} AND content_files.to_archive = 0;")

        self.curr.execute(query)
        record = self.curr.fetchone()

        self.__close_connection()

        return record

    def read_media_pools_of_account(self, account_id):
        """
        Reads and returns the records of media pool that a specific account uses.
        Args:
            account_id (int): The specific account id.
        Returns:
            a tuple or array of tuples containing the media pools linked to the account
        """
        self.__make_connection()

        query = (f"SELECT * FROM media_pools "
                 f"JOIN j_accounts__media_pools jt ON media_pools.media_pool_id = jt.media_pool_id "
                 f"WHERE jt.account_id = {account_id} "
                 f"ORDER BY RAND() "
                 f"LIMIT 20; ")

        self.curr.execute(query)
        record = self.curr.fetchall()

        self.__close_connection()

        return record

    def read_media_pool_by_name(self, media_pool_name):
        """
        Reads and returns a record (or multiple records) of a media pool given a pool name
        Args:
            media_pool_name (str): String arg to search for the media pool record
        Returns:
            a tuple or array of tuples containing the records of the media pool(s)
        """
        self.__make_connection()

        table = 'media_pools'
        query = f"SELECT * FROM {table} WHERE media_pool_name=\'{media_pool_name}\';"

        self.curr.execute(query)
        record = self.curr.fetchall()

        self.__close_connection()

        return record

    def read_rand_media_file_of_pool(self, media_pool_id):
        """
        Reads and returns a random media file given a specific media pool id
        Args:
            media_pool_id (int): The id for the media pool
        Returns:
            A tuple that contains the record for a media file.
        """
        self.__make_connection()

        query = (f"SELECT * FROM media_files "
                 f"JOIN j_media_pools__media_files jt ON media_files.media_file_id = jt.media_file_id "
                 f"WHERE jt.media_pool_id = {media_pool_id} AND media_files.to_archive = 0 "
                 f"ORDER BY RAND() "
                 f"LIMIT 1; ")

        self.curr.execute(query)

        record = self.curr.fetchone()

        self.__close_connection()

        return record

    def read_all_media_files_of_pool(self, media_pool_id):
        """
        Reads and returns all media files in a given media pool
        Args:
            media_pool_id (int): The id for the media pool
        Return:
            a tuple or array of tuples that contains the relationship to the selected pool
        """
        self.__make_connection()

        query = (f"SELECT * FROM media_files "
                 f"JOIN j_media_pools__media_files jt ON media_files.media_file_id = jt.media_file_id "
                 f"WHERE jt.media_pool_id = {media_pool_id} AND media_files.to_archive = 0 ")

        self.curr.execute(query)

        record = self.curr.fetchall()

        self.__close_connection()

        return record

    def read_specific_media_file_by_name(self, title):
        """
        Reads and returns a record of a specific media_file by its title property
        Args:
            title (str): The string input of the title
        Returns:
            An array of tuples that contains the entries that match the query.
        """
        self.__make_connection()

        table = "media_files"
        query = f"SELECT * FROM {table} WHERE title=\'{title}\';"
        self.curr.execute(query)

        record = self.curr.fetchall()

        self.__close_connection()

        return record

    # ------------ Update Methods ------------ #

    def update_to_archived(self, table_name, content_id):
        """
        Given a table, updates the to_archive column (if it exists) from 0 to 1.
        Arg:
            account_id (int): The account id the content
            media_id (int): The content id for the record
        """

        self.__make_connection()

        # Check if the table exists
        if not self.__table_exists(table_name):
            raise ValueError("Given table does not exist")

        # The input is valid, now get the two specific column names we need to insert a value.
        self.__update_query(table_name, content_id, 'to_archive', 1)

        self.__close_connection()

        return
    
    def update_to_unarchived(self, table_name, content_id):
        """
        Given a table, updates the to_archive column (if it exists) from 1 to 0.
        Arg:
            account_id (int): The account id the content
            media_id (int): The content id for the record
        """
        self.__make_connection()

        # Check existence
        if not self.__table_exists(table_name):
            raise ValueError("Given table does not exist")

        # Now update
        self.__update_query(table_name, content_id, 'to_archive', 0)

        self.__close_connection()

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

    # ------------ Auxiliary Methods ------------ #
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
            raise FileNotFoundError('Failed to read config file')

        # Parse and then output
        output_dict = {
            "ip": config['CREDENTIALS']['ip'],
            "port": config['CREDENTIALS']['port'],
            "user": config['CREDENTIALS']['user'],
            "password": config['CREDENTIALS']['password'],
            "database": config['CREDENTIALS']['database'],
            "nas_root": config['CREDENTIALS']['nas_root']
        }

        return output_dict

    def make_connection_config(self, host_ip, port, user, password, database, nas_root):
        """
        Writes a cred.cfg file that configures how to connect to the database
        and applies that connection to current connection obj.

        Args:
            host_ip (string): The host ip for the database.
            port (string): The port for the sql service.
            user (string): The username of the database authentication account.
            password (string): The password of the database authentication account.
            database (string): The name of the database being accessed.
            nas_root (string): The root location of where the nas file system is mounted on this deployment
        """
        config = configparser.ConfigParser()
        config['CREDENTIALS'] = {}
        creds = config['CREDENTIALS']
        creds['ip'] = host_ip
        creds['port'] = port
        creds['user'] = user
        creds['password'] = password
        creds['database'] = database
        creds['nas_root'] = nas_root
        with open('cred.cfg', 'w') as configfile:
            config.write(configfile)
        self.credentials = self.__load_connection_config()

    # ------------ Private Methods ------------ #
    
    def __table_exists(self, table_name):
        """
        Private method for checking if the given table name exists in database
        Args:
            table_name (str): The name of the table
        Returns:
            If table does exist, return true, else return false.
        Precondition:
            A valid connection is established (ie: self._make_connection() has been called)
        """
        # First check if the inputted table exists
        query = 'SHOW TABLES;'
        self.curr.execute(query)
        list_of_tables = self.curr.fetchall()
        list_of_table_names = [table[0] for table in list_of_tables]  # wtf is this gpt?

        # Check if you inputted a valid table
        if table_name in list_of_table_names:
            return True
        else:
            return False

    def __update_query(self, target_table_name, target_id, column_property, value):
        """
        private method for isolating and updating a specific value on a table.
        Args:
            target_table_name (str): The name of the target table.
            target_id (int): The specific entry id that we modify on the target table.
            column_property (str): The specific property we are modifying on the table.
            value: The value we are updating the target with.
        Preconditions:
            1) A valid connection is already established.
            2) The target table exists.
        """
        query = f"DESC {target_table_name}"
        self.curr.execute(query)
        columns = self.curr.fetchall()
        column_names = [column[0] for column in columns]

        # Attempt to find the index of the to_archive property
        if column_property not in column_names:
            raise ValueError("Property," + column_property + " is not in the table: " + target_table_name)

        # With the column names, now write the query to update the value
        query = (f'UPDATE {target_table_name} '
                 f'SET {column_property} = \'{value}\''
                 f'WHERE {column_names[0]} = {target_id};')

        self.curr.execute(query)

        return

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
