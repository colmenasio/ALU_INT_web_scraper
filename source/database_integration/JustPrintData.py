from source.database_integration.AbsDatabase import AbsDatabase


class JustPrintData(AbsDatabase):
    """Doesn't send anything to the database, just prints the information, useful for debugging"""

    has_done_startup_command_prompt = False

    def __init__(self):
        if not JustPrintData.has_done_startup_command_prompt:
            self._do_startup_command_prompt()
            JustPrintData.has_done_startup_command_prompt = True

    def save_to_database(self, disaster_instance_arg) -> None:
        print(disaster_instance_arg)

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    @staticmethod
    def _do_startup_command_prompt() -> None:
        print("\n-----------------------------------------------\n"
              "No database was selected. As a result the data will not be stored, only printed to the command line")
        if input("Continue anyways? (Y/N)").lower() != "y":
            exit()
