# -*- coding: utf-8 -*-

# type: ignore

"""
Module that contains some common functions to handle with ahp data.
It performs the ahp calculations.

.. calculate ahp:
"""

from copy import deepcopy
from typing import Dict, Final, List, Tuple, Union, no_type_check
import typing


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


def calculate(obj: List[List[float]], roundp: int = 4) -> Tuple[float, List[float]]:
    """
    Calculates AHP and returns the *IC* and *priority_vector*.
    To an AHP be valid, it must have its IC bellow than 0.1.

    .. tip::

        This method not change the current value of object. So we can use it later if not pass through test.

    :Args:
        - `obj`: The matrix(NxN) that holds the ahp values
        - `matrix`: *OPTIONAL*. If pass some value, we'll gonna change the object passed.
            Usually is the same object as the first param

    :Kwargs:
        - `roundp`: The number of decimal places used to round.

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
    Price   |    0.6289    |   0.6002    |    0.6891    |  0.500 | (
        0.6289+0.6002+0.6891+0.500)/4
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
            matrix[row][col] = round(
                priorityVec[col] * matrix[row][col], roundp)

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


def _mapping_competences(secoes: Dict[str, Union[List[float], float]]) -> Dict[str, float]:
    """
    Mapping the AHP priority vector to questions

    :Args:
        - `secoes`: A dictionary containing a list (or scalar), to every matrix. A matrix is defined as *root*, *q1*, *q12*, *q13*, *q15*, *q2*, *q3*

    :Returns:
        - It returns a dictionary mapping competences to an specific scalar.
    """
    # montando o vetor para situado na mesma posição (root ignorado)
    return {

        "Conhecimento técnico": secoes['root'][0],
        "Competências, habilidades e atributos pessoais e profissionais: gerenciar projetos, compreender problemas e autoaprendizado": secoes['root'][1],
        "Competências e habilidades interpessoais: trabalho em equipe e comunicação": secoes['root'][2],

        "Conhecimento, métodos e ferramentas fundamentais de computação básica": secoes['q1'][1],
        "Conhecimento, métodos e ferramentas na área de sistemas de software": secoes['q1'][2],
        "Conhecimentos básicos em sistemas de comunicação": secoes['q1'][4],

        "Desenvolvimento Web e Mobile": secoes['q13'][5],


        "Matemática e física": secoes['q1'][0],
        "Lógica, algoritmos, teoria da comp,  estruras de dados.": secoes['q12'][0],
        "Linguagens e paradigmas.": secoes['q12'][1],
        "PAA": secoes['q12'][2],
        "Configurar plataformas para softwares e serviços.": secoes['q13'][0],
        "Arquiteturas de computadores": secoes['q13'][1],
        "Segurança de sis. de comp.": secoes['q13'][2],
        "Engenharia de software": secoes['q13'][3],
        "Inteligência artificial": secoes['q13'][4],
        "Sistemas microprocessados": secoes['q1'][3],

        "Redes de computadores": secoes['q15'],
        # 1/secoes['q15'],
        "Software para sistemas de comunicação": 1 - secoes['q15'],

        "Conhecimento em sistemas de automação ": secoes['q1'][5],
        "Gerenciar projetos e sistemas de computação": secoes['q2'][0],
        "Engenharia-econômica": secoes['q2'][1],
        "Compreender e resolver problemas": secoes['q2'][2],
        "Autoaprendizado": secoes['q2'][3],
        "Criatividade e Inovação": secoes['q2'][4],
        "Comunicação oral e escrita": secoes['q3'][0],
        "Língua inglesa": secoes['q3'][1],
        "Empreender e exercer liderança": secoes['q3'][2],
        "Trabalho em equipe": secoes['q3'][3],
    }


def get_q15_value(v: float, roundp: int = 3) -> float:
    """
    Get the equivalent value `v`, in percentual terms. (Normalized value)

    :Args:
        - `v`: The number to be normalized

    :Kwargs:
        - `roundp`: The number of decimal places to be rounded

    :Returns:
        The equivalent number converted into a value in [0..~1]

    .. caution::

        This number should be in:

        .. centered:: v = [1/9, 1/7, 1/5, 1/3, 1, 3, 5, 7, 9]


    It does the following operation:

    .. math::

        x(n) = \\frac{V(n) - 1/9}{9-1/9} \\\\
        \\therefore \\begin{cases} x(1/9) \\approx 0 \\\\ x(9) \\approx 1 \\end{cases}
    """
    return round((v-1/9) / (9-1/9), roundp)


class Mapping:
    """
    A class object used to encapsulate all the mapping methods.
    Usually used with values obtained of :meth:`.calculate`
    or :meth:`modules.grid.walk_through_graph`
    """

    MATRICES_IDENTIFIERS: Final[List[str]] = [
        'root', 'q1', 'q12', 'q13', 'q2', 'q3']

    # The section root there's no binding equivalent for student's
    COMPETENCES_MATRIX_ROOT: Final[List[str]] = [
        "Conhecimento técnico",
        "Competências, habilidades e atributos pessoais e profissionais: gerenciar projetos, compreender problemas e autoaprendizado",
        "Competências e habilidades interpessoais: trabalho em equipe e comunicação",
    ]

    # In sheets, there's no such fields
    COMPETENCES_MATRIX_Q1: Final[List[str]] = [
        "Matemática e física",
        # "Conhecimento, métodos e ferramentas fundamentais de computação básica",
        # "Conhecimento, métodos e ferramentas na área de sistemas de software",
        "Sistemas microprocessados",
        # "Conhecimentos básicos em sistemas de comunicação",
        "Conhecimento em sistemas de automação ",
    ]

    # In sigaa's form there is these fields
    COMPETENCES_MATRIX_FORM_Q1: Final[List[str]] = [
        "Matemática e física",
        "Conhecimento, métodos e ferramentas fundamentais de computação básica",
        "Conhecimento, métodos e ferramentas na área de sistemas de software",
        "Sistemas microprocessados",
        "Conhecimentos básicos em sistemas de comunicação",
        "Conhecimento em sistemas de automação ",
    ]

    COMPETENCES_MATRIX_Q12: Final[List[str]] = [
        "Lógica, algoritmos, teoria da comp,  estruras de dados.",
        "Linguagens e paradigmas.",
        "PAA",
    ]

    COMPETENCES_MATRIX_Q13: Final[List[str]] = [
        "Configurar plataformas para softwares e serviços.",
        "Arquiteturas de computadores",
        "Segurança de sis. de comp.",
        "Engenharia de software",
        "Inteligência artificial",
        "Desenvolvimento Web e Mobile",
    ]

    COMPETENCES_MATRIX_Q15: Final[List[str]] = [
        "Redes de computadores",
        "Software para sistemas de comunicação",
    ]

    COMPETENCES_MATRIX_Q2: Final[List[str]] = [
        "Gerenciar projetos e sistemas de computação",
        "Engenharia-econômica",
        "Compreender e resolver problemas",
        "Autoaprendizado",
        "Criatividade e Inovação",
    ]

    COMPETENCES_MATRIX_Q3: Final[List[str]] = [
        "Comunicação oral e escrita",
        "Língua inglesa",
        "Empreender e exercer liderança",
        "Trabalho em equipe",
    ]

    @staticmethod
    def to_sections(competences: Dict[str, float]) -> Dict[str, Union[List[float], float]]:
        """
        Mapping the output of graphs  - calculated in function :meth:`modules.grid.Competence.walk_through_graph` - into a mapping
        of matrix to list of float (ordered)

        :Args:
            - `competences`: A dictionary containing competences and it's results

        :Returns:
            A dictionary mapping this competences to it's equivalent matrix.

        .. note::

            Map the student's propagated value of its competence into sections equivalent. This step is important
            because it's used to normalize the competences values into this sections.

        :Example:
            .. code-block:: python
                :linenos:

                competences = {
                    "Conhecimento técnico": 0.8,
                    "Competências, habilidades e atributos ...": 0.9,
                    "Competências e habilidades interpessoais ...": 0.3,
                }

                Mapping.to_sections(competences)

                # Will be
                {
                    "q1": [0.8, 0.9, 0.3]
                }
        """
        keys: List[str] = list(competences.keys())

        # mapping root
        # NOTE: root can't be tracked due to its functionality
        # root: List[str] = []
        # for competence in Mapping.COMPETENCES_MATRIX_ROOT:
        #     if competence not in keys:
        #         raise Exception(f"Element {competence} not in competences")
        #     else:
        #         root.append(competences[competence])

        q1: List[str] = []
        for competence in Mapping.COMPETENCES_MATRIX_Q1:
            if competence not in keys:
                raise Exception(f"Element {competence} not in competences")
            else:
                q1.append(competences[competence])

        q12: List[str] = []
        for competence in Mapping.COMPETENCES_MATRIX_Q12:
            if competence not in keys:
                raise Exception(f"Element {competence} not in competences")
            else:
                q12.append(competences[competence])

        q13: List[str] = []
        for competence in Mapping.COMPETENCES_MATRIX_Q13:
            if competence not in keys:
                raise Exception(f"Element {competence} not in competences")
            else:
                q13.append(competences[competence])

        q15: List[str] = []
        for competence in Mapping.COMPETENCES_MATRIX_Q15:
            if competence not in keys:
                raise Exception(f"Element {competence} not in competences")
            else:
                q15.append(competences[competence])

        q2: List[str] = []
        for competence in Mapping.COMPETENCES_MATRIX_Q2:
            if competence not in keys:
                raise Exception(f"Element {competence} not in competences")
            else:
                q2.append(competences[competence])

        q3: List[str] = []
        for competence in Mapping.COMPETENCES_MATRIX_Q3:
            if competence not in keys:
                raise Exception(f"Element {competence} not in competences")
            else:
                q3.append(competences[competence])

        return dict(zip(
            ['q1', 'q12', 'q13', 'q15', 'q2', 'q3'],
            [q1, q12, q13, q15, q2, q3]))

    @staticmethod
    def to_matrices(competences: Dict[str, float]) -> Dict[str, Union[List[float], float]]:
        """
        It's just a bidding to :meth:`.to_sections`
        """
        return Mapping.to_sections(competences)

    @staticmethod
    def remove_unused_keys(data: List[float]) -> List[float]:
        """
        This method, remove the elements in intersection between
        COMPETENCES_MATRIX_FORM_Q1 - COMPETENCES_MATRIX_Q1
        """
        return [data[0], data[3], data[5]]

    @staticmethod
    def to_competences(matrices: Dict[str, Union[List[float], float]]) -> Dict[str, float]:
        """
        Does a mapping with AHP priority vector.

        :Args:
            - `matrices`: A dictionary containing a list (or scalar), to every matrix. \
                          A matrix is defined as *root*, *q1*, *q12*, *q13*, *q15*, *q2*, *q3*

        :Returns:
            It returns a dictionary mapping competences to an specific scalar.

        .. tip::

            Usually used with values of *priority vector*, obtained in function :meth:`calculate`
        """
        competences: Dict[str, float] = {}

        # check if all matrices exists
        for matrix in ['q1', 'q12', 'q13', 'q2', 'q3']:
            if matrix not in matrices.keys():
                raise Exception(
                    f'Matrix {matrix} doesn\' not exist in matrices dict')

        if 'root' in matrices:
            if len(matrices['root']) != 3:
                raise Exception('Length of root matrix aren\'t corrent')
            for index, competence in enumerate(Mapping.COMPETENCES_MATRIX_ROOT):
                competences[competence] = matrices['root'][index]

        # NOTE: that you can pass COMPETENCES_MATRIX_FORM_Q1, however
        # it will be mapped to COMPETENCES_MATRIX_Q1
        if len(matrices['q1']) == 6:
            matrices['q1'] = Mapping.remove_unused_keys(matrices['q1'])

        if len(matrices['q1']) != 3:
            raise Exception('Length of q1 matrix aren\'t corrent')
        for index, competence in enumerate(Mapping.COMPETENCES_MATRIX_Q1):
            competences[competence] = matrices['q1'][index]

        if len(matrices['q12']) != 3:
            raise Exception('Length of q12 matrix aren\'t corrent')
        for index, competence in enumerate(Mapping.COMPETENCES_MATRIX_Q12):
            competences[competence] = matrices['q12'][index]

        if len(matrices['q13']) != 6:
            raise Exception('Length of q13 matrix aren\'t corrent')
        for index, competence in enumerate(Mapping.COMPETENCES_MATRIX_Q13):
            competences[competence] = matrices['q13'][index]

        if type(matrices['q15']) == float:
            competences[Mapping.COMPETENCES_MATRIX_Q15[0]] = matrices['q15']
            competences[Mapping.COMPETENCES_MATRIX_Q15[1]] = 1 - \
                matrices['q15']
        elif type(matrices['q15']) == list:
            for index, competence in enumerate(Mapping.COMPETENCES_MATRIX_Q15):
                competences[competence] = matrices['q15'][index]

        if len(matrices['q2']) != 5:
            raise Exception('Length of q2 matrix aren\'t corrent')
        for index, competence in enumerate(Mapping.COMPETENCES_MATRIX_Q2):
            competences[competence] = matrices['q2'][index]

        if len(matrices['q3']) != 4:
            raise Exception('Length of q3 matrix aren\'t corrent')
        for index, competence in enumerate(Mapping.COMPETENCES_MATRIX_Q3):
            competences[competence] = matrices['q3'][index]

        return competences
