class UnableToDetectDisasterType(Exception):
    pass


class Disaster:
    """Class containing several fuctions to parse a new, process it, and send scraped data to a database"""

    def __init__(self, unprocessed_data_arg: dict):
        pass

    def process_data(self):
        pass

    def save_to_database(self):
        print("suppose we do something")