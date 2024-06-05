import os.path
import mysql.connector
import json


class mySQL_api:
    """Wrapper class whose purpose is mostly to implement
    the __exit__ method in case shit hits the fan (cause it will)"""
    CREDENTIALS_FILENAME = "credentials.json"

    def __init__(self):
        self.curr_session = self.do_login()
        print("Login Successful")

    def __enter__(self):
        return self.curr_session

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Loging out")
        self.curr_session.close()

    def do_login(self):
        credentials_exist = os.path.isfile(self.CREDENTIALS_FILENAME)
        if not credentials_exist:
            print(f"Runtime Error: '{self.CREDENTIALS_FILENAME}' not found in the directory. Create it?")
            if input("(Y/N)").lower() == "y":
                self.create_credentials()
        with open(self.CREDENTIALS_FILENAME) as fstream:
            credentials = json.load(fstream)
        are_credentials_valid = all([credential in credentials.keys() for credential in ["host", "user", "password"]])
        if not are_credentials_valid:
            print("Runtime Error: Credentials are not valid (Ensure the host, user and password fields are defined)")
            exit()
        try:
            return mysql.connector.connect(**credentials)
        except mysql.connector.errors.ProgrammingError:
            print("Runtime Error: Credentials invalid. Wrong host, username or password. Edit them?")
            if input("(Y/N)").lower() == "y":
                self.create_credentials()
                print("Re-run the script to retry login")
            exit()

    def create_credentials(self):
        host = input("host (default 'localhost'): ")
        if len(host) == 0: host = "localhost"
        user = input("user: ")
        password = input("password: ")
        with open(self.CREDENTIALS_FILENAME, "w") as fstream:
            fstream.write(f'{{"host": "{host}", "user": "{user}", "password": "{password}"}}')
        print(f"'{self.CREDENTIALS_FILENAME}' created")


def check_if_already_existing(session, db_name):
    pass


def create_database(session, db_name):
    pass


def get_cursor(session, db_name):
    pass


def create_tables(cursor):
    pass


if __name__ == "__main__":
    with mySQL_api() as session:
        # TODO add database name input prompt
        # TODO add logs and prints and stuff
        db_name = "web-scraper-test"
        check_if_already_existing(session, db_name)
        create_database(session, db_name)
        cursor = get_cursor(session, db_name)
        create_tables(cursor)
