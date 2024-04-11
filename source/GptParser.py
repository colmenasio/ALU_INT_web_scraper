from __future__ import annotations

import warnings
from json import load
import openai


class GptParser:
    try:
        with open("../config/gpt_keys/keys.json") as fstream:
            keys_json = load(fstream)
            if keys_json.get("key") is None:
                raise IOError("keys.json does not have a 'key' field")
            if keys_json.get("organization") is None:
                warnings.warn("keys.json does not have a 'organization' field")
            openai_keys = (
                keys_json.get("key"),
                keys_json.get("organization")
            )
            del keys_json
    except FileNotFoundError as e:
        print(f"GPT KEYS NOT FOUND (Looked in {__file__}):\n"
              "A 'keys.json' file is required for the gpt parser to function\n"
              "Refer to the README in /gpt_keys for more information\n", e)
        raise FileNotFoundError

    # parser_chat_lock = Lock()  # I think it's not needed due to GIL

    @staticmethod
    def classify(new_arg: dict, categories_arg: [str]) -> str | None:
        """Classifies a given new into one of the provided categories.json.

        :param new_arg: A dictionary containing 2 keys: title and body, of the New to be classified.
        :param categories_arg: List of categories.json.
        :returns: A string containing the category of the new, or None if the new does not belong to any of the categories.json.
        """
        # TODO make the prompt better and stuff
        if len(categories_arg) == 0:
            raise ValueError("Categories were not specified for the classifier!")
        stringified_new = GptParser._stringify_new(new_arg)

        classifier_client = openai.OpenAI(api_key=GptParser.openai_keys[0], organization=GptParser.openai_keys[1])
        response = classifier_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system",
                       "content": "You are a news articles classifying tool.\n"
                                  "You will be given a news article and your task it to classify it "
                                  f"into one of the following categories.json: {categories_arg}\n."
                                  "Awnser the category that best fits the new.\n"
                                  "Awnser 'None' the new does not fit any of the categories.json given.\n\n"
                                  "The new you must classify is the following:\n"
                                  f"{stringified_new}"}
                      ])
        try:
            disaster_type = response.choices[0].message.content
        except TypeError:
            print("whf how did this happen")
            return None
        if disaster_type not in categories_arg:
            return None
        return disaster_type

    @staticmethod
    def answer_questions(new_arg: dict, questions_arg: tuple[dict]) -> dict:
        sys_message = "You are a news scraping tool.\n" \
                      "You will be provided with a news article, and then the following user messages will ask " \
                      "categories.json about the content of the text.\n" \
                      "Your job is to answer those categories.json according to the new you will be provided.\n" \
                      "Said categories.json will consist of a question and a format the answer must be in.\n" \
                      "The format can either be:\n" \
                      "- int: The answer must be numeric (20, 123...). " \
                      "If inexact numerals are present (such as 'hundreds' or 'dozens') " \
                      "interpret them as numeric ('100' and '12' respectively)\n" \
                      "- str: The answer must be a character string\n" \
                      "- date: The asnwer mus be in ISO 8601 format\n\n" \
                      "In case the new contains only partial information try to give an approximate answer " \
                      "according to the format\n" \
                      "In case the new does not contain enough information for even an approximate answer, " \
                      "answer 'None'\n" \
                      "You must be as concise as possible. " \
                      "Only anwser in the format you are given, and use as few words as possible.\n" \
                      "Do not try to answer with a fully structured sentence if not necesary. " \
                      "Just answer in the format you are given" \
                      "For example, if you are asked where did the event take place in, only answer the location\n" \
                      "Here are some examples on how you are expected to operate:\n" \
                      "Examples:\n" \
                      "-News Article: \n" \
                      "*Dozens of people die in a forest fire*\n" \
                      "In the first of may of this year, a fire in a forest in Norway" \
                      "caused the death of dozens of persons and the displacement of 100 people.\n\n" \
                      "-Question: How many people died?\n" \
                      "-Format: integer\n" \
                      "In this case, your answer should be '12'\n\n" \
                      "Here is another example:\n" \
                      "-News Article: " \
                      "*Earthquake hits tokyo*\n" \
                      "This week a horrible earthquake of magnitude 5 hit the city of tokyo, causing estimated " \
                      "damages of over 1 Million dollars\n\n" \
                      "-Question: What are the estimated damages in dollars?\n" \
                      "-Format: integer\n" \
                      "In this case, your answer should be: '1000000'\n\n" \
                      "Here is a third example:\n" \
                      "-News Article: " \
                      "*Plague of malaria hits nigeria*\n" \
                      "The numbers of cases of malaria detected over the last few weeks in nigeria has rising in an" \
                      "unexpected fashion. Over a thousand cases were detected, " \
                      "already 100 lethal victims are confirmed \n\n" \
                      "-Question: How many people were infected?\n" \
                      "-Format: integer\n" \
                      "In this case, your answer should be: '1000'\n\n"
        results = dict()
        for question in questions_arg:
            parser_client = openai.OpenAI(api_key=GptParser.openai_keys[0], organization=GptParser.openai_keys[1])
            response = parser_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": sys_message},
                    {"role": "user",
                     "content": f"-News Article:\n {GptParser._stringify_new(new_arg)}\n\n"
                                f"-Question: {question['question']}\n"
                                f"-Format: {question['format']}"}
                ]
            )
            try:
                answer = GptParser._type_cast_answer(response.choices[0].message.content, question['format'])
            except TypeError:
                answer = None
            except ValueError:
                answer = None
            results[f"{question['parameter_name']}"] = answer
        return results

    @staticmethod
    def _stringify_new(new_arg: dict) -> str | None:
        title = new_arg.get("title")
        body = new_arg.get("body")
        if title is None or body is None:
            raise ValueError("The new is missing either a title or a body key!")
        return f"*{title}*\n{body}\n\n"

    @staticmethod
    def _type_cast_answer(answer: str, result_format: str):
        if result_format == "int":
            return int(answer.rstrip())
        if result_format == "str":
            return answer
        if result_format == "date":
            return answer
        raise ValueError(f"GptParser tried casting its answer to {result_format}, "
                         "which is a type for which answer casting is not yet implemented")
