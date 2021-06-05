# -*- coding: utf-8 -*-
from typing import List
import unittest
from modules.grid import Competence
from modules.grid.Competence import __get_period as get_period

import pandas as pd


class TestCompetence(unittest.TestCase):
    def setUp(self) -> None:
        from os import path
        self.dataframe = pd.read_csv(
            path.join(path.dirname(__file__), 'mock', 'dataframe.csv'))

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
        ...
