# -*- coding: utf-8 -*-

"""
Module that contains some common functions to handle with ahp data.
It performs the ahp calculations.

.. calculate ahp:
"""

from copy import deepcopy
from typing import List, Tuple


"""
Inconsistency index (Random Index, RI) mapping.
The index is equivalent to matrix cols (n) -1

JS_Index | cols |Random index  (calculated by Saaty)
---------|------|----------------------------------
   0     |   1  | there's only one question. Therefore, you can't apply AHP
   1     |   2  | there's only two questions. Therefore, you can't apply AHP, since that you just have two possible choices.
   2^    |  3^  | there's at least three questions. Therefore, you use the value
"""
# test
__RI: List[float] = [
    0,
    0,
    0.58,
    0.9,
    1.12,
    1.24,
    1.32,
    1.41,
    1.45,
    1.49,
    1.51,
    1.48,
    1.56,
    1.57,
    1.59
]


def calculate(obj: List[List[float]]) -> Tuple[float, List[float]]:
    """
    Calculates AHP and returns the *IC* and *priority_vector*.
    To an AHP be valid, it must have its IC bellow than 0.1.

    .. warning::

        This method not change the current value of object. So we can use it later if not pass through test.

    :Args:
        - `obj`: The matrix(NxN) that holds the ahp values
        - `matrix`: *OPTIONAL*. If pass some value, we'll gonna change the object passed.
            Usually is the same object as the first param

    :See:
        A reference to `AHP`_ .

    :Returns:
        It returns a tuple/vector, where the first element is the IC calculated over ahp,
        and the second one, is the proper index.

    :Example:
        .. code-block:: python
            :linenos:
            :name: this-py

            # import this module
            from modules.ahp import Ahp

            # some input matrix
            matrix = [
                [1, 1, 1],
                [1, 1, 1],
                [1, 1, 1],
            ]

            # calculate the index and its priority vector
            consistency_index, priority_vector = Ahp.calculate(matrix)

            # in this case, should not raise this
            assert consistency_index>=0.1, "Inconsistent ahp matrix"

    .. _AHP: https://www.youtube.com/watch?v=J4T70o8gjlk&ab_channel=ManojMathew
    """

    """
    The AHP work as follows:

    1) Developing a hierarchical structure with a goal at the top level, the attributes/criteria at
        the second level and the alternatives at the third level
    2) Determine the relative importance of different attributes or Criteria with respect to the goal
        Pairwise comparation matrix. Bellow follows the example of relative scaling:
                1           - Equal importance
                3           - Moderate importance
                5           - Strong importance
                7           - Very strong importance
                9           - Extreme importance
            2,4,5,8        - Intermediate values
        1/3, 1/5, 1/7, 1/9  - Are values for inverse comparison
    3) Calculate the consistency


    Therefore, to this form:
    1) The Main objective is get the discrepance bettween answers, the alternatives are the questions
    """

    # the length of my matrix
    length = len(obj)

    # If exist only 2 questions, ahp is not needed
    if (length <= 2):
        return 1, []

    # If we don't pass matrix object, we'll ...
    # ... copy the matrix, doing so, we don't change the current value of matrix stored in "obj"
    # if matrix is None:
    matrix = list(map(lambda row: deepcopy(row), obj))

    """
    This is the Pair-wise comparasion matrix

    :Description:
        Object that will be modified in ahp.
        At this point it will be the copy of `obj`, which is something like this:

    :Example:
    ________| Price | Storage | Camera | Looks
    Price   |   1   |    5    |   4    | 7
    Storage |  1/5  |    1    |   1/2  | 3
    Camera  |  1/4  |    2    |   1    | 3
    Looks   |  1/7  |   1/3   |  1/3   | 1
    """
    pair_wise_comp_matrix = list(map(lambda row: deepcopy(row), obj))

    # Normalize the pair-wise matrix
    for col in range(length):
        """
        Sum each column

        ________| Price | Storage | Camera | Looks
        Price   |   1   |    5    |   4    | 7
        Storage |  1/5  |    1    |   1/2  | 3
        Camera  |  1/4  |    2    |   1    | 3
        Looks   |  1/7  |   1/3   |  1/3   | 1
        --------|-------|---------|--------|--------
        Sum     |  1.59 |   8.33  |5.83    | 14
        """
        column_sum = 0
        for row in range(length):
            column_sum += matrix[row][col]

        """
        Normalize the copied table

        ________|     Price    |   Storage   |    Camera    | Looks
        Price   |   (1)/1.59   |  (5)/8.33   |   (4)/5.83   | (7)/14
        Storage |  (1/5)/1.59  |  (1)/8.33   |  (1/2)/5.83  | (3)/14
        Camera  |  (1/4)/1.59  |  (2)/8.33   |   (1)/5.83   | (3)/14
        Looks   |  (1/7)/1.59  | (1/3)/8.33  |  (1/3)/5.83  | (1)/14
        --------|--------------|-------------|--------------|--------
        Sum     |     1.59     |    8.33     |     5.83     |   14
        """
        for row in range(length):
            pair_wise_comp_matrix[row][col] /= column_sum

    """
    Priority vector (sum of row / row length). Also named as criteria weights
    ________|     Price    |   Storage   |    Camera    | Looks  | SUM(row)/cols -> criteria weights
    Price   |    0.6289    |   0.6002    |    0.6891    |  0.500 | (0.6289+0.6002+0.6891+0.500)/4
    Storage |  (1/5)/1.59  |  (1)/8.33   |  (1/2)/5.83  | (3)/14 |
    Camera  |  (1/4)/1.59  |  (2)/8.33   |   (1)/5.83   | (3)/14 |
    Looks   |  (1/7)/1.59  | (1/3)/8.33  |  (1/3)/5.83  | (1)/14 |
    --------|--------------|-------------|--------------|--------|
    Sum     |     1.59     |    8.33     |     5.83     |   14
    """
    priorityVec: List[float] = [0.0]*length
    for row in range(length):
        priorityVec[row] = sum(pair_wise_comp_matrix[row])/length

    """
    Apply the (priorityVec) into column values

    Criteria|
     weights|    0.6038    |      0.1365     |    0.1957      | 0.0646
    --------|--------------|-----------------|----------------|-----------
            |     Price    |     Storage     |     Camera     | Looks
    Price   |   1 * 0.6038 |    5 * 0.1365   |   4 * 0.1957   | 7 * 0.0646
    Storage |  1/5 * 0.6038|    1 * 0.1365   |   1/2 * 0.1957 | 3 * 0.0646
    Camera  |  1/4 * 0.6038|    2 * 0.1365   |   1 * 0.1957   | 3 * 0.0646
    Looks   |  1/7 * 0.6038|   1/3 * 0.1365  |  1/3 * 0.1957  | 1 * 0.0646
    """
    for col in range(length):
        for row in range(length):
            matrix[row][col] = round(priorityVec[col] * matrix[row][col], 2)

    """
    Weight vector

    Criteria|              |                 |                |           | Weigth
     weights|    0.6038    |      0.1365     |    0.1957      | 0.0646    | vector
    --------|--------------|-----------------|----------------|-----------|--------
            |     Price    |     Storage     |     Camera     | Looks     | SUM(row)
    Price   |   1 * 0.6038 |    5 * 0.1365   |   4 * 0.1957   | 7 * 0.0646| 0.6038 + 0.6825 + 0.7832 + 0.4522 = 2.517
    Storage |  1/5 * 0.6038|    1 * 0.1365   |   1/2 * 0.1957 | 3 * 0.0646|
    Camera  |  1/4 * 0.6038|    2 * 0.1365   |   1 * 0.1957   | 3 * 0.0646|
    Looks   |  1/7 * 0.6038|   1/3 * 0.1365  |  1/3 * 0.1957  | 1 * 0.0646|
    """
    weightVec: List[float] = [0.0]*length
    for row in range(length):
        weightVec[row] = sum(matrix[row])

    """
    Check consistency

    Criteria|              |                |            |           | Weigth  | Result
     weights|    0.6038    |      0.1365    |   0.1957   |  0.0646   | vector  |
    --------|--------------|----------------|------------|-----------|---------|-------------
            |     Price    |    Storage     |   Camera   |   Looks   | SUM(row)| weightVec/priorityVec
    Price   |    0.6038    |     0.6825     |   0.7832   |   0.4522  |  2.517  | 2.517/0.6038
    Storage |    0.1208    |    0.1365      |   0.0979   |   0.1938  |  0.5490 | 0.5490/0.1365
    Camera  |    0.1510    |    0.2730      |   0.1958   |   0.1938  |  0.8136 | 0.8136/0.1957
    Looks   |    0.0863    |    0.0455      |   0.0653   |   0.0646  |  0.2616 | 0.2616/0.0646
    --------|--------------|----------------|------------|-----------|---------|-------------
    ->  lambda_max =>  [ (2.517/0.6038) + (0.5490/0.1365) + (0.8136/0.1957) + (0.2616/0.0646) ] / 4
    ->  CI => [lambda_max - n]/n - 1, where n is the number of cols
    """
    # We must use a function because lambda doesn't suppor tuple anymore
    def divide(icurr):
        # unpack
        i, curr = icurr
        return curr/priorityVec[i]
    lambda_max = sum(
        list(map(divide, enumerate(weightVec)))) / length
    ci = (lambda_max - length) / (length-1)

    """
    Calculate the consistency ratio CR, which is given by the formula:
    CR = CI/RI, where RI is the random index calculated by Saaty
    """
    cr = ci / __RI[length-1]

    # to compare, it must be less than 0.1 by Saaty
    return cr, priorityVec
