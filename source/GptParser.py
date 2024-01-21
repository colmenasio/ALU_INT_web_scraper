from __future__ import annotations
from json import dumps
import openai


class GptParser:
    try:
        with open("../gpt_keys/keys.txt") as stream:
            # TODO this is horrible. Words cannot describe how horrible it is. i shall F I X I T
            openai_keys = list(map(lambda x: x.rstrip("\n", ), stream.readlines()))

    except FileNotFoundError as e:
        print(f"GPT KEYS NOT FOUND (Looked in {__file__}):\n"
              "A 'keys.txt' file is required for the gpt parser to function\n"
              "Refer to the README in /gpt_keys for more information", e)
        raise FileNotFoundError

    # parser_chat = openai.OpenAI(api_key=openai_keys[0], organization=openai_keys[1])
    # parser_chat_lock = Lock()  # I think it's not needed due to GIL

    @staticmethod
    def classify(new_arg: dict, categories_arg: list) -> str | None:
        """Classifies a given new into one of the provided categories.

        :param new_arg: A dictionary containing 2 keys: title and body, of the New to be classified.
        :param categories_arg: List of categories.
        :returns: A string containing the category of the new, or None if the new does not belong to any of the categories.
        """
        # TODO This function is so bad it's painful to look at, ill rewrite it later
        # TODO make the prompt better and stuff
        classifier_client = openai.OpenAI(api_key=GptParser.openai_keys[0], organization=GptParser.openai_keys[1])
        response = classifier_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system",
                       "content": "You are a news articles classifying tool. The following messages will contain"
                                  "news articles structured as a json file, and you must classify them into one of "
                                  f"the following categories: {categories_arg}\n."
                                  "Return a string specifying the category the category the new belongs to.\n"
                                  "Return 'None' if not sure or the new doesnt fit in the categories"},
                      {"role": "user",
                       "content": dumps(new_arg)}])
        try:
            disaster_type = response.choices[0].message.content
        except TypeError:
            print("whf how did this happen")
            return None
        if disaster_type not in categories_arg:
            return None
        return disaster_type

    @staticmethod
    def extract_json(new_arg: dict, search_parameters_arg: list) -> str | None:
        """Analyzes the new and finds information according to the search parameters.
        This function is so bad it's painful to look at, ill rewrite it later

        :param new_arg: A dictionary containing 2 keys: title and body, of the New to be classified.
        :param search_parameters_arg: A list of parameters to fulfill. Eg; ("date", "number_of_deaths"...).
        :returns: Either a string formatted in json, or None in case of fatal error."""
        # TODO make the prompt better and E N S U R E it outputs correct json
        parser_client = openai.OpenAI(api_key=GptParser.openai_keys[0], organization=GptParser.openai_keys[1])
        response = parser_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system",
                       "content": "You are a scraping tool. The following message will contain text from a new, parsed "
                                  "as a python dictionary, as well as a list of parameters. Parse the new, obtaining "
                                  "the data corresponding to each parameter, and return the answers in json format."
                                  "Each parameter is followed by the type it must be answered with in parenthesis;\n"
                                  "- int indicates unsigned integer. If an exact number cannot be extracted, provide a "
                                  "lower bound. For example, 'dozens' -> '12', 'hundreds' -> '100'\n"
                                  "- str indicates string\n"
                                  "- date indicates a string containing the date in the format: "
                                  "'from yyyy/mm/dd to yyyy/mm/dd'. If a specific date is unknown, replace its digits "
                                  "with '-'. For example, 'from 2020/01/-- to 2020/03/01' would represent a span of "
                                  "time starting some day in January of 2020 and ending in March first 2020.\n"
                                  "Note that these `type tags` are not to be included in the json output\n"
                                  "In case the article does not contain the information required to answer a "
                                  "particular parameter, its value should be 'null'\n"
                                  "Example:\n "
                                  "New: "
                                  "{'title': 'Dozens of people die in a forest fire', "
                                  "'body': 'In the first of may of this year, a fire in a forest in Norway"
                                  "caused the death of dozens of persons and the displacement of 100 persons.'}\n"
                                  "Parameters: ('Date (date)', 'Region (str)', "
                                  "'Number of lethal victims (int)', 'Author of the new (str)')\n\n"
                                  "In this case, the expected output would be:"
                                  '{\n"Number of lethal victims": 12,\n'
                                  '"Date of the disaster": "from 2023/05/01 to ----/--/--",\n'
                                  '"Region": "Norway"\n'
                                  '"Author of the new": none\n'
                                  '}'
                       },
                      {"role": "user",
                       "content": f"New: {dumps(new_arg)}\n"
                                  f"Parameters: {search_parameters_arg}"}
                      ])

        try:
            return response.choices[0].message.content
        except TypeError:
            return None
