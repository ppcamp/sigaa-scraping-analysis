# -*- coding: utf-8 -*-
from typing import Dict, List
import unittest
from modules.grid import Competence
from modules.grid.Competence import __get_period as get_period
from os import path
import pandas as pd
import networkx as nx


def read_scores_csv(data_folder: str) -> Dict[str, float]:
    """
    A testing function, only used in the TestCompetence.
    It should return the 'scores.csv' file parsed into dictionary

    Args
    ----
    `data_folder`:
      The path to data folder (where the samples will be placed)

    Returns
    -------
    Dict[str, float]
      A dictionary mapping a subject to a given value

    Important
    ---------
    function used only to parse data
    """
    scores: Dict[str, float] = {}

    with open(path.join(data_folder, 'scores.csv')) as f:
        lines: List[str] = f.readlines()
        header: str = lines.pop(0)
        for line in lines:
            key: str
            value: str
            key, value = line.split(';')
            scores[key] = float(value)
    return scores


class TestCompetence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data_folder: str = path.join(path.dirname(__file__), 'data')
        # read dataframe
        cls.dataframe = pd.read_csv(
            path.join(cls.data_folder, 'dataframe.csv'))

    def test_get_period(self):
        result: List[int] = [i for i in get_period()]
        expected: List[int] = [i for i in range(1, 11)]
        self.assertListEqual(expected, result)

    def test_get_period_classes(self):
        ...

    def test_competence_not_exist_in(self):
        ...

    def test_get_competence_weight(self):
        ...

    def test_BFS_generate_graphs(self):
        ...

    def test_BFS_get_weight(self):
        ...

    def test_BFS_walk(self):
        # read student's score
        self.scores: Dict[str, float] = read_scores_csv(self.data_folder)
        # testing for Web Dev Mobile
        HUMI01 = 7.0
        MATI01 = 7.2
        MATI02 = 7.3
        ECOI04 = 8.4
        ECOI09 = 7.3
        MATI04 = 6.8
        ECOI11 = 6.3
        ECOI14 = 8.7
        ECOI25 = 9.8
        # makes calculations
        period_1 = (1.0 * HUMI01/10)*0.2 + 0.4 * \
            ((1.0 * MATI01/10) + (1.0 * MATI02/10))
        period_2 = (period_1 * ECOI04/10) * (0.5+0.5)
        period_4 = (period_2 * ECOI09/10) * (0.3126+0.3126) + \
            (period_2 * MATI04/10)*(0.1874+0.1874)
        period_5 = (period_4 * ECOI11/10)*0.7499 + \
            (period_4 * ECOI14/10)*0.2501
        # however, when the period is equal to 0, the accumulated do not change, so
        period_9 = (period_5 * ECOI25/10)
        # at the end, round by 2
        expected = round(period_9 * 1.0, 2)
        # get the graph equivalent for this test
        graph: Dict[str, nx.DiGraph] = {
            'Desenvolvimento Web e Mobile':
            nx.read_gpickle(
                path.join(self.data_folder, 'web_graph.gpickle'))}
        # runs this test
        notas = Competence.BFS.walk(graph, self.scores, roundp=2)
        # TEST
        self.assertEqual(expected, notas['Desenvolvimento Web e Mobile'])
