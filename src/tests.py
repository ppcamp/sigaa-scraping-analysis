# -*- coding: utf-8 -*-

"""
Scipt used to test all files
"""
import unittest
import os
from unittest import runner

if __name__ == '__main__':
    start_path: str = os.path.realpath(os.path.dirname(__file__))
    start_path: str = os.path.join(start_path, 'modules')
    # Append this libraries if not in the path
    import os
    import sys

    current_path = os.path.realpath(__file__)
    module_path = os.path.join(current_path, '..', '..', '..')
    module_path = os.path.realpath(module_path)

    suite = unittest.TestLoader().discover(start_path)  # , pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=True)
    runner.run(suite)
