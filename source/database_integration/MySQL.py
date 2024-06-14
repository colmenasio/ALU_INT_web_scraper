from source.database_integration.AbsDatabase import AbsDatabase
from os import path, listdir
import mysql.connector
import json


class MySQL(AbsDatabase):
    DATABASE_NAME = "test_web_scraper"
    # TODO make this a prompt or a config or something idk this is just sad

    CREDENTIALS_FILEPATH = "../../configs/mysql_credentials/credentials.json"
    CATEGORIES_FILEPATH = "../../configs/categories/categories.json"
    WEBSITE_DEFINITIONS_FILEPATH = "../../configs/website_definitions/definitions"

    def __init__(self):
        print("\n-----------------------------------------------\n"
              "MySQL was selected as the destination of the data.\n"
              f"The database that will be used is '{self.DATABASE_NAME}'")
        # TODO add options to change the database selected
        if input("Proceed? (Y/N) ").lower() != "y":
            exit()
        self.session = self._do_login()
        self.cursor = self.session.cursor()
        self._check_if_db_exists()

    def save_to_database(self, disaster_instance_arg) -> None:
        raise NotImplementedError

    def _do_login(self):
        credentials = self._get_credentials()
        try:
            return mysql.connector.connect(**credentials)
        except mysql.connector.errors.ProgrammingError:
            print("Credentials invalid. Wrong host, username or password. Edit them?")
            if input("(Y/N)").lower() == "y":
                self._create_credentials()
                print("Re-run the script to retry login")
            exit()

    def _get_credentials(self) -> dict:
        credentials_exist = path.isfile(self.CREDENTIALS_FILEPATH)
        if not credentials_exist:
            print(f"Credentials not found in '{self.CREDENTIALS_FILEPATH}'. Create it?")
            if input("(Y/N)").lower() == "y":
                self._create_credentials()
        with open(self.CREDENTIALS_FILEPATH) as fstream:
            credentials = json.load(fstream)
        are_credentials_valid = all([credential in credentials.keys() for credential in ["host", "user", "password"]])
        if not are_credentials_valid:
            print("Runtime Error: Credentials are not valid (Ensure the host, user and password fields are defined)")
            exit()
        return credentials

    def _create_credentials(self):
        host = input("host (default 'localhost'): ")
        if len(host) == 0:
            host = "localhost"
        user = input("user: ")
        password = input("password: ")
        with open(self.CREDENTIALS_FILEPATH, "w") as fstream:
            fstream.write(f'{{"host": "{host}", "user": "{user}", "password": "{password}"}}')
        print(f"'{self.CREDENTIALS_FILEPATH}' created")

    def _check_if_db_exists(self) -> None:
        self.cursor.execute("SHOW DATABASES")
        if self.DATABASE_NAME not in [x[0] for x in self.cursor]:
            print(f"Database named '{self.DATABASE_NAME}' does not exist.")
            if input("Create It (Y/N) ").lower() == "y":
                self._create_database()
        self.cursor.execute(f"USE {self.DATABASE_NAME}")

    def _create_database(self) -> None:
        # TODO make it so that if the creation process excepts, the half-finished database is dropped
        self.cursor.execute(f"CREATE DATABASE {self.DATABASE_NAME}")
        try:
            self.cursor.execute(f"USE {self.DATABASE_NAME}")
            self._create_main_table()
            self._create_news_portals_table()
            self._create_disasters_tables()
            print(f"Database named {self.DATABASE_NAME} created correctly")
        except mysql.connector.ProgrammingError as e:
            print(f"Process of creating the database named: {self.DATABASE_NAME} failed.")
            if input("Delete the half-finished database? (Y/N)").lower() == "y":
                self.cursor.execute(f"DROP DATABASE {self.DATABASE_NAME}")
            raise e

    def _create_main_table(self) -> None:
        """Creates the main table of the database"""
        with open(self.CATEGORIES_FILEPATH) as fstream:
            disaster_types = str(list(json.load(fstream).keys())).strip("[]")
        self.cursor.execute("CREATE TABLE RawNews ("
                            "RawNews_ID INT AUTO_INCREMENT PRIMARY KEY, "
                            "NewsPortal_ID VARCHAR(50) NOT NULL, "
                            f"DisasterType ENUM({disaster_types}) NOT NULL, "
                            "Disaster_ID INT NOT NULL, "
                            "NewURL VARCHAR(255) NOT NULL, "
                            "NewTitle VARCHAR(255) NOT NULL, "
                            "NewBody TEXT NOT NULL, "
                            "UNIQUE (DisasterType, Disaster_ID), "
                            "INDEX (DisasterType, Disaster_ID)"
                            ")")

    def _create_news_portals_table(self) -> None:
        """Creates the table holding information of the news portals from data in the website_definitions"""
        """Creates the main table of the database"""
        self.cursor.execute("CREATE TABLE NewsPortals ("
                            "Name VARCHAR(50) PRIMARY KEY, "
                            "MainURL VARCHAR(255) NOT NULL, "
                            "Language CHAR(2) NOT NULL"
                            ")")
        definitions = listdir(self.WEBSITE_DEFINITIONS_FILEPATH)
        website_def_filenames = [file_name for file_name in definitions if file_name.endswith(".json")]
        print("The metadata of the following websites will be loaded into the database:")
        print([web_name.removesuffix(".json") for web_name in website_def_filenames])
        for website_def in website_def_filenames:
            with open(f"{self.WEBSITE_DEFINITIONS_FILEPATH}/{website_def}") as fstream:
                website_configs = json.load(fstream)
            try:
                # TODO sanitize stuff just in case idk
                web_name = website_configs["web_name"]
                web_main_url = website_configs["main_page_link"]
                web_language = website_configs["language"]
            except KeyError:
                print(f"Error loading metadata from '{website_def}'")
                continue
            query = "INSERT INTO NewsPortals (Name, MainURL, Language) " \
                    f"VALUES ('{web_name}', '{web_main_url}', '{web_language}')"
            try:
                self.cursor.execute(query)
            except mysql.connector.ProgrammingError as e:
                print(f"Error inserting metadata from '{website_def}' into database.\n"
                      f"The following query caused the error: {query}")
            except mysql.connector.DataError as e:
                print(f"Data in '{website_def}' is not valid\n"
                      f"The following query caused the error: {query}")
                print(e)

    def _create_disasters_tables(self) -> None:
        """Creates a table from each type of disaster defined in the categories."""
        with open(self.CATEGORIES_FILEPATH) as fstream:
            disaster_types = json.load(fstream)
        keys = list(disaster_types.keys())
        for key in keys:
            query = f"CREATE TABLE {key} ("
            for column in disaster_types[key]:
                query += self._format_disaster_column(column)
                query += ", "
            query = query.removesuffix(", ")
            query += ")"
            self.cursor.execute(query)

    @staticmethod
    def _format_disaster_column(dict_arg: dict) -> str:
        name = dict_arg["parameter_name"].replace(" ", "_")
        types_dict = {
            "int": "INT",
            "str": "VARCHAR(255)",
            "date": "DATE",
            "bool": "TINYINT"
        }
        return f"{name} {types_dict[dict_arg['format']]}"

    @staticmethod
    def _generate_disaster_query(disaster_instance_arg) -> str:
        column_names = str(list(disaster_instance_arg.data.keys())).strip("[]")
        values = str(list(disaster_instance_arg.data.values())).strip("[]")
        query = f"INSERT INTO {disaster_instance_arg.category} ({column_names}) VALUES ({values})"
        return query

    def _generate_rawnew_query(self, disaster_instance_arg, disaster_key: int, news_portal_key: str) -> str:
        pass

