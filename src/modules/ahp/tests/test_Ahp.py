# -*- coding: utf-8 -*-

from typing import List
import unittest
from modules.ahp import Ahp


class TestAhpModule(unittest.TestCase):
    def test_calculate(self):
        import pandas as pd

        # https://www.youtube-nocookie.com/embed/J4T70o8gjlk?start=335
        # https://www.youtube-nocookie.com/embed/J4T70o8gjlk?start=569
        ahp_testing_data = pd.DataFrame(
            data={
                'Price or Cost': [1, 0.2, 0.25, 0.14],
                'Storage Space': [5, 1, 2, 0.33],
                'Camera': [4, 0.5, 1, 0.33],
                'Looks': [7, 3, 3, 1]},
            index=['Price or Cost', 'Storage Space', 'Camera', 'Looks'])

        # converting into a List[List[float]]
        ahp_testing_data_matrix: List[List[float]] = list(
            map(list, ahp_testing_data.to_numpy()))  # type: ignore

        ahp_test_ci: float
        ahp_test_pv: List[float]
        ahp_test_ci, ahp_test_pv = Ahp.calculate(ahp_testing_data_matrix)

        expected_pv = pd.DataFrame(
            index=['Price or Cost', 'Storage Space', 'Camera', 'Looks'],
            data={'Criteria weights': [0.6038, 0.1365, 0.1958, 0.0646]}
        )
        expected_ci = 0.037311
        expected_pv_list = expected_pv['Criteria weights'].to_list()

        for expected, result in zip(expected_pv_list, ahp_test_pv):
            self.assertAlmostEqual(expected, result, 2)
        self.assertAlmostEqual(expected_ci, ahp_test_ci, 2)

    def test_get_q15_value(self):
        self.assertEqual(1.0, Ahp.get_q15_value(9))
        self.assertEqual(0.1, Ahp.get_q15_value(1))
        self.assertEqual(0.0, Ahp.get_q15_value(1/9))
