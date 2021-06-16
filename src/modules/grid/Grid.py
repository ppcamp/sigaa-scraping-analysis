# -*- coding: utf-8 -*-

"""
This module contains the functions which check for existency and,
if didn't found, scrap it from sigaa's systems.

Todo
----
Implement `loggers` and `tests` for Grid
"""


from math import log
from .Scrapping import scrapping_grid as scrapping
# Import database connection
from .Database import Grids
# New type
from typing import Tuple
# Digraph model
from networkx import DiGraph
# logging
import logging
logger = logging.getLogger(__name__)
# Module responsable to get grid


def get_grid(grid: str, connection: str) -> Tuple[DiGraph, DiGraph]:
    """
    Get this grid.
    If the grid is not in database. Got it and then, store in database

    Args
    ----
    `grid`:
        The grid id. E.g, '0192015'
    `connection`:
        The connection string needed to access mongodb

    Returns
    -------
    Tuple[DiGraph, DiGraph]
        A `tuple` containing the pre and co requisite (networkx.DiGraph)
    """
    logger.info("Loading Database")
    # Store in mongodb those two graphs
    # Create a mongoclient
    Database = Grids(connection)

    GraphCo: DiGraph
    GraphPre: DiGraph

    # Check if grid exists
    if grid in Database:
        logger.info("Returning grid {} from database".format(grid))
        # Get grid from database
        GraphPre, GraphCo = Database[grid]
    else:
        # Otherwise, run scrapping in sigaa's system
        logger.info(
            "Grid {} wasn't found in database. Srapping it".format(grid))
        GraphPre, GraphCo = scrapping(grid)
        # Store it in database
        logger.debug("Storing grid {} in database".format(grid))
        # Database.set(grid, GraphPre, GraphCo)

    return GraphPre, GraphCo  # type: ignore
