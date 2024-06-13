from __future__ import annotations

from json import load


class Categories:
    """Wrapper over the categories.json to be sent to the openai API"""
    CATEGORIES_PATH = "../configs/categories/categories.json"

    def __init__(self, questions_arg: dict):
        self._questions = questions_arg

    @staticmethod
    def build_from_json() -> Categories:
        with open(Categories.CATEGORIES_PATH) as fstream:
            raw_categories = load(fstream)
        categories = dict()
        for category in raw_categories:
            categories[category] = Categories._validate_questions(raw_categories[category])
        return Categories(categories)

    @staticmethod
    def _validate_questions(questions_arg: list[dict]) -> tuple[dict]:
        """Makes sure the questions_arg follow the required format and parses them into tuples instead of lists"""
        for question in questions_arg:
            if not set(question.keys()).issubset({'parameter_name', 'question', 'format'}):
                raise IOError("Question parameters were missing\n."
                              "In the categories.json.json file, questions_arg must have the following three fields: "
                              "'parameter_name', 'question' and 'format'\n")

        return tuple(questions_arg)

    def get_categories(self) -> [str]:
        return list(self._questions.keys())

    def get_questions_for(self, category: str) -> tuple[dict]:
        questions = self._questions.get(category)
        if questions is None:
            raise KeyError(f"Tried acessing the {category} category, which is not defined in categories.json")
        return questions
