from __future__ import annotations
import json
import pprint
from typing import Dict, List
from copy import deepcopy


class FormData:
    def __init__(self, obj: Dict = {}):
        if not obj:
            # create a sample model
            self._obj = {
                'date': 'None',
                'email': 'None',
                'matrices': {
                    'q1': 'A 6x6 matrix',
                    'q12': 'A 3x3 matrix',
                    'q13': 'A 6x6 matrix',
                    'q15': 0,
                    'q2': 'A 5x5 matrix',
                    'q3': 'A 4x4 matrix',
                    'root': 'A 3x3 matrix'
                },
                'name': 'SomeName'
            }
        else:
            self._obj = deepcopy(obj)

    def setEmail(self, email: str) -> FormData:
        self._obj['email'] = email
        return self

    def setName(self, name: str) -> FormData:
        self._obj['name'] = name
        return self

    def setDate(self, date: str) -> FormData:
        self._obj['date'] = date
        return self

    def setMatrixRoot(self, matrix: List[List]) -> FormData:
        self._obj['matrices']['root'] = matrix
        return self

    def setMatrixQ1(self, matrix: List[List]) -> FormData:
        self._obj['matrices']['q1'] = matrix
        return self

    def setMatrixQ1sec2(self, matrix: List[List]) -> FormData:
        self._obj['matrices']['q12'] = matrix
        return self

    def setMatrixQ1sec3(self, matrix: List[List]) -> FormData:
        self._obj['matrices']['q13'] = matrix
        return self

    def setMatrixQ1sec5(self, number: int) -> FormData:
        self._obj['matrices']['q15'] = number
        return self

    def setMatrixQ2(self, matrix: List[List]) -> FormData:
        self._obj['matrices']['q2'] = matrix
        return self

    def setMatrixQ3(self, matrix: List[List]) -> FormData:
        self._obj['matrices']['q3'] = matrix
        return self

    def parse(self) -> json:
        """
        Parse into json objects. It's a destructive action

        Return
        ------
        Parsed json objects
        """
        if "id" in self._obj:
            # already parsed
            pass
        else:
            obj_id = self._obj.pop('_id')
            self._obj['id'] = str(obj_id)
            self._obj = json.loads(json.dumps(self._obj))
        return self

    def __repr__(self) -> str:
        return pprint.pformat(self._obj, indent=1)

    def pretty(self) -> str:
        local_obj = deepcopy(self._obj)

        if "id" not in local_obj:
            obj_id = local_obj.pop('_id')
            local_obj['id'] = str(obj_id)
            local_obj = json.loads(json.dumps(local_obj))

        return pprint.pformat(local_obj, indent=1)

    def getEmail(self) -> str:
        return self._obj['email']

    def getName(self) -> str:
        return self._obj['name']

    def getDate(self) -> str:
        return self._obj['date']

    def getMatrices(self) -> List[Dict]:
        return self._obj['matrices']

    def getRoot(self) -> str:
        return self._obj['matrices']['q1']

    def getMatrixQ1sec2(self) -> str:
        return self._obj['matrices']['q12']

    def getMatrixQ1sec3(self) -> str:
        return self._obj['matrices']['q13']

    def getMatrixQ1sec5(self) -> str:
        return self._obj['matrices']['q15']

    def getMatrixQ2(self) -> str:
        return self._obj['matrices']['q2']

    def getMatrixQ3(self) -> str:
        return self._obj['matrices']['q3']

    def toDict(self) -> Dict:
        return self._obj

    def getDict(self) -> Dict:
        return self.toDict()
