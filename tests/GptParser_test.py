from source.GptParser import GptParser
import tests.test_samples.some_news as test_cases
from json import loads, JSONDecodeError


def run_tests():
    test_classifier()


def test_classifier():
    assert GptParser.classify(test_cases.NEW_FOREST_FIRE, test_cases.CATEGORIES) == "Forest Fire"
    assert GptParser.classify(test_cases.NEW_EARTHQUAKE, test_cases.CATEGORIES) == "Earthquake"
    assert GptParser.classify(test_cases.NEW_MEDICINE, test_cases.CATEGORIES) == "Medicine"
    assert GptParser.classify(test_cases.NEW_TECH, test_cases.CATEGORIES) is None


def test_extract_json_produces_json():
    assert is_valid_json(GptParser.extract_json(test_cases.NEW_FOREST_FIRE, ["number of victims", "name of the author"]))


def is_valid_json(string: str) -> bool:
    try:
        loads(string)
    except JSONDecodeError as e:
        print(e)
        return False
    return True


if __name__ == "__main__":
    run_tests()
