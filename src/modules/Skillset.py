# -*- coding: utf-8 -*-

"""
This module contains all functions used to read the CSV files under a specified
directory. It's responsable to parse the data obtained in the `Google Sheets`

Todo
----
Implement loggers for

- read_csvs

Implement tests for:

- test_read_csvs
- merge_data
"""

# list files over a specified directory
from os import listdir
from os import path
# Dataframe
import pandas as pd
# typings marks
from typing import List
# logging
import logging
import unittest

# A object used only to specify the type
DataFrames = List[pd.DataFrame]


def read_csvs(sheetsDir: str) -> DataFrames:
    """
    Open a directory and read all csv files inside.
    This function clean some unusefull elements based on researches models.

    Args
    ----
    `sheetsDir`:
        Directory to search for csv files.

    Returns
    -------
    List[pandas.DataFrame]
        A list of pandas dataframes
    """
    full_path: str = path.realpath(sheetsDir)

    # Get form's infos
    infos = []

    def is_csv(element: str):
        return path.isfile(path.join(full_path, element)) and element[-4:] == '.csv'

    directory: List[str] = listdir(full_path)
    csvs = list(filter(is_csv, directory))

    for f in csvs:
        logging.debug(f"Reading file: {f}")
        tmpDF = pd.read_csv(f"{sheetsDir}/{f}").fillna(0)

        # Remove two last lines
        # tmpDF = tmpDF[:-2]

        # Renaming columns
        header: List[str] = tmpDF.columns.to_list()  # type: ignore
        header[0] = 'Periodo'
        header[1] = 'Sigla'
        header[2] = 'Nome da disciplina'
        header[-1] = 'Somatório'
        tmpDF.columns = header
        # Removing unecessary columns
        tmpDF.drop(['Periodo', 'Nome da disciplina',
                    'Somatório'], axis=1, inplace=True)
        # Turn initials into index
        tmpDF.set_index('Sigla', inplace=True)

        # Append this dataframe to info vec
        infos.append(tmpDF)

    # Return a list of dataframes
    return infos


def merge_data(dataframes: DataFrames) -> pd.DataFrame:
    """
    It performs the join of multiple dataframes objects into a single one,
    basing on a specified method. By default, it does a mean operation,
    ie.:

    .. math:: \\frac{\\sum_{i=0}^N \\text{dataframes}_i}{N}

    Args
    ----
    `dataframes`:
        A list of dataframes to be merged.

    Returns
    -------
    pandas.DataFrame
        A single dataframe based on values passed through. mean(dataframes)
    """
    # Juntando os arquivos num único dataframe
    out = pd.concat(dataframes)

    # Realizando a média
    out = out.groupby(out.index)  # type: ignore
    out = out.mean()

    return out


class TestSkillsetCSVS(unittest.TestCase):
    def test_read_csvs(self):
        ...

    def test_merge_data(self):
        ...


if __name__ == '__main__':
    unittest.main()
