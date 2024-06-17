from source.database_integration.MakeConnectionPool import MakeConnectionPool


class Connector_Example:
    ID_counter = 0

    def __init__(self):
        self.ID = self.generate_id()
        self.letter = "superduper"[self.ID % 10]

    @classmethod
    def generate_id(cls) -> int:
        ID = cls.ID_counter
        cls.ID_counter += 1
        return ID

    def __enter__(self):
        return self.letter

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Releasing connector with ID: {self.ID}")


if __name__ == '__main__':
    with MakeConnectionPool(Connector_Example, 10) as pool:
        print("Connection pool made, now we would do operations")
        print(f"The resources we got are: {pool}")
    print("By now all resources should have been released")

