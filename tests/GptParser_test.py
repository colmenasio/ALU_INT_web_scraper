from source.GptParser import GptParser
import tests.test_samples.some_news as test_cases


def run_tests():
    test_classifier()


def test_classifier():
    print(GptParser.openai_keys)  # TODO WHYYYYY WHY DOES THE CLASS NOT INITIALIZE O N L Y IN THE TESTS
    assert GptParser.classify(test_cases.NEW_FOREST_FIRE, test_cases.CATEGORIES) == "Forest Fire"
    assert GptParser.classify(test_cases.NEW_EARTHQUAKE, test_cases.CATEGORIES) == "Earthquake"
    assert GptParser.classify(test_cases.NEW_MEDICINE, test_cases.CATEGORIES) == "Medicine"
    assert GptParser.classify(test_cases.NEW_TECH, test_cases.CATEGORIES) == "None"


if __name__ == "__main__":
    run_tests()
