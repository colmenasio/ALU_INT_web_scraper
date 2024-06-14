from source.Categories import Categories
from source.CustomExceptions import InsufficientInformation, InvalidCategoryErr
from source.GptParser import GptParser
from source.database_integration.MySQL import MySQL


class Disaster:
    """Class containing methods to parse a new, process it, and send scraped data to a database

    The idea is to initialize a Disaster instance with some attributes unspecified, and then use the provided methods to
    fill the remaining ones until the instance is ready to be sent to the database"""

    categories = Categories.build_from_json()
    database = MySQL()
    # TODO Since eventually the database will change, make the selection of the db used a command prompt or a config idc

    def __init__(self,
                 raw_data_arg: dict = None,
                 news_portal_arg: str = None,
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
        self.news_portal = news_portal_arg
        self.link = link_arg
        self.language = language_arg
        # TODO sanitize the category input
        self.category = category_arg
        # TODO sanitize the data input
        self.data = data_arg

    def classify(self) -> None:
        """In-place classification of the new. Fills self->category using self->raw_data"""
        if self.raw_data is None or self.language is None:
            raise InsufficientInformation(Disaster.classify.__name__, "self.raw_data and self.language")
        result = GptParser.classify(self.raw_data, list(self.categories.get_categories()))
        if result is None:
            raise InvalidCategoryErr()
        self.category = result

    def extract_data(self) -> None:
        """In-place extraction of information. Fills the self->data field using self->raw_data and self->category"""
        if self.raw_data is None or self.category is None or self.language is None:
            raise InsufficientInformation(
                Disaster.extract_data.__name__, "self.raw_data, self.language and self.category"
            )
        self.data = GptParser.answer_questions(self.raw_data, self.categories.get_questions_for(self.category))

    def save_to_database(self) -> None:
        """Requires self->category and self->data to be specified"""
        if self.category is None or self.data is None:
            raise InsufficientInformation(Disaster.save_to_database.__name__, "self.category and self.data")
        self.database.save_to_database(self)

    def __str__(self):
        print(f"Object: {self.__repr__()}\n"
              f"Unparsed Data: {self.raw_data}"
              f"Link: {self.link}\n")
