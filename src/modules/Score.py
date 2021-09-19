# -*- coding: utf-8 -*-

"""
This module contains methods to:

- Read a given student history (pdf), and parse it into a dataframe. :meth:`parse_pdf`
- Save the dataframe into a json. :meth:`save_analysis`
- Load the json equivalent to a dataframe object. :meth:`read_json`

Todo
----
Implement tests for:

- test_read_json
- test_save_analysis
- Testtest_parse_pdf

Implement loggers for:

- parse_pdf
"""

from os import path
from typing import List, Union
# Tabula also needs the java installed
import tabula
# Pandas dataframe type
from pandas import DataFrame
# Parse json to string
import json
# numpy object
import numpy as np
import random


def read_json(filepath: str) -> json:
    """
    Read a json file equivalent to student's grid.

    Args
    ----
    `filepath`:
        path where to load the json file

    Returns
    -------
    json
        The equivalent json representation

    Note
    ----
    It's just a shortcut to read the file

    Example
    -------
    >>> from modules.score import read_json
    >>> import os
    >>> p = os.path.realpath("../file.json")
    >>> read_json(p)
    """
    out = None
    with open(filepath) as f:
        out = json.loads(f.read())
    return out


def save_analysis(out: DataFrame, filename: str, dirname: str) -> None:
    """
    Save the score loaded into a json object.
    Usually, this methods depends of :meth:`parse_pdf`.

    Args
    ----
    `out`:
        the data to store
    `filename`:
        the name of generated file
    `dirname`:
        place to put the output file
    """
    with open(path.join('..', dirname, filename + '.json'), 'w') as outfile:
        outfile.write(json.dumps(out))


def parse_pdf(studentId: str, inputDir: str, outDir: str = None) -> DataFrame:
    """
    Read a student score and parse it to a json file

    Args
    ----
    `studentId`:
        The student unique id
    `inputDir`:
        Directory where are placed the input files. (Based on current file)

    Keyword Args
    ------------
    `outDir`:
        Directory to save the json objects. (Based on project dir)

    Returns
    -------
    DataFrame
        Returns a dataframe containing the parsed value
    """

    # Read pdf file
    df: List[DataFrame] = tabula.read_pdf(  # type: ignore
        path.join(inputDir, f'historico_{studentId}.pdf'),
        pages='all')

    # Internal function
    def get_before(dataframe: DataFrame, currentline: int, columname: str) -> str:
        """
        Search for lines above to get an non NaN value
        (Only work for string)

        Args
        ----
        `dataframe`:
            Pandas dataframe containing
        `currentline`:
            The number that represetns the current line to search before
        `columnname`:
            Column's name to search for

        Returns
        -------
        str
            A string containing the usable value
        """
        i, value = currentline, ''
        while True:
            if i < 0:
                raise Exception(f'Ultrapassou o limite. Verifique o código.')
            value = dataframe.loc[i, columname]  # type: ignore

            if type(value) is str:
                return value
            else:
                i -= 1

    # Internal function
    def fix_scores(dflist: List[DataFrame]) -> DataFrame:
        """
        Merge the multiples dataframes into a only one

        Args
        ----
        `dflist`:
            A list of dataframes to search for

        Returns
        -------
        DataFrame
            A unique merged dataframe
        """
        scores = {}

        # ==
        def change_number(number: str) -> str:
            """
            Change "," to "." character

            Args
            ----
            `number`:
                A value to convert the float format

            Returns
            -------
            str
                A new string that represents this value in '.' format
            """
            return number.replace(',', '.')

        # ==
        def change_key(val) -> Union[str, float]:
            """
            Check if type is string, if so, convert it and return (or just return)

            Args
            ----
            `val`:
                a object that will be checked for its properties

            Returns
            -------
            Union[str, float]
                A new string or a float equivalent
            """
            if (type(val) is str) and ('--' not in val):
                return float(change_number(val))  # type:ignore
            else:
                return '--'

        # Itera sobre cada um dos dataframes de saída -> len == 7
        for table in dflist:
            # Pula se não for uma tabela de matérias concluídas/cursando
            if 'Ano/Período' not in table.columns.to_list():  # type: ignore
                continue

            # Renaming columns
            cols = table.columns.to_list()  # type: ignore
            fstRow = table.iloc[0]
            for i in range(len(cols)):
                if type(fstRow[i]) is str:
                    cols[i] = fstRow[i]
            table.columns = cols

            # print(f'Table names: {table.columns.to_list()}')

            # Itera sobre as matérias cursadas
            for turma in range(0, table.shape[0]):

                # Fix the case when there's another column
                if 'Unnamed: 1' in table.columns:
                    sigla = table.loc[turma, 'Unnamed: 1']  # type: ignore
                else:
                    sigla = table.iloc[turma, 1]

                # Pula se o valor da coluna não for a sigla da matéria
                if type(sigla) is not str or len(sigla) < 3:
                    continue
                # Resolve o problema caso não apareça os elementos corretos
                periodo = get_before(table, turma, 'Ano/Período')
                freq = change_key(table.loc[turma, 'Freq %'])  # type: ignore
                nota = change_key(table.loc[turma, 'Média'])  # type: ignore
                sit = table.loc[turma, 'Situação']  # type: ignore
                if type(sit) is not str:
                    sit = '--'

                # Caso contrário, adiciona no scores
                if periodo not in scores:
                    scores[periodo] = {}
                scores[periodo][sigla] = {
                    'scores': nota,
                    'situation': sit,
                    'freq': freq
                }

        # Return the output dict
        return scores  # type: ignore

    # Run the file scrapping
    out = fix_scores(df)

    # Save to file
    if outDir is not None:
        save_analysis(out, studentId, outDir)

    # Return the json object
    return out



