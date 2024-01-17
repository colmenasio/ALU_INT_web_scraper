import GptParser


class InvalidCategoryErr(Exception):
    """To be raised when the classifier wasn't able to classify a given new"""
    def __init__(self):
        super.__init__(f"Classifier could not classify the new into any given category")


class Disaster:
    """Class containing several methods to parse a new, process it, and send scraped data to a database"""
    generic_parameters = ("Number of lethal victims (int)", "Number of affected people (int)",
                          "Date of the disaster (date)", "Region (str)")
    subtypes_parameters = {
        "Flood": generic_parameters,
        "Drought": generic_parameters,
        "Disease": ("Number of lethal victims (int)", "Region (str)", "Name of the disease (str)"),
        "Earthquake": generic_parameters
    }

    def __init__(self, unprocessed_data_arg: dict, link_arg: str, category_arg: str = None, data_arg: str = None):
        """
        :param unprocessed_data_arg: A dictionary containing 2 keys: title and body, of the New
        :param link_arg: A string containing the link to the New
        """
        self.raw_data = unprocessed_data_arg
        self.link = link_arg
        # TODO sanitize the category input
        self.category = category_arg
        # TODO sanitize the data input
        self.data = data_arg

    def classify(self) -> None:
        """In-place classification of the new"""
        result = GptParser.classify(self.raw_data, list(Disaster.subtypes_parameters.keys()))
        if result is None:
            raise InvalidCategoryErr()
        self.category = result

    def extract_data(self) -> None:
        """In-place extraction of information"""
        self.data = GptParser.extract_json(self.raw_data, self.subtypes_parameters[self.category])

    def save_to_database(self) -> None:
        print(f"suppose we send {self} to db\n"
              f"Disaster type: {self.category}\n"
              f"Disaster data: {self.data}")
