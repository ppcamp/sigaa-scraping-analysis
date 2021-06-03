# -*- coding: utf-8 -*-

"""
Testing all files
"""
import unittest
import os
import sys
from unittest import runner

if __name__ == '__main__':
    start_path: str = os.path.realpath(os.path.join(
        os.path.dirname(__file__), '..', '..'))

    suite = unittest.TestLoader().discover(start_path, pattern="*.py")
    runner = unittest.TextTestRunner(verbosity=True)
    runner.run(suite)
