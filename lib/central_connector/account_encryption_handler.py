"""
account_handler.py

handles account data as it goes to the central database on the publisher.
"""


class AccountEncryptionHandler:
    """
    Private Variables
    """
    central_connection = None

    def __init__(self, connection):
        self.central_connection = connection

    # TODO implement
    def encrypt_send(self):
        """
        Encrypts the username and password using aes + a password file then creates a new account record.
        """
        return

    # TODO implement
    def receive_decrypt(self):
        """
        Receives and decrypts the email and password.
        """
        return

    # TODO implement
    def create_key(self):
        """
        Creates a key using openssl
        """
        return
