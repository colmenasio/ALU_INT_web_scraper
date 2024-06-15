from abc import ABC, abstractmethod

# TODO tbh i think this is too much voodo. It makes clear the interface for future implementations of other databases,
#  but is it really worth the extra abstraction?? Maybe ill remove in the future


class AbsDatabase(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        """Logs in, does the setup necessary to get the connection going, handles creation
        of the database in case of its non-existence, etc..."""
        pass

    @abstractmethod
    def save_to_database(self, disaster_instance_arg) -> None:
        """Stores the data passed in the disaster_instace """
        pass

    @abstractmethod
    def close_connection(self) -> None:
        pass
