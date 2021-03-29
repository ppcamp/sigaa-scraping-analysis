# -*- coding: utf-8 -*-

"""
This module it's responsable to store/retrieve the graphs from mongodb.
"""

# Convert Graph to json
import json
from typing import Any, Tuple
from networkx.classes.digraph import DiGraph
from networkx.readwrite import json_graph
# MongoDB
from pymongo import MongoClient


class Grids(object):
    """
    This class is responsable to get/put grids into database.

    :Example:
        .. code-block:: python

            # importing this module
            from modules.grid.Database import Grids

            grids_module = Grids(mongo_connection_string)
            unexistent_courseCode = "coxinha"

            # throw this AssertionError
            assert unexistent_courseCode in grids_module, "It will throw this error"
    """

    def __init__(self, connectionString) -> None:
        """
        By default, it starts a mongodb client.
        """
        # Create a mongoclient
        self.client = MongoClient(connectionString)
        # Connect to database
        self.db = self.client.sigaadb

    # override
    def set(self, grid: str, GraphPreReq: DiGraph, GraphCoReq: DiGraph) -> None:
        """
        Convert graphs to json, then, to string. After that, store it
        into database.

        :Parameters:
            - `grid`: A grid string like. E.g: "0192015"
            - `GraphPreReq`: A `networkx.DiGraph`, where the edges are the pre requisite
            - `GraphCoReq`: A `networkx.DiGraph`, where the edges are the co requisite

        :Notes:
            Check it out the :mod:`.Grid` module.
        """
        pre = json_graph.node_link_data(GraphPreReq)
        co = json_graph.node_link_data(GraphCoReq)

        # To store the graph (Seariallized -- as string)
        # pre, co = dumps(pre), dumps(co)

        value = {"pre": pre, "co": co}
        try:
            self.db.Grids.insert_one({"grid": grid, "values": value})
        except Exception as e:
            print(f'Error: {e}')

    # override
    def get(self, grid: str) -> Tuple[DiGraph, DiGraph]:
        """
        Get object then convert it to graph again

        :Parameters:
            - `grid`: Equivalent grid number.

        :Returns:
            - `Tuple`: (pre, co) Pre and corequisites (digraphs)

        :Raises:
            *Exception* if couldn't fetch some object with this courseCode.
        """
        # Get object
        obj = self.db.Grids.find_one({"grid": grid})
        # Check if exists
        if obj == None:
            # print(f'This object don\'t exists.')
            raise Exception("Don't exists graphs associated to this grid.")

        # Extract those params
        pre = obj["values"]["pre"]
        co = obj["values"]["co"]

        # Otherwise, convert it into graph again
        # pre = loads(obj["values"]["pre"])
        # co = loads(obj["values"]["co"])

        # To get back the graph
        pre: DiGraph = json_graph.node_link_graph(pre)  # type: ignore
        co: DiGraph = json_graph.node_link_graph(co)  # type: ignore

        # Return it
        return pre, co

    def __contains__(self, item: str) -> bool:
        """
        Check if exists this item in dabatase

        :Parameters:
            - `item`: The course code to be checked. E.g: "0192015"

        :Returns:
            True if the item exists in database
        """
        # Get object
        obj = self.db.Grids.find_one({"grid": item})
        # Check if exists
        return obj != None

    def __getitem__(self, key: str) -> Tuple[DiGraph, DiGraph]:
        """
        Get the object with this key. This function is an alias to :meth:`get`

        :Parameters:
            - `key`: A courseCode string
        """
        return self.get(key)

    def close(self):
        """
        Close mongo's connections
        """
        self.client.close()
