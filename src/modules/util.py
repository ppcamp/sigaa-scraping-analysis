# -*- coding: utf-8 -*-

"""
A module containing some usefull functions that can be shared with another modules
"""

from __future__ import annotations
from typing import Dict, List
import logging as logger
import sys
from pymongo import MongoClient


class SigaaDatabase:
    """
    This class is responsable to fetch and push data to mongo
    """

    def __init__(self, connection_string: str, database_name: str = "") -> None:
        """
        Starts a mongodb client

        :Args:
            - `connection_string`: A connection string to mongo server.

        :Kwargs:
            - `database_name`: *OPTIONAL*, Default value is "sigaadb"
        """
        # Create a mongoclient
        self.__client = MongoClient(connection_string)

        if database_name:
            connection = "self.__client.{}".format(database_name)
            self._db = eval(connection)
        else:
            # Connect to database sigaadb (default)
            self._db = self.__client.sigaadb


def average(*args: List[float] or List[List[float]], roundp: int = 4):
    """
    Calculate the mean of a given amount of values.
    It can performs the mean over List[List[float]] or List[float].

    .. math:: \\frac{\\sum_{i=0}^N\\text{arg}_i}{N}

    :Args:
        - `*args`: A list of floats or a list of matrices

    :Kwargs:
        - `roundp`: Number of decimal places used to round

    :Example:
        .. code-block:: python
            :linenos:
            :caption: Using a list of float

            l = [1, 1, 1, 1, 1]
            # will not throw an error
            assert 1 == average(*l)

        .. code-block:: python
            :linenos:
            :caption: Using a list of list of floats

            from copy import deepcopy

            a = [
                [1, 1, 1],
                [1, 1, 1],
            ]
            b = deepcopy(a)

            result = average(a,b)
            expected_result = deepcopy(a)

            # iterate and raise an error. P.S.: It won't throw any error
            for row in range(2):
                for col in range(3):
                    assert result[row][col] == expected_result[row][col]
    """
    from statistics import mean

    # must exist at least two matrices
    if len(args) < 2:
        raise Exception("Must exist at least two itens")

    if type(args[0]) is not list:
        out = round(mean([scalar for scalar in args]), roundp)  # type:ignore
        return out

    matrix_length = len(args[0])
    # create a new matrix
    output_matrix = [[0]*matrix_length]*matrix_length

    # calcula a média item a item
    for row in range(matrix_length):
        for col in range(matrix_length):
            output_matrix[row][col] = round(
                mean([m[row][col] for m in args]), roundp)  # type: ignore

    return output_matrix


def normalize_vectors(d: Dict[str, float], roundp: int = 4) -> Dict[str, float]:
    """
    Normalize a dictionary basing on its maximum value.

    .. warning:: This function should be used?

    .. todo:: Remove this function

    :Args:
        - `d`: A dictionary mapping competency with value. \
            Usually, based on :meth:`.Ahp.mapping_competences`

    :Kwargs:
        - `roundp`: The number of decimal places used to round

    :Returns:
        The competency mapping normalized by its maximum value.
    """
    logger.debug("Normalizing vectors")
    maxv: float = sum(d.values())
    n: Dict[str, float] = {}
    for k, v in d.items():
        res = round(v/maxv, roundp)
        n[k] = res
    logger.debug("Returning normalized vectors")
    return n


def errprint(msg: str) -> None:
    """
    Print some error message, returning a different value from default (1).

    :Args:
        - `msg`: Message to be shown
    """
    sys.stderr.write('Error: ' + msg)
