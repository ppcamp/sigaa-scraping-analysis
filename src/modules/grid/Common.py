"""
Test
"""

from networkx import DiGraph
import sys
from typing import Dict, List

from networkx.classes.digraph import DiGraph
from pandas.core.frame import DataFrame


# Variável que irá iterar sobre os períodos


def get_periodo() -> int:
    """
    Função que computa o período atual

    Returns:
        A value for every period
    """
    p = 0
    while p < 10:
        p += 1
        yield p

# --


def get_materias(nodes: DiGraph, periodo: int) -> List[str]:
    """
    Obtêm todas a lista de todas as siglas de matérias do período

    Args:
        periodo: número que indica o período atual entre [1,10]

    Returns:
        Uma lista contendo todas as siglas das matérias deste período
    """
    return [sigla for sigla, data in nodes.nodes(data=True) if data['period'] == str(periodo)]  # type:ignore


# --
def check_competencia(out: DataFrame, materias_atuais: List[str], competencia: str) -> bool:
    """
    Verifica se tem algum valor para esta competência neste periodo

    Parameters
    ----------
    materias_atuais: lista de materias no periodo atual
    competencia: competencia a ser analizada

    Returns
    -------
    True para caso não tenha uma disciplina no período atual que possua esta competência
    """
    return sum([out.loc[i][competencia] for i in materias_atuais]) == 0


def get_peso_competencia(out: DataFrame, materias_atuais: List[str], competencia: str, materia: str) -> float:
    """
    FIXME: Peso errado? Não, o peso das arestas é referente ao período do vértice de onde sai, se só tiver 1 matéria, irá ser peso 1 para qualquer aresta.

    Obtêm o peso da disciplina normalizado pelo peso de disciplinas no semestre, i.e., o máximo que uma competência pode ter no semestre é 1 ou 100%

    Parameters
    ----------
    materias_atuais: lista de materias no periodo atual
    competencia: competencia a ser analizada
    materia: materia que se deseja obter o peso da competencia para este periodo

    Returns
    -------
    Um float arredondado à duas casas decimais
    """
    total = sum([out.loc[i][competencia] for i in materias_atuais])

    # debug(f'get_peso_competencia({materia},  {materias_atuais}) -> Total {total}, Matéria {out.loc[materia][competencia]}\n')
    return round(out.loc[materia][competencia]/total, 2)  # type:ignore


def errprint(msg: str) -> None:
    """
    Exibe uma mensagem de error usando o stderr
    """
    sys.stderr.write('Error: ' + msg)


def get_nota(notas: Dict[str, float], materia: str, peso: float, acumulado: float) -> float:
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
    A recursive walk
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
