# -*- coding: utf-8 -*-

"""
Module that contains some common functions to handle with mongo database connections.
It's a wrapper to *pymongo*
"""

from typing import Any, Dict, List
from modules.ahp.Types import FormData
from modules.util import SigaaDatabase
from bson.objectid import ObjectId


class AhpForm(SigaaDatabase):
    """
    A mongodb class used to connect and retrieve (already parsed), objects.
    Those objects are the answers of `AHP`_ site.
    """

    def findById(self, id: str) -> FormData:
        """
        Find an element by a given Id.

        :Parameters:
            - `id`: The unique identifier.

        :Returns:
            A :class:`.Types.FormData` for the matched object.
        """
        element = self._db.AhpForm.find_one(ObjectId(id))
        return FormData(element)  # type:ignore

    def findByDict(self, args: Dict[str, Any]) -> FormData:
        """
        Find an element by a given Id.

        :Parameters:
            - `args`: A dictionary containing the filters to object keys.

        :Returns:
            A :class:`.Types.FormData` for the matched object.
        """
        element = self._db.AhpForm.find_one(args)
        return FormData(element)  # type:ignore

    def getAll(self) -> List[FormData]:
        """
        Get all database elements.

        :Returns:
            A *List* of :class:`.Types.FormData` objects, containing all database elements.
        """
        # iterate and get all elements
        cursor = self._db.AhpForm.find()
        elements = [FormData(el) for el in cursor]
        return elements

    def insert(self, args) -> FormData:
        """
        Insert a new item in database.

        :Parameters:
            - `args`:
                You should pass a dictionary with the necessary
                keys to this database collection.
                You can use the :class:`.Types.FormData` object, and then, call the :meth:`modules.ahp.Types.FormData.toDict` .

        :Returns:
            A :class:`.Types.FormData` for the matched object.
        """
        element = self._db.AhpForm.insert_one(args)
        return FormData(element)  # type:ignore

    def delete(self, id: str) -> FormData:
        """
        Remove an element from this table

        :Parameters:
            - `id`: An unique identifier to this json object that will be, permanenlty, removed from database.

        """
        element = self.findById(ObjectId(id))  # type:ignore
        self._db.AhpForm.delete_one(ObjectId(id))
        return element
