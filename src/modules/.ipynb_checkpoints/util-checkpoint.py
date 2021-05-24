# -*- coding: utf-8 -*-

"""
A module containing some usefull functions that can be shared with another modules
"""

from __future__ import annotations
from typing import Any, Dict, List, Union
import logging as logger
import sys
import numpy as np

import pandas as pd
from modules.ahp import Ahp

from modules.ahp.Types import FormData, FormDataType


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


def competences_relations(data: List[FormData], tt: FormDataType):
    t: str = tt.value

    # dataframe de consistência para cada resposta
    _dfconsist = [
        'type',
        'root',
        'q1',
        'q12',
        'q13',
        'q2',
        'q3',
    ]
    mongo_competences_consistency: pd.DataFrame = pd.DataFrame(
        columns=_dfconsist)

    # cria um dataframe para armazenar a relação de respostas por competência
    mongo_competences: pd.DataFrame = pd.DataFrame(columns=[
        'type',

        # root
        "Conhecimento técnico",
        "Competências, habilidades e atributos pessoais e profissionais: gerenciar projetos, compreender problemas e autoaprendizado",
        "Competências e habilidades interpessoais: trabalho em equipe e comunicação",

        # q1
        "Matemática e física",
        "Conhecimento, métodos e ferramentas fundamentais de computação básica",
        "Conhecimento, métodos e ferramentas na área de sistemas de software",
        "Sistemas microprocessados",
        "Conhecimentos básicos em sistemas de comunicação",
        "Conhecimento em sistemas de automação ",

        # q12
        "Lógica, algoritmos, teoria da comp,  estruras de dados.",
        "Linguagens e paradigmas.",
        "PAA",

        # q13
        "Configurar plataformas para softwares e serviços.",
        "Arquiteturas de computadores",
        "Segurança de sis. de comp.",
        "Engenharia de software",
        "Inteligência artificial",
        "Desenvolvimento Web e Mobile",

        # q15
        "Redes de computadores",
        "Software para sistemas de comunicação",

        # q2
        "Gerenciar projetos e sistemas de computação",
        "Engenharia-econômica",
        "Compreender e resolver problemas",
        "Autoaprendizado",
        "Criatividade e Inovação",

        # q3
        "Comunicação oral e escrita",
        "Língua inglesa",
        "Empreender e exercer liderança",
        "Trabalho em equipe",
    ])

    for response in data:
        _secoes = {}
        _matrices = response.getMatrices()
        _cline = {k: None for k in _dfconsist}
        _cline['type'] = t  # type:ignore

        for k, v in _matrices.items():
            # verifica se é um escalar
            if k == "q15":
                priority_vec = Ahp.get_q15_value(v)  # type:ignore
                logger.debug(f"q15: {v} -> {priority_vec}")
            else:
                # caso seja uma matriz, calcula o ahp ...
                # ... NOTE que aceita AHP errados
                if v[0][0] != 0:
                    _cline[k], priority_vec = Ahp.calculate(v)  # type: ignore
                else:
                    _cline[k] = 0  # type: ignore
                    priority_vec = [0]*len(v)

            # adiciona as competências para cada matriz
            _secoes[k]: Union[float, List[float]
                              ] = priority_vec  # type: ignore

        mongo_competences_consistency = mongo_competences_consistency.append(
            _cline, ignore_index=True)
        # faz o mapping para essas competências
        _n: Dict[str, float] = Ahp.mapping_competences(_secoes)
        _n['type'] = t  # type:ignore
        # adiciona o dicionário de competências ao dataframe
        mongo_competences = mongo_competences.append(_n, ignore_index=True)

    return mongo_competences, mongo_competences_consistency


def calc_mean_matrices(data: List[FormData]):
    # dicionário de matrizes (que irão conter a média das matrizes )
    matrices: Dict[str, Union[List[List[float]], float]] = {}

    # obtém as possiveis keys do questionário (ids das matrizes)
    matrices_ids: List[str] = list(data[0].getMatrices().keys())

    # calcula a média ponderada das matrizes
    for matrix in matrices_ids:
        _mats = []
        # anda sobre uma determinada "matrix" sobre todas as respostas
        for response in data:
            # obtêm a matriz
            _m: List[List] = response.getMatrices()[matrix]

            # verifica se é uma matriz com base na chave (q15 é um escalar)
            if matrix != 'q15':
                # verifica se a matriz atual é um AHP válido ...
                # ... se for, adiciona essa matriz válida ...
                # ... dessa forma, futuramente, ela será incluída no cálculo da média
                if _m[0][0] != 0:
                    cr, _comp = Ahp.calculate(_m)
                else:
                    # ... IGNORA MATRIZES QUE NÃO HOUVERAM RESPOSTAS
                    cr = 1E9
                    _comp = [0]*len(_m)
                if cr <= 0.1:
                    _mats.append(_m)
            # caso contrário, se trata de um escalar e, portanto, deverá ...
            # ... ser encontrado o seu equivalente
            else:
                # ... IGNORA MATRIZES QUE NÃO HOUVERAM RESPOSTAS
                if _m != 0:
                    _mats.append(Ahp.get_q15_value(_m))  # type:ignore

        # calcula a média ponderada para cada matriz válida
        matrices[matrix] = average(*_mats)  # type:ignore

    return matrices


def calc_ahp_for_new_mat(matrices: Dict[str, Any]):
    secoes: Dict[str, List or float] = {}
    logger.debug('Calculating ahp for new matrices')

    for matrix in matrices:
        logger.debug(f'Calculating for matrix: {matrix}')
        logger.info(matrices[matrix])
        cr, priorityVec = 0, matrices[matrix]

        # se for uma matriz, calcula o ahp
        if matrix != 'q15':
            cr, priorityVec = Ahp.calculate(matrices[matrix])
            logger.debug(f'Cr calculated: {cr}')
            logger.debug(f'PriorityVec: {priorityVec}')
            # arredonda o vetor de saída (resultante) para 2 casas decimais
            priorityVec = list(np.round(priorityVec, 2))

        # adiciona este dado no vetor de competências do mercado
        secoes[matrix] = priorityVec
    logger.debug('\n\n')
    return secoes
