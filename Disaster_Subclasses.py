from abc import ABCMeta, abstractmethod


class UnableToDetectDisasterType(Exception):
    pass


class Disaster(metaclass=ABCMeta):
    """Abstract parent dataclass, whose children are different types of disasters (eg: flood, etc.)
        Note that this class and its children are nothing more than glorified data structures"""

    def __init__(self, start_date_arg, end_date_arg, killed_arg: int, victims_arg: int, displaced_arg: int):
        self.start_date = start_date_arg
        self.end_date = end_date_arg
        self.killed = killed_arg
        self.victims = victims_arg
        self.displaced = displaced_arg

    @abstractmethod
    def save_to_database(self):
        pass


class NoneDisaster(Disaster):
    """Debugging tool that holds an unprocessed disaster subclass"""
    def __init__(self, contents_arg):
        super().__init__(0, 0, 0, 0, 0)
        self.unprocessed_contents = contents_arg

    def save_to_database(self):
        print(self.unprocessed_contents)


class Flood(Disaster):
    """Generic Flood Class"""
    def __init__(self):
        super().__init__(0, 0, 0, 0, 0)
        self.stuff = "initialize"

    def save_to_database(self):
        print(self)
        raise NotImplementedError


class Drought(Disaster):
    """Generic Drought Class"""
    def __init__(self):
        super().__init__(0, 0, 0, 0, 0)
        self.stuff = "initialize"

    def save_to_database(self):
        print(self)
        raise NotImplementedError


class Earthquake(Disaster):
    """Generic Earthquake Class"""
    def __init__(self):
        super().__init__(0, 0, 0, 0, 0)
        self.stuff = "initialize"

    def save_to_database(self):
        print(self)
        raise NotImplementedError


class ForestFire(Disaster):
    """Generic ForestFire Class"""
    def __init__(self):
        super().__init__(0, 0, 0, 0, 0)
        self.stuff = "initialize"

    def save_to_database(self):
        print(self)
        raise NotImplementedError


class Tsunami(Disaster):
    """Generic Tsunami Class"""
    def __init__(self):
        super().__init__(0, 0, 0, 0, 0)
        self.stuff = "initialize"

    def save_to_database(self):
        print(self)
        raise NotImplementedError


class Volcano(Disaster):
    """Generic Volcano Class"""
    def __init__(self):
        super().__init__(0, 0, 0, 0, 0)
        self.stuff = "initialize"

    def save_to_database(self):
        print(self)
        raise NotImplementedError
