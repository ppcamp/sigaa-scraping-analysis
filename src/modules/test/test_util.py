# -*- coding: utf-8 -*-

from typing import List
import unittest
import modules
import modules.util


class TestBasics(unittest.TestCase):
    def test_average_to_floats(self):
        v = [3.0, 56.0, 1.0, 41.0]
        test = round(sum(v)/len(v), 3)
        result = modules.util.average(v, roundp=3)
        self.assertEqual(test, result, "Values didn't match")

    def test_average_to_matrices(self):
        from copy import deepcopy

        a: List[List[float]] = [[1.0, 1.0, 1.0], [1.0, 1.0, 1.0]]
        b: List[List[float]] = deepcopy(a)

        result = modules.util.average([a, b])
        expected_result: List[List[float]] = deepcopy(a)

        # iterate and raise an error. P.S.: It won't throw any error
        for row in range(2):
            for col in range(2):
                self.assertEqual(
                    result[row][col],
                    expected_result[row][col],
                    f"result[{row}][{col}] = {result[row][col]}")

    def test_raise_MinimumLenghtError(self):
        ...

    def test_raise_TypeError(self):
        ...

    def test_get_competences_and_consistency(self):
        ...

    def test_calc_mean_matrix(self):
        ...

    def test_calc_ahp_for_new_mat(self):
        ...
