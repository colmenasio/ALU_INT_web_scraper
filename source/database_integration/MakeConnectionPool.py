class MakeConnectionPool:
    """A context manager to deal with several connections in a 'arena' sort of way"""
    pass

    def __init__(self, DatabaseClass, number_of_connections_arg: int):
        """Create a connection pool for context management. Meant to be used in a with block, returning an array of
        instances the provided DatabaseClass

        :arg DatabaseClass: Class to be instanciated. Needs to inherit from the AbsDatabase class
        :arg number_of_connections_arg: Number of connections to be opened"""
        self._db_instances = [DatabaseClass() for _ in range(number_of_connections_arg)]  # Instanciate the connections

    def __enter__(self):
        return self._db_instances

    def __exit__(self, exc_type, exc_val, exc_tb):
        for db_instances in self._db_instances:
            db_instances.close_connection()
