# -*- coding: utf-8 -*-

"""
Module that contains some common functions to handle with mongo database connections.
It's a wrapper to *pymongo*.

"""

from typing import Any, Dict, List
from modules.ahp.Types import FormData
from modules.util import SigaaDatabase
from bson.objectid import ObjectId


class AhpForm(SigaaDatabase):
    """
    A mongodb class used to connect and retrieve (already parsed), objects.
    Those objects are the answers of `AHP`_ site.

    :Example:
        .. code-block:: python

            # import this module
            from modules.ahp import Database

            # mongodb connection string
            connection_string = "mongodb://ppcamp:password@localhost:27017/?authSource=admin"
            ahp = Database.AhpForm(connection_string)

    """

    def findById(self, id: str) -> FormData:
        """
        Find an element by a given Id.

        :Args:
            - `id`: The unique identifier.

        :Returns:
            A :class:`.Types.FormData` for the matched object.

        :Example:
            .. code-block:: python

                resp = ahp.findById("7ab8ccba-e123-4e52-835a-93fd8b86b1b7")
        """
        element = self._db.AhpForm.find_one(ObjectId(id))
        return FormData(element)  # type:ignore

    def findByDict(self, args: Dict[str, Any]) -> FormData:
        """
        Find an element by a given Id.

        :Args:
            - `args`: A dictionary containing the filters to object keys.

        :Returns:
            A :class:`.Types.FormData` for the matched object.

        :Example:
            .. code-block:: python

                resp = ahp.findByDict({"email":"7ab8ccba-e123-4e52-835a-93fd8b86b1b7"})
        """
        element = self._db.AhpForm.find_one(args)
        return FormData(element)  # type:ignore

    def getAll(self) -> List[FormData]:
        """
        Get all database elements.

        :Returns:
            A *List* of :class:`.Types.FormData` objects, containing all database elements.

        :Example:
            .. code-block:: python

                # get all responses stored in database
                responses = ahp.getAll()
        """
        # iterate and get all elements
        cursor = self._db.AhpForm.find()
        elements = [FormData(el) for el in cursor]
        return elements

    def insert(self, args) -> FormData:
        """
        Insert a new item in database.

        :Args:
            - `args`:
                You should pass a dictionary with the necessary
                keys to this database collection.
                You can use the :class:`.Types.FormData` object, and then, call the :meth:`modules.ahp.Types.FormData.toDict` .

        :Returns:
            A :class:`.Types.FormData` for the matched object.

        :Example:
            .. code-block:: python

                from modules.ahp.Types import FormData
                from modules.ahp import Database

                ahp = Database.AhpForm(connection_string)

                # lRoot, q1s2, q1sec5, q3

                new_response = FormData() \\
                .setName("Joãozinho") \\
                .setEmail("joaozinho@teste.com") \\
                .setDate("03-03-2021") \\
                .setMatrixRoot([
                    [1,1,0.33],
                    [1,1,0.33],
                    [3.03,3.03,1],
                ]) \\
                .setMatrixQ1([
                    [1,5,5,5,1,1],
                    [0.2,1,1,1,0.2,0.2],
                    [0.2,1,1,1,0.2,0.2],
                    [0.2,1,1,1,0.2,0.2],
                    [1,5,5,5,1,1],
                    [1,5,5,5,1,1],
                ]) \\
                .setMatrixQ1sec2([
                    [1,1,1],
                    [1,1,1],
                    [1,1,1],
                ]) \\
                .setMatrixQ1sec3([
                    [1,3,1,5,3,5],
                    [0.33,1,0.33,5,1,3],
                    [1,3.03,1,5,1,3],
                    [0.2,0.2,0.2,1,0.2,0.33],
                    [0.33,1,1,5,1,3],
                    [0.2,0.33,0.33,3.03,0.33,1],
                ]) \\
                .setMatrixQ1sec5(0.2) \\
                .setMatrixQ2([
                    [1,0.33,3,3,3],
                    [3.03,1,3,5,3],
                    [0.33,0.33,1,1,1],
                    [0.33,0.2,1,1,1],
                    [0.33,0.33,1,1,1],
                ]) \\
                .setMatrixQ3([
                    [1,0.33,1,1],
                    [3.03,1,3,3],
                    [1,0.33,1,1],
                    [1,0.33,1,1],
                ])

                ahp.insert(new_response.toDict())
        """
        element = self._db.AhpForm.insert_one(args)
        return FormData(element)  # type:ignore

    def delete(self, id: str) -> FormData:
        """
        Remove an element from this table

        :Args:
            - `id`: An unique identifier to this json object that will be, permanenlty, removed from database.

        :Example:
            .. code-block:: python

                removed_el = ahp.delete("5cbfb7d6-c6b9-4342-8c9b-52d6a9a9ed2f")
        """
        element = self.findById(ObjectId(id))  # type:ignore
        self._db.AhpForm.delete_one(ObjectId(id))
        return element
