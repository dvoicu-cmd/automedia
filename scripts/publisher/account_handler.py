"""
account_encryption_handler.py

handles encryption and decryption of account data as it goes to the central database
"""
from project_automatic.scripts.central.db_nas_connection import DbNasConnection


class AccountEncryptionHandler:
    """
    Private Variables
    """
    central_connection = None

    def __init__(self, connection):
        self.central_connection = connection


    def encrypt_send(self):
        """
        Encrypts the username and password using aes + a password file then creates a new account record.
        """
        return


    def receive_decrypt(self):
        """
        Receives and decrypts the email and password.
        """
        return


    def create_key(self):
        """
        Creates a key using openssl
        """
        return