def gen_score(
  rounded: int = 2,
  start: float = 7.0,
  end: float = 10.0) -> float:
  """
  Generates a random float number between `start` and `end` rounded by `rounded`

  Kwargs
  ----
  `rounded`:
    The number of decimal places
  `start`:
    The first number that can be generated
  `end`:
    The last number that can be generated
  """
  return round(random.uniform(start,end),rounded)


"""DISCIPLINES is the list of classes splitted by its focused content"""
DISCIPLINES = {
  "HARDWARE": np.array([
    "EELI02",
    "EELI03",
    "ECOI12",
    "EELI07",
    "ECAI26",
    "EELI10",
    "EELI11",
    "ECOI10",
    "EELI12",
    "EELI13",
    "EELI14",
    "EELI15",
    "ECAI04",
    "ECOI21",
    "ECAI11",
    "ECAI44",
    "ECOI18",
    "ECOI33",
    "ECAI05",
    "ECAI07",
    "ECOI33",
    "ECAI13",
    "ECOI07",
    "ECOI32",
    "ECOI19",
  ]),
  "SOFTWARE": np.array([
    "ECOI02",
    "ECOI03",
    "ECOI04",
    "ECOI08",
    "ECOI14",
    "ECOI30",
    "ECOI15",
    "ECOI16",
    "ECOI11",
    "ECOI13",
    "ECOI22",
    "ECOI25",
    "ECOI09",
    "ECOI23",
    "ECOI24",
    "ECOI26",
  ]),
  "UNCLASSIFIED": np.array([
    'EAMI30',
    'ECAI29',
    'ECO038',
    'ECOI01',
    'ECOI20',
    'ECOI61',
    'EMBI02',
    'EMEI02',
    'EMEI06',
    'EMEI07',
    'EMEI08',
    'EMTI02',
    'EMTI03',
    'EPRI02',
    'EPRI04',
    'EPRI30',
    'FISI01',
    'FISI02',
    'FISI03',
    'FISI04',
    'FISI04',
    'FISI05',
    'FISI06',
    'FISI07',
    'HUMI01',
    'HUMI02',
    'HUMI04',
    'HUMI06',
    'MATI01',
    'MATI02',
    'MATI03',
    'MATI03',
    'MATI04',
    'MATI05',
    'MATI06',
    'MATI07',
    'MATI08'])
}