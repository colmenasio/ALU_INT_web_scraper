from source.database_integration.MySQL import MySQL


def database_creation():
    MySQL.DATABASE_NAME = "test_run"
    MySQL.CREDENTIALS_FILEPATH = "../configs/mysql_credentials/credentials.json"
    MySQL.CATEGORIES_FILEPATH = "../configs/categories/categories.json"
    MySQL.WEBSITE_DEFINITIONS_FILEPATH = "../configs/website_definitions/definitions"
    database = MySQL()


if __name__ == "__main__":
    database_creation()
