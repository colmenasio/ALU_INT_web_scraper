from source.database_integration.AbsDatabase import AbsDatabase


class JustPrintData(AbsDatabase):
    """Doesn't send anything to the database, just prints the information, useful for debugging"""
    def __init__(self):
        print("\n-----------------------------------------------\n"
              "No database was selected. As a result the data will not be stored, only printed to the command line")
        if input("Continue anyways? (Y/N)").lower() != "y":
            exit()

    def save_to_database(self, disaster_instance_arg) -> None:
        print(disaster_instance_arg)

    def close_connection(self) -> None:
        pass