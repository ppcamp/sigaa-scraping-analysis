# Grid Scrapping

# This script is responsable to open the sigaa system and then scrapy if don't find the course in sqlite database.


# Debugging library
from IPython.core.display import display, HTML

# Module responsable to get grid
from modules.Grid import get as Scrapping
from modules.Database import Grids


def get(grid):
    """
    Get this grid,
    """
    # Store in mongodb those two graphs
    # Create a mongoclient
    Database = Grids(
        'mongodb+srv://ppcamp:DRrPaRrHqmaWo43D@cluster0.tgt68.mongodb.net/')

    # Check if grid exists
    if grid in Database:
        # Get grid from database
        GraphPre, GraphCo = Database[grid]
    else:
        # Otherwise, run scrapping in sigaa's system
        print("[Debug] Searching in sigaa's system")
        GraphPre, GraphCo = Scrapping(grid)
        # Store it in database
        print("[Debug] Storing in database")
        Database.set(grid, GraphPre, GraphCo)

    return GraphPre, GraphCo


if __name__ == "__main__":
    # Get grid
    grid = '0192015'
    GraphPre, GraphCo = get(grid)

    print(GraphPre.edges())
