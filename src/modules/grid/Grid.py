# -*- coding: utf-8 -*-
from .Scrapping import _scrapping_grid as scrapping
# Import database connection
from .Database import Grids
# New type
from typing import Tuple
# Digraph model
from networkx import DiGraph


# Module responsable to get grid
def get_grid(grid: str, connection: str) -> Tuple[DiGraph, DiGraph]:
    """
    Get this grid. If the grid is not in database. Got it and then, store in database
    """
    # Store in mongodb those two graphs
    # Create a mongoclient
    Database = Grids(connection)

    # Check if grid exists
    if grid in Database:
        # Get grid from database
        GraphPre, GraphCo = Database[grid]
    else:
        # Otherwise, run scrapping in sigaa's system
        # print("[Debug] Searching in sigaa's system")
        GraphPre, GraphCo = scrapping(grid)
        # Store it in database
        print("[Debug] Storing in database")
        # Database.set(grid, GraphPre, GraphCo)

    return GraphPre, GraphCo
