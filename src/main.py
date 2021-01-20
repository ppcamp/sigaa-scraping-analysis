# -*- coding: utf-8 -*-

from modules.Scrapping import get_grid
import networkx as nx
from modules.Plot import only_grid

if __name__ == "__main__":
    # Get grid
    grid = '0192015'
    GraphPre, GraphCo = get_grid(grid)

    # Print grid
    only_grid(GraphPre.nodes(), GraphPre.edges(), GraphCo.edges())
