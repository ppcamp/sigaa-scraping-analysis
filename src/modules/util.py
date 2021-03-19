from __future__ import annotations

# MongoDB
from pymongo import MongoClient
# from bson.objectid import ObjectId


class SigaaDatabase:
    """
    This class is responsable to fetch and push data to mongo
    """

    def __init__(self, connection_string: str, database_name: str = "") -> SigaaDatabase:
        """
        Starts a mongodb client

        Parameters
        ----------
        connection_string: str
          A connection string to mongo server.
        database_name: str
          OPTIONAL, Default value is "sigaadb"

        """
        # Create a mongoclient
        self.__client = MongoClient(connection_string)

        if database_name:
            connection = "self.__client.{}".format(database_name)
            self._db = eval(connection)
        else:
            # Connect to database sigaadb (default)
            self._db = self.__client.sigaadb


def average(*args):
    from statistics import mean

    # must exist at least two matrices
    if len(args) < 2:
        raise Exception("Must exist at least two itens")

    if type(args[0]) is not list:
        out = round(mean([scalar for scalar in args]), 2)
        return out

    matrix_length = len(args[0])
    # create a new matrix
    output_matrix = [[0]*matrix_length]*matrix_length

    # calcula a média item a item
    for row in range(matrix_length):
        for col in range(matrix_length):
            output_matrix[row][col] = round(
                mean([m[row][col] for m in args]), 2)

    return output_matrix
