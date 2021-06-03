# -*- coding: utf-8 -*-

"""
Module that contains some common classes to handle with ahp data.
It has the class to hold and retrieve ahp data.
"""

from __future__ import annotations
from enum import Enum, unique
import json
import pprint
from typing import Any, Dict, List, Union
from copy import deepcopy


@unique
class FormDataType(Enum):
    TEACHER = 'teacher'
    MARKET = 'market'


class FormData:
    """
    .. _FormData:

    This class hold some usefull methods to handle with *AHP* site data.

    Examples
    --------

    Example passing a value from mongodb

        >>> # import this module
        >>> from modules.ahp import Types
        >>> # import object id (used to parse id into uuid object type)
        >>> from bson.objectid import ObjectId
        >>> # mongodb connection string
        >>> connection_string = "mongodb://ppcamp:password@localhost:27017/?authSource=admin"
        >>> # Create a mongoclient
        >>> client = MongoClient(connection_string)
        >>> # Connect to database sigaadb (default)
        >>> db = client.sigaadb
        >>> response = db.find_one(ObjectId("20de2b50-5349-4cae-b72e-d85ea47417f2"))

    Example using empty value

        >>> # import this module
        >>> from modules.ahp.Types import FormData
        >>> # lRoot, q1s2, q1sec5, q3
        >>> new_response = FormData() \\
        ... .setName("Joãozinho") \\
        ... .setEmail("joaozinho@teste.com") \\
        ... .setDate("03-03-2021") \\
        ... .setMatrixRoot([
        ...     [1,1,0.33],
        ...     [1,1,0.33],
        ...     [3.03,3.03,1],
        ... ]) \\
        ... .setMatrixQ1([
        ...     [1,5,5,5,1,1],
        ...     [0.2,1,1,1,0.2,0.2],
        ...     [0.2,1,1,1,0.2,0.2],
        ...     [0.2,1,1,1,0.2,0.2],
        ...     [1,5,5,5,1,1],
        ...     [1,5,5,5,1,1],
        ... ]) \\
        ... .setMatrixQ1sec2([
        ...     [1,1,1],
        ...     [1,1,1],
        ...     [1,1,1],
        ... ]) \\
        ... .setMatrixQ1sec3([
        ...     [1,3,1,5,3,5],
        ...     [0.33,1,0.33,5,1,3],
        ...     [1,3.03,1,5,1,3],
        ...     [0.2,0.2,0.2,1,0.2,0.33],
        ...     [0.33,1,1,5,1,3],
        ...     [0.2,0.33,0.33,3.03,0.33,1],
        ... ]) \\
        ... .setMatrixQ1sec5(0.2) \\
        ... .setMatrixQ2([
        ...     [1,0.33,3,3,3],
        ...     [3.03,1,3,5,3],
        ...     [0.33,0.33,1,1,1],
        ...     [0.33,0.2,1,1,1],
        ...     [0.33,0.33,1,1,1],
        ... ]) \\
        ... .setMatrixQ3([
        ...     [1,0.33,1,1],
        ...     [3.03,1,3,3],
        ...     [1,0.33,1,1],
        ...     [1,0.33,1,1],
        ... ])
    """

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
                'type': FormDataType.MARKET.value,
                'name': 'SomeName'
            }
        else:
            self._obj = deepcopy(obj)

    def setEmail(self, email: str) -> FormData:
        """
        Update the email of this object.

        Args
        ----
        `email`:
            An email string.

        Returns
        -------
        FormData
            This object itself. It can use nested calls.
        """
        self._obj['email'] = email
        return self

    def setType(self, type: FormDataType) -> FormData:
        """
        Update the type of this object.

        Args
        ----
        `type`:
            An type string. You should encounter in :class:`.FormDataType`

        Returns
        -------
        FormData
            This object itself. It can use nested calls.
        """
        self._obj['type'] = type.value
        return self

    def setName(self, name: str) -> FormData:
        """
        Update the name of this object.

        Args
        ----
        `name`:
            A string name.

        Returns
        -------
        FormData
            This object itself. It can use nested calls.
        """
        self._obj['name'] = name
        return self

    def setDate(self, date: str) -> FormData:
        """
        Update the date of this object.

        Args
        ----
        `date`:
            An date string.

        Returns
        -------
        FormData
            This object itself. It can use nested calls.
        """
        self._obj['date'] = date
        return self

    def setMatrixRoot(self, matrix: List[List[float]]) -> FormData:
        """
        Update the root of this object.

        Args
        -----
        `root`:
            An root matrix.

        Returns
        --------
        FormData
            This object itself. It can use nested calls.
        """
        self._obj['matrices']['root'] = matrix
        return self

    def setMatrixQ1(self, matrix: List[List[float]]) -> FormData:
        """
        Update the q1 matrix of this object.

        Args
        -----
        `matrix`:
            An q1 matrix.

        Returns
        --------
        FormData
            This object itself. It can use nested calls.
        """
        self._obj['matrices']['q1'] = matrix
        return self

    def setMatrixQ1sec2(self, matrix: List[List[float]]) -> FormData:
        """
        Update the Q1sec2 matrix of this object.

        Args
        -----
        `matrix`:
            An Q1sec2 matrix.

        Returns
        --------
        FormData
            This object itself. It can use nested calls.
        """
        self._obj['matrices']['q12'] = matrix
        return self

    def setMatrixQ1sec3(self, matrix: List[List[float]]) -> FormData:
        """
        Update the Q1sec3 matrix of this object.

        Args
        -----
        `matrix`:
            An Q1sec3 matrix.

        Returns
        --------
        FormData
            This object itself. It can use nested calls.
        """
        self._obj['matrices']['q13'] = matrix
        return self

    def setMatrixQ1sec5(self, number: int) -> FormData:
        """
        Update the Q1sec5 matrix of this object.

        Args
        -----
        `matrix`:
            An Q1sec5 matrix.

        Returns
        --------
        FormData
            This object itself. It can use nested calls.
        """
        self._obj['matrices']['q15'] = number
        return self

    def setMatrixQ2(self, matrix: List[List[float]]) -> FormData:
        """
        Update the Q2 matrix of this object.

        Args
        -----
        `matrix`:
            An Q2 matrix.

        Returns
        --------
        FormData
            This object itself. It can use nested calls.
        """
        self._obj['matrices']['q2'] = matrix
        return self

    def setMatrixQ3(self, matrix: List[List[float]]) -> FormData:
        """
        Update the q3 matrix of this object.

        Args
        -----
        `matrix`:
            An q3 matrix.

        Returns
        --------
        FormData
            This object itself. It can use nested calls.
        """
        self._obj['matrices']['q3'] = matrix
        return self

    def parse(self) -> json:
        """
        Parse into json objects. It's a destructive action

        Returns
        -------
        json
            Parsed json objects
        """
        obj = deepcopy(self._obj)
        # conver unique id into str
        obj['id'] = str(obj.pop('_id'))
        obj = json.loads(json.dumps(obj))
        return obj

    def __repr__(self) -> str:
        """
        Get a representation of this object

        Returns
        --------
        str
            A formatted string
        """
        return pprint.pformat(self._obj, indent=1)

    def pretty(self) -> str:
        """
        Prettifies this object

        Returns
        --------
        str
            A formatted string
        """
        local_obj = deepcopy(self._obj)

        if "id" not in local_obj:
            obj_id = local_obj.pop('_id')
            local_obj['id'] = str(obj_id)
            local_obj = json.loads(json.dumps(local_obj))

        return pprint.pformat(local_obj, indent=1)

    def getEmail(self) -> str:
        """
        Get this email

        Returns
        --------
        str
            A email string.
        """
        return self._obj['email']

    def getName(self) -> str:
        """
        Get this name

        Returns
        --------
        str
            A name string.
        """
        return self._obj['name']

    def getDate(self) -> str:
        """
        Get this date

        Returns
        --------
        str
            A date string.
        """
        return self._obj['date']

    def getMatrices(self) -> Dict[str, Union[List[List[float]], float]]:
        """
        Get the dictionary equivalent to matrices.

        Returns
        --------
        Union[List[List[float]], float]]
            A dictionary mapping to matrices.
        """
        return self._obj['matrices']

    def getMatrixRoot(self) -> List[List[float]]:
        """
        Get the root matrix.

        Returns
        --------
        List[List[float]]
            The root matrix object.
        """
        return self._obj['matrices']['root']

    def getMatrixQ1(self) -> List[List[float]]:
        """
        Get the q1 matrix.

        Returns
        --------
        List[List[float]]
            The q1 matrix object.
        """
        return self._obj['matrices']['q1']

    def getMatrixQ1sec2(self) -> List[List[float]]:
        """
        Get the Q1sec2 matrix.

        Returns
        --------
        List[List[float]]
            The Q1sec2 matrix object.
        """
        return self._obj['matrices']['q12']

    def getMatrixQ1sec3(self) -> List[List[float]]:
        """
        Get the Q1sec3 matrix.

        Returns
        --------
        List[List[float]]
            The Q1sec3 matrix object.
        """
        return self._obj['matrices']['q13']

    def getMatrixQ1sec5(self) -> float:
        """
        Get the Q1sec5 matrix.

        Returns
        --------
        float
            The Q1sec5 matrix object.
        """
        return self._obj['matrices']['q15']

    def getMatrixQ2(self) -> List[List[float]]:
        """
        Get the Q2 matrix.

        Returns
        --------
        List[List[float]]
            The Q2 matrix object.
        """
        return self._obj['matrices']['q2']

    def getMatrixQ3(self) -> List[List[float]]:
        """
        Get the Q3 matrix.

        Returns
        --------
        List[List[float]]
            The Q3 matrix object.
        """
        return self._obj['matrices']['q3']

    def toDict(self) -> Dict[str, Union[str, Dict[str, Union[List[List[float]], float]]]]:
        """
        .. _FormData.toDict():

        Convert to a dictionary

        Returns
        --------
        List[List[float]]
            A dictionary equivalent to this object.
        """
        return self._obj

    def getDict(self) -> Dict[str, Union[str, Dict[str, Union[List[List[float]], float]]]]:
        """
        A alias to `FormData.toDict()`_ method.
        """
        return self.toDict()
