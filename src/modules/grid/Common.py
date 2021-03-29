# -*- coding: utf-8 -*-

"""
This module contains some usefull functions to iterate over competency graph and sigaa's graphs.
"""

from networkx import DiGraph
import sys
from typing import Dict, List

from networkx.classes.digraph import DiGraph
from pandas.core.frame import DataFrame


def get_periodo() -> int:
    """
    Computes the current period

    :Yields:
        A value for every period
    """
    p = 0
    while p < 10:
        p += 1
        yield p


def get_materias(nodes: DiGraph, periodo: int) -> List[str]:
    """
    Get all class acronyms for a given `periodo`.

    :Parameters:
        - `nodes`: a DiGraph containing graphs and edges
        - `periodo`: current grade period. Bettween [1,10]. See :meth:`get_periodo`


    :Returns:
        A List containing all classes for a given `periodo`.
    """
    return [sigla for sigla, data in nodes.nodes(data=True) if data['period'] == str(periodo)]  # type:ignore


def check_competencia(out: DataFrame, materias_atuais: List[str], competencia: str) -> bool:
    """
    Check if exist some value (edge) to some `competencia` in a given list of period, `materias_atuais`.

    :Parameters:
        - `materias_atuais`: list of class acronyms for a some period. Check it out :meth:`get_periodo`
        - `competencia`: competency to be analysed. E.g: 'BAC01'

    :Returns:
        True if there's none class in this period with this competency.
    """
    return sum([out.loc[i][competencia] for i in materias_atuais]) == 0


def get_peso_competencia(out: DataFrame, materias_atuais: List[str], competencia: str, materia: str) -> float:
    """
    Get the class weight normalized by total amount of classes in a given semester.
    The maximum value that a given competency can have is 1 (100%).

    .. math:: \\frac{\\sum_{i=0}^N \\text{competency}_i}{N}

    :Note:
        *Peso errado?* Não, o peso das arestas é referente ao período do vértice de onde sai,
        se só tiver 1 matéria, irá ser peso 1 para qualquer aresta.

    :Parameters:
        - `materias_atuais`: list of classes in the current period. Check :meth:`get_materias`
        - `competencia`: competency to be analized.
        - `materia`: class acronym to get the edge weight.

    :Returns:
        A stipulated weight rounded by 2 decimal places.
    """
    total = sum([out.loc[i][competencia] for i in materias_atuais])

    # debug(f'get_peso_competencia({materia},  {materias_atuais}) -> Total {total}, Matéria {out.loc[materia][competencia]}\n')
    return round(out.loc[materia][competencia]/total, 2)  # type:ignore


def get_nota(notas: Dict[str, float], materia: str, peso: float, acumulado: float) -> float:
    """
    Calculate the class scores.

    .. math:: x =
        \\begin{cases}
            \\text{acumulado}\\cdot\\text{peso}, \\text{Se...?} \\\\
            \\left(\\frac{\\text{notas[materia]}}{10}+\\text{acumulado}\\right)\\cdot\\text{peso},\\text{Se...?} \\\\
        \\end{cases}


    TODO:
        - Update and understand better this documentation HERE

    """
    # Caso o aluno não tenha feito a matéria ainda, propaga o acumulado pelo peso
    if materia not in notas:
        return round(acumulado * peso, 3)
    # Caso já tenha feito a matéria, calcula pelo peso e retorna mais o acumulado
    return round((notas[materia]/10 + acumulado)*peso, 3)


# DFS
# A função poderá ser chamada recursivamente 1000x (default)
sys.setrecursionlimit(1000)


def dfs_walk(notas: Dict[str, float], grafo: DiGraph, materia: str, acumulado: float = 0.0) -> float:
    """
    A recursive walk over competency graph

    :Parameters:
        - `notas`:
            A dictionary mapping a class acronym to an value.
            Usually, this value will be the highest student's score to this class.
        - `grafo`: A graph equivalent to some competency.
        - `materia`: A name for a given node.
        - `acumulado`: The propagated value until some point

    :Returns:
        The propageted `acumulado` value over it's childrens/leafs.
    """
    total: float = 0

    # Anda sobre os filhos
    for filho in grafo.neighbors(materia):
        # Obtém o peso da aresta que manda para o filho
        peso = grafo[materia][filho]['weight']
        # Obtém a nota (acumulada) que será enviada para o filho
        novo_acumulado: float = get_nota(notas, materia, peso, acumulado)
        # Caminha para este filho
        total += dfs_walk(notas, grafo, filho, novo_acumulado)
    else:
        # Não possui filhos (última da grade com essa competência)
        total: float = get_nota(notas, materia, 1, acumulado)

    # Retorna o valor acumulado (dos filhos e até ela)
    return total
