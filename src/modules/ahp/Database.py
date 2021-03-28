from typing import Dict, List
from modules.ahp.Types import FormData
from modules.util import SigaaDatabase
from bson.objectid import ObjectId


class AhpForm(SigaaDatabase):
    def findById(self, id: str) -> FormData:
        element = self._db.AhpForm.find_one(ObjectId(id))
        return FormData(element)  # type:ignore

    def findByDict(self, args: Dict) -> FormData:
        element = self._db.AhpForm.find_one(args)
        return FormData(element)  # type:ignore

    def getAll(self) -> List[FormData]:
        # iterate and get all elements
        cursor = self._db.AhpForm.find()
        elements = [FormData(el) for el in cursor]
        return elements

    def insert(self, args) -> FormData:
        element = self._db.AhpForm.insert_one(args)
        return FormData(element)  # type:ignore

    def delete(self, id: str) -> FormData:
        """
        Remove an element from this table

        :Parameters:
            - `id`: An unique identifier to this json object

        """
        element = self.findById(ObjectId(id))  # type:ignore
        self._db.AhpForm.delete_one(ObjectId(id))
        return element
