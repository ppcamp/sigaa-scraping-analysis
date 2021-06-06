# -*- coding: utf-8 -*-

"""
Module that contains some common functions to handle with mongo database connections.
It's a wrapper to *pymongo*.

Todo
----
Implement tests for:

- test_findById
- test_findByDict
- test_getAll
- test_insert
- test_delete
"""


from typing import Any, Dict, List, Union
from modules.ahp.Types import FormData, FormDataType
from bson.objectid import ObjectId
from pymongo import MongoClient
import logging
logger = logging.getLogger(__name__)


class SigaaDatabase:
    """
    This class is responsable to fetch and push data to mongo

    Args
    ----
    `connection_string`:
        A connection string to mongo server.

    Keyword Args
    ------------
    `database_name`:
        *OPTIONAL*, Default value is "sigaadb"
    """

    def __init__(self, connection_string: str, database_name: str = "") -> None:
        # Create a mongoclient
        self.__client = MongoClient(connection_string)

        logger.info(f'Creating a MongoClient for {connection_string}')

        if database_name:
            connection = "self.__client.{}".format(database_name)
            self._db = eval(connection)
        else:
            # Connect to database sigaadb (default)
            self._db = self.__client.sigaadb


class AhpForm(SigaaDatabase):
    """
    A mongodb class used to connect and retrieve (already parsed), objects.
    Those objects are the answers of *AHP* site.

    Todo
    ----
    Missing tests

    Example
    -------
    >>> # import this module
    >>> from modules.ahp import Database
    >>> # mongodb connection string
    >>> connection_string = "mongodb://ppcamp:password@localhost:27017/?authSource=admin"
    >>> ahp = Database.AhpForm(connection_string)
    """

    def findById(self, id: str) -> Union[FormData, None]:
        """
        Find an element by a given Id.

        Args
        ----
        `id`:
            The unique identifier.

        Returns
        -------
        Union[FormData, None]
            A :class:`.Types.FormData` for the matched object (or None, if dind't find none)

        Example
        -------
        >>> resp = ahp.findById("7ab8ccba-e123-4e52-835a-93fd8b86b1b7")
        """
        element = self._db.AhpForm.find_one(ObjectId(id))
        if element is None:
            return None
        return FormData(element)  # type:ignore

    def findByDict(self, args: Dict[str, Any]) -> List[FormData]:
        """
        Find a *list* of elements that matches with this field.

        Args
        ----
        `args`:
            A dictionary containing the filters to object keys.

        Returns
        -------
        List[FormData]
            A :class:`.Types.FormData` for the matched object.

        Example
        -------
        >>> resp = ahp.findByDict({"email":"7ab8ccba-e123-4e52-835a-93fd8b86b1b7"})

        Important
        ---------
        The list will be empty if didn't found objects that matches with it
        """
        element = self._db.AhpForm.find(args)
        element = list(map(lambda el: FormData(el), element))  # type: ignore
        return element

    def findByType(self, type: FormDataType) -> List[FormData]:
        """
        Find an element by a given Id.

        Args
        -----
        `type`:
            The type of the searched element

        Returns
        -------
        List[FormData]
            A :class:`.Types.FormData` for the matched object.

        Example
        -------
        >>> answers = ahp.findByType({"email":"7ab8ccba-e123-4e52-835a-93fd8b86b1b7"})

        Important
        ---------
        The list will be empty if didn't found objects that matches with it
        """
        return self.findByDict({"type": type.value})

    def getAll(self) -> List[FormData]:
        """
        Get all database elements.

        Returns
        -------
        List[FormData]
            A *List* of :class:`.Types.FormData` objects, containing all database elements.

        Example
        -------
        >>> responses = ahp.getAll()

        Important
        ---------
        The list will be empty if didn't found objects that matches with it
        """
        # iterate and get all elements
        cursor = self._db.AhpForm.find()
        elements = [FormData(el) for el in cursor]
        return elements

    def insert(self, args) -> FormData:
        """
        Insert a new item in d-atabase.

        Args
        -----
        `args`:
            You should pass a dictionary with the necessary \
                keys to this database collection. \
                    You can use the :class:`.Types.FormData` object, \
                        and then, call the :meth:`modules.ahp.Types.FormData.toDict` .

        Returns
        -------
        FormData
            A :class:`.Types.FormData` for the matched object.

        Example
        -------
        >>> from modules.ahp.Types import FormData
        >>> from modules.ahp import Database
        >>> ahp = Database.AhpForm(connection_string)
        >>> # lRoot, q1s2, q1sec5, q3
        >>> new_response = FormData() \\
        ... .setName("Joãozinho") \\
        ... .setEmail("joaozinho@teste.com") \\
        ... .setDate("03-03-2021") \\
        ... .setMatrixRoot([
        ...    [1,1,0.33],
        ...    [1,1,0.33],
        ...    [3.03,3.03,1],
        ... ]) \\
        ... .setMatrixQ1([
        ...    [1,5,5,5,1,1],
        ...    [0.2,1,1,1,0.2,0.2],
        ...    [0.2,1,1,1,0.2,0.2],
        ...    [0.2,1,1,1,0.2,0.2],
        ...    [1,5,5,5,1,1],
        ...    [1,5,5,5,1,1],
        ... ]) \\
        ... .setMatrixQ1sec2([
        ...    [1,1,1],
        ...    [1,1,1],
        ...    [1,1,1],
        ... ]) \\
        ... .setMatrixQ1sec3([
        ...    [1,3,1,5,3,5],
        ...    [0.33,1,0.33,5,1,3],
        ...    [1,3.03,1,5,1,3],
        ...    [0.2,0.2,0.2,1,0.2,0.33],
        ...    [0.33,1,1,5,1,3],
        ...    [0.2,0.33,0.33,3.03,0.33,1],
        ... ]) \\
        ... .setMatrixQ1sec5(0.2) \\
        ... .setMatrixQ2([
        ...    [1,0.33,3,3,3],
        ...    [3.03,1,3,5,3],
        ...    [0.33,0.33,1,1,1],
        ...    [0.33,0.2,1,1,1],
        ...    [0.33,0.33,1,1,1],
        ... ]) \\
        ... .setMatrixQ3([
        ...    [1,0.33,1,1],
        ...    [3.03,1,3,3],
        ...    [1,0.33,1,1],
        ...    [1,0.33,1,1],
        ... ])
        >>> ahp.insert(new_response.toDict())
        """
        element = self._db.AhpForm.insert_one(args)
        logger.debug('Data inserted into Database')
        return FormData(element)  # type:ignore

    def delete(self, id: str) -> FormData:
        """
        Remove an element from this table

        Args
        -----
        `id`:
            An unique identifier to this json object that will be, permanenlty, removed from database.

        Example
        -------
        >>> removed_el = ahp.delete("5cbfb7d6-c6b9-4342-8c9b-52d6a9a9ed2f")

        Raises
        ------
        `ValueError`
            The element with this id couldn't be found
        """
        element: Union[FormData, None] = self.findById(
            ObjectId(id))  # type:ignore
        if element is None:
            raise ValueError(
                f'Couldn\'t found an object associated with this id ({id})')
        self._db.AhpForm.delete_one(ObjectId(id))
        logger.debug(f'Object({id}) removed from database')
        return element
