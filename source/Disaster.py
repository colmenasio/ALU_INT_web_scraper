from source.CustomExceptions import InsufficientInformation, InvalidCategoryErr
from source.GptParser import GptParser


class Disaster:
    """Class containing methods to parse a new, process it, and send scraped data to a database

    The idea is to initialize a Disaster instance with some attributes unspecified, and then use the provided methods to
    fill the remaining ones until the instance is ready to be sent to the database"""

    generic_parameters = ("Number of lethal victims (int)", "Number of affected people (int)",
                          "Date of the disaster (date)", "Region (str)")
    subtypes_parameters = {
        "Flood": generic_parameters,
        "Drought": generic_parameters,
        "Disease": ("Number of lethal victims (int)", "Region (str)", "Name of the disease (str)"),
        "Earthquake": generic_parameters
    }

    def __init__(self,
                 raw_data_arg: dict = None,
                 link_arg: str = None,
                 language_arg: str = None,
                 category_arg: str = None,
                 data_arg: str = None):
        """
        Instance constructor. All parameters default to None

        :param raw_data_arg: A dictionary containing 2 keys: title and body, of the New
        :param link_arg: A string containing the link to the New
        :param category_arg
        """
        self.raw_data = raw_data_arg
        self.language = language_arg
        self.link = link_arg # TODO deprecated attribute, remove it
        # TODO sanitize the category input
        self.category = category_arg
        # TODO sanitize the data input
        self.data = data_arg

    def classify(self) -> None:
        """In-place classification of the new. Fills self->category using self->raw_data"""
        if self.raw_data is None or self.language is None:
            raise InsufficientInformation(Disaster.classify.__name__, "self.raw_data and self.language")
        result = GptParser.classify(self.raw_data, list(Disaster.subtypes_parameters.keys()))
        if result is None:
            raise InvalidCategoryErr()
        self.category = result

    def extract_data(self) -> None:
        """In-place extraction of information. Fills the self->data field using self->raw_data and self->category"""
        if self.raw_data is None or self.category is None or self.language is None:
            raise InsufficientInformation(
                Disaster.extract_data.__name__, "self.raw_data, self.language and self.category"
            )
        self.data = GptParser.extract_json(self.raw_data, self.subtypes_parameters[self.category])

    def save_to_database(self) -> None:
        """Requires self->category and self->data to be specified"""
        if self.category is None or self.data is None:
            raise InsufficientInformation(Disaster.save_to_database.__name__, "self.category and self.data")
        print(f"suppose we send {self.__repr__()} to db\n"
              f"Rawdata: {self.raw_data}\n"
              f"Disaster type: {self.category}\n"
              f"Disaster data: {self.data}")

    def __str__(self):
        print(f"Object: {self.__repr__()}\n"
              f"Unparsed Data: {self.raw_data}"
              f"Link: {self.link}")
