import openai
from threading import Lock


class UnableToDetectDisasterType(Exception):
    pass


class Disaster:
    """Class containing several fuctions to parse a new, process it, and send scraped data to a database"""
    with open("gpt_keys.txt") as stream:
        openai_keys = list(map(lambda x: x.rstrip("\n", ), stream.readlines()))
    subtypes = ("Flood", "Drought", "Disease")
    subtypes_parameters = {}

    parser_chat = openai.OpenAI(api_key=openai_keys[0], organization=openai_keys[1])
    parser_chat_lock = Lock()  # i think it's not needed due to GIL

    def __init__(self, unprocessed_data_arg: dict):
        self.disaster_type = None
        self.disaster_data = None
        print(f"PASSED DATA: {unprocessed_data_arg}")

    def classify_new(self) -> str:
        """Consumer coroutine"""
        classifier = openai.OpenAI(api_key=Disaster.openai_keys[0],
                                   organization=Disaster.openai_keys[1]).chat.completions
        classifier.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system",
                       "message": "You are a news articles classifying tool. The following messages will contain"
                                  "news articles parsed as python dictionaries, and you must classify them into one of "
                                  f"the following categories: {Disaster.subtypes}\n."
                                  "Return a single string containing the category.\n"
                                  "Return 'None' if not sure"}]
        )
        classifier_lock = Lock()  # i think it's not needed due to GIL
        while True:
            response = classifier.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user",
                           "message": (yield)}]
            )

    def process_data(self):
        print(f"suppose we process {self} and stuff")

    def save_to_database(self):
        print(f"suppose we send {self} to db")
