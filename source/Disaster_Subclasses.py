import openai
from threading import Lock


class UnableToDetectDisasterType(Exception):
    pass


class Disaster:
    """Class containing several fuctions to parse a new, process it, and send scraped data to a database"""
    with open("gpt_keys.txt") as stream:
        openai_keys = list(map(lambda x: x.rstrip("\n", ), stream.readlines()))
    subtypes = ("Flood", "Drought", "Disease", "Earthquake")
    generic_parameter = ("Number of lethal victims (int)", "Number of affected people (int)",
                         "Date of the disaster (date)", "Region (str)")
    subtypes_parameters = {
        "Flood": generic_parameter,
        "Drought": generic_parameter,
        "Disease": ("Number of lethal victims (int)", "Region (str)", "Name of the disease (str)"),
        "Earthquake": generic_parameter
    }

    parser_chat = openai.OpenAI(api_key=openai_keys[0], organization=openai_keys[1])
    parser_chat_lock = Lock()  # i think it's not needed due to GIL

    def __init__(self, unprocessed_data_arg: dict):
        self.raw_data = unprocessed_data_arg
        self.disaster_type = None
        self.disaster_data = None
        print(f"PASSED DATA: {unprocessed_data_arg}")

    def classify_new(self) -> None:
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
        disaster_type = response.choices[0].message.content
        if disaster_type not in Disaster.subtypes:
            print(f"CLASSIFIER ERROR, detected: {disaster_type}")
            raise UnableToDetectDisasterType
        self.disaster_type = disaster_type

    def extract_json(self) -> None:
        """Parses a new obtaining the parameters specified in its disaster subtype. This functions is so bad it's a pain
        to look at, ill rewrite it later"""
        parser_client = openai.OpenAI(api_key=Disaster.openai_keys[0], organization=Disaster.openai_keys[1])
        response = parser_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system",
                       "content": "You are a scraping tool. The following messages will containt text from news parsed "
                                  "as a python dictionary, as well as a list of parameters. Parse the new, obtaining "
                                  "the data corresponding to each parameter, and return the answers in json format."
                                  "Each parameter is followed by the type it must be answered with in parenthesis;\n"
                                  "- int indicates unsigned integer\n"
                                  "- str indicates string\n"
                                  "- date indicates a string containing the date in the format: "
                                  "'from yyyy/mm/dd to yyyy/mm/dd'. If a specific date is unknown, replace its digits "
                                  "with '-'. For example, 'from 2020/01/-- to 2020/03/01' would represent a span of "
                                  "time starting some day in January of 2020 and ending in March first 2020.\n"
                                  "In case the article does not contain the information required to answer a "
                                  "particular parameter, its value should be 'None'"},
                      {"role": "user",
                       "content": f"New: {self.raw_data}\n"
                                  f"Parameters: {Disaster.subtypes_parameters[self.disaster_type]}"}
                      ])
        self.disaster_data = response.choices[0].message.content

    def save_to_database(self):
        print(f"suppose we send {self} to db\n"
              f"Disaster type: {self.disaster_type}\n"
              f"Disaster data: {self.disaster_data}")
