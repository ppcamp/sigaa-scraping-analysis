# -*- coding: utf-8 -*-
import unittest
from modules.ahp import Types


class TestFormData(unittest.TestCase):
    def test_email(self):
        test = Types.FormData().setEmail("test@email.com")
        self.assertEqual("test@email.com", test.getEmail())

    def test_type(self):
        ...

    def test_date(self):
        ...

    def test_matrix_root(self):
        ...

    def test_matrix_q1(self):
        ...

    def test_matrix_q1sec2(self):
        ...

    def test_matrix_q1sec3(self):
        ...

    def test_matrix_q1sec5(self):
        ...

    def test_matrix_q2(self):
        ...

    def test_matrix_q3(self):
        ...

    def test_parse(self):
        ...

    def test_repr(self):
        ...

    def test_pretty(self):
        ...

    def test_toDict(self):
        ...
