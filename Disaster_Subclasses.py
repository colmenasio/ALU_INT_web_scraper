from abc import ABCMeta, abstractmethod


class UnableToDetectDisasterType(Exception):
    pass


class Disaster(metaclass=ABCMeta):
    """Abstract parent dataclass, whose children are different types of disasters (eg: flood, etc.)
        Note that this class and its children are nothing more than glorified data structures"""
    sub_classes = {}

    def __init__(self, unprocessed_data_arg: dict):
        self.start_date = None
        self.end_date = None
        self.killed = None
        self.victims = None
        self.displaced = None
        self.unprocessed_data = unprocessed_data_arg

    @abstractmethod
    def save_to_database(self):
        pass

    @abstractmethod
    def process_data(self):
        pass

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Disaster.sub_classes[cls.__name__] = cls


class NoneDisaster(Disaster):
    """Debugging tool that holds an unprocessed disaster subclass"""

    def __init__(self, contents_arg):
        super().__init__(contents_arg)

    def process_data(self):
        print(f"Suposse we are processing the data({self.__class__.__name__})")

    def save_to_database(self):
        print(self.unprocessed_data)


class Flood(Disaster):
    """Generic Flood Class"""

    def __init__(self, unprocessed_data_arg):
        super().__init__(unprocessed_data_arg)
        self.stuff = "initialize"

    def process_data(self):
        print(f"Suposse we are processing the data({self.__class__.__name__})")

    def save_to_database(self):
        print(self)
        raise NotImplementedError


class Drought(Disaster):
    """Generic Drought Class"""

    def __init__(self, unprocessed_data_arg):
        super().__init__(unprocessed_data_arg)
        self.stuff = "initialize"

    def process_data(self):
        print(f"Suposse we are processing the data({self.__class__.__name__})")

    def save_to_database(self):
        print(self)
        raise NotImplementedError


class Earthquake(Disaster):
    """Generic Earthquake Class"""

    def __init__(self, unprocessed_data_arg):
        super().__init__(unprocessed_data_arg)
        self.stuff = "initialize"

    def process_data(self):
        print(f"Suposse we are processing the data({self.__class__.__name__})")

    def save_to_database(self):
        print(self)
        raise NotImplementedError


class ForestFire(Disaster):
    """Generic ForestFire Class"""

    def __init__(self, unprocessed_data_arg):
        super().__init__(unprocessed_data_arg)
        self.stuff = "initialize"

    def process_data(self):
        print(f"Suposse we are processing the data({self.__class__.__name__})")

    def save_to_database(self):
        print(self)
        raise NotImplementedError


class Tsunami(Disaster):
    """Generic Tsunami Class"""

    def __init__(self, unprocessed_data_arg):
        super().__init__(unprocessed_data_arg)
        self.stuff = "initialize"

    def process_data(self):
        print(f"Suposse we are processing the data({self.__class__.__name__})")

    def save_to_database(self):
        print(self)
        raise NotImplementedError


class Volcano(Disaster):
    """Generic Volcano Class"""

    def __init__(self, unprocessed_data_arg):
        super().__init__(unprocessed_data_arg)
        self.stuff = "initialize"

    def process_data(self):
        print(f"Suposse we are processing the data({self.__class__.__name__})")

    def save_to_database(self):
        print(self)
        raise NotImplementedError


class Pandemic(Disaster):
    """Generic Volcano Class"""

    def __init__(self, unprocessed_data_arg):
        super().__init__(unprocessed_data_arg)
        self.stuff = "initialize"

    def process_data(self):
        print(f"Suposse we are processing the data({self.__class__.__name__})")

    def save_to_database(self):
        print(self)
        raise NotImplementedError


if __name__ == "__main__":
    a = Disaster.sub_classes["Flood"]({"link": "nothing.com", "title": "Ejemplo titulo", "body": "nada de nada"})
    print(list(Disaster.sub_classes.keys()))
    print(a.stuff)
    a.process_data()
