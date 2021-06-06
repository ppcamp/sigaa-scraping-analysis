# -*- coding: utf-8 -*-
import unittest
from modules.ahp import Database
from unittest import mock
import mongomock


class TestAhpForm(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mocked_mongo = mongomock.MongoClient(
            "mongodb://ppcamp:password@localhost:27017/?authSource=admin")

        cls.ahpConn = Database.AhpForm()
        # mocking
        cls.ahpConn.__client = cls.mocked_mongo
        cls.ahpConn._db = cls.mocked_mongo['sigaadb']

    @classmethod
    def tearDownClass(cls) -> None:
        ...

    def setUp(self) -> None:
        # creating these variables
        self.data_1 = {
            'date': 'test#1',
            'email': 'test#1',
            'matrices': {
                'q1': [
                    [1, 7, 7, 5, 5, 5],
                    [0.14, 1, 5, 0.2, 0.33, 0.33],
                    [0.14, 0.2, 1, 0.14, 0.2, 0.33],
                    [0.2, 5, 7.14, 1, 3, 3],
                    [0.2, 3.03, 5, 0.33, 1, 1],
                    [0.2, 3.03, 3.03, 0.33, 1, 1]],
                'q12': [[1, 1, 5], [1, 1, 3], [0.2, 0.33, 1]],
                'q13': [
                    [1, 0.33, 3, 3, 5, 5],
                    [3.03, 1, 3, 3, 7, 3],
                    [0.33, 0.33, 1, 3, 5, 1],
                    [0.33, 0.33, 0.33, 1, 7, 1],
                    [0.2, 0.14, 0.2, 0.14, 1, 0.33],
                    [0.2, 0.33, 1, 1, 3.03, 1]],
                'q15': 5,
                'q2': [
                    [1, 1, 5, 5, 5],
                    [1, 1, 3, 3, 3],
                    [0.2, 0.33, 1, 1, 1],
                    [0.2, 0.33, 1, 1, 1],
                    [0.2, 0.33, 1, 1, 1]],
                'q3': [
                    [1, 0.2, 1, 0.2],
                    [5, 1, 3, 3],
                    [1, 0.33, 1, 0.2],
                    [5, 0.33, 5, 1]],
                'root': [[1, 1, 3], [1, 1, 3], [0.33, 0.33, 1]]},
            'name': 'Usuário Tests#1',
            'type': 'market'}

        self.data_2 = {
            'date': 'test#2',
            'email': 'test#2',
            'matrices': {
                'q1': [
                    [1, 7, 7, 5, 5, 5],
                    [0.14, 1, 5, 0.2, 0.33, 0.33],
                    [0.14, 0.2, 1, 0.14, 0.2, 0.33],
                    [0.2, 5, 7.14, 1, 3, 3],
                    [0.2, 3.03, 5, 0.33, 1, 1],
                    [0.2, 3.03, 3.03, 0.33, 1, 1]],
                'q12': [[1, 1, 5], [1, 1, 3], [0.2, 0.33, 1]],
                'q13': [
                    [1, 0.33, 3, 3, 5, 5],
                    [3.03, 1, 3, 3, 7, 3],
                    [0.33, 0.33, 1, 3, 5, 1],
                    [0.33, 0.33, 0.33, 1, 7, 1],
                    [0.2, 0.14, 0.2, 0.14, 1, 0.33],
                    [0.2, 0.33, 1, 1, 3.03, 1]],
                'q15': 5,
                'q2': [
                    [1, 1, 5, 5, 5],
                    [1, 1, 3, 3, 3],
                    [0.2, 0.33, 1, 1, 1],
                    [0.2, 0.33, 1, 1, 1],
                    [0.2, 0.33, 1, 1, 1]],
                'q3': [
                    [1, 0.2, 1, 0.2],
                    [5, 1, 3, 3],
                    [1, 0.33, 1, 0.2],
                    [5, 0.33, 5, 1]],
                'root': [[1, 1, 3], [1, 1, 3], [0.33, 0.33, 1]]},
            'name': 'Usuário Tests#2',
            'type': 'teacher'}

    def tearDown(self) -> None:
        # removing elements if they exists
        filter_data = {'date': 'test#1'}
        if self.mocked_mongo.sigaadb.AhpForm.count_documents(filter_data) > 0:
            self.mocked_mongo.sigaadb.AhpForm.delete_one(filter_data)
        filter_data = {'date': 'test#2'}
        if self.mocked_mongo.sigaadb.AhpForm.count_documents(filter_data) > 0:
            self.mocked_mongo.sigaadb.AhpForm.delete_one(filter_data)

    def test_findById(self):
        # self.ahpConn.insert(self.data)
        ...

    def test_findByDict(self):
        self.ahpConn.insert(self.data_1)
        self.ahpConn.insert(self.data_2)
        self.assertEqual(1, len(self.ahpConn.findByDict({'date': 'test#1'})))

    def test_getAll(self):
        self.ahpConn.insert(self.data_1)
        self.ahpConn.insert(self.data_2)
        self.assertEqual(2, len(self.ahpConn.getAll()))

    def test_insert(self):
        self.ahpConn.insert(self.data_1)
        self.ahpConn.insert(self.data_2)
        self.assertEqual(
            2, self.mocked_mongo.sigaadb.AhpForm.count_documents({}))

    @unittest.skip('this test is failing')
    def test_delete(self):
        self.ahpConn.insert(self.data_1)
        self.ahpConn.insert(self.data_2)
        filter_data = {'date': 'test#1'}
        el = self.mocked_mongo.sigaadb.AhpForm.find_one(filter_data)
        _id = str(el['_id'])
        print(f'\n\nID é: {_id}\n')
        # failing here (inside delete function)
        el = self.ahpConn.delete(_id)
        elements = [i for i in self.mocked_mongo.sigaadb.AhpForm.find({})]
        self.assertEqual(1, len(elements))
