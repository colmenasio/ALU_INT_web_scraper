
class InvalidCategoryErr(Exception):
    """To be raised when the classifier wasn't able to classify a given new"""
    def __init__(self):
        super().__init__("Classifier could not classify the new into any given category")


class InsufficientInformation(Exception):
    """The called method requires more information"""
    def __init__(self, method_name, required_parameters):
        super().__init__(f"The method: {method_name} requires {required_parameters} to be specified")
