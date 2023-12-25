import openai
from threading import Lock


class UnableToDetectDisasterType(Exception):
    pass


class Disaster:
    """Class containing several fuctions to parse a new, process it, and send scraped data to a database"""
    with open("gpt_keys.txt") as stream:
        openai_keys = list(map(lambda x: x.rstrip("\n", ), stream.readlines()))
    subtypes = ("Flood", "Drought", "Disease", "Earthquake")
    subtypes_parameters = {}

    parser_chat = openai.OpenAI(api_key=openai_keys[0], organization=openai_keys[1])
    parser_chat_lock = Lock()  # i think it's not needed due to GIL

    def __init__(self, unprocessed_data_arg: dict):
        self.raw_data = unprocessed_data_arg
        self.disaster_type = None
        self.disaster_data = None
        print(f"PASSED DATA: {unprocessed_data_arg}")

    def classify_new(self) -> str:
        """Classifies a new into one of the disaster subtypes. This functions is so bad it's a pain to look at,
         ill rewrite it later"""
        classifier_client = openai.OpenAI(api_key=Disaster.openai_keys[0], organization=Disaster.openai_keys[1])
        response = classifier_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system",
                       "content": "You are a news articles classifying tool. The following messages will contain"
                                  "news articles parsed as python dictionaries, and you must classify them into one of "
                                  f"the following categories: {Disaster.subtypes}\n."
                                  "Return a single string containing the category.\n"
                                  "Return 'None' if not sure or the new doesnt fit in the categories"},
                      {"role": "user",
                       "content": str(self.raw_data)}])
        return response.choices[0].message.content

    def extract_json(self) -> str:
        """Parses a new obtaining the parameters specified in its disaster subtype. This functions is so bad it's a pain
        to look at, ill rewrite it later"""
        print(f"suppose we process and stuff")
        return ""
        parser_client = openai.OpenAI(api_key=Disaster.openai_keys[0], organization=Disaster.openai_keys[1])
        response = parser_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system",
                       "content": "You are a scraping tool. The following messages will containt text from news parsed "
                                  "as a python dictionary, as well as a list of parameters. Parse the new, obtaining "
                                  "the data corresponding to each parameter, and return the answers in json format."},
                      {"role": "user",
                       "content": str(self.raw_data)}
                      ])
        return response.choices[0].message.content

    def save_to_database(self):
        print(f"suppose we send {self} to db")
