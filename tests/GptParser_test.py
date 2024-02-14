from source.GptParser import GptParser
import tests.test_samples.some_news as test_cases
from json import loads, JSONDecodeError


def run_tests():
    test_classifier()


def test_classifier():
    assert GptParser.classify(test_cases.NEW_FOREST_FIRE, test_cases.CATEGORIES) == "Forest Fire"
    print("next")
    assert GptParser.classify(test_cases.NEW_EARTHQUAKE, test_cases.CATEGORIES) == "Earthquake"
    print("next")
    assert GptParser.classify(test_cases.NEW_MEDICINE, test_cases.CATEGORIES) == "Medicine"
    print("next")
    assert GptParser.classify(test_cases.NEW_TECH, test_cases.CATEGORIES) is None


def is_valid_json(string: str) -> bool:
    try:
        loads(string)
    except JSONDecodeError as e:
        print(e)
        return False
    return True


if __name__ == "__main__":
    run_tests()
