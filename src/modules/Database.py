# -*- coding: utf-8 -*-
# Convert Graph to json
from networkx.readwrite import json_graph
# Convert json to string
from json import dumps, loads
# MongoDB
from pymongo import MongoClient
# Mongo object
from bson.objectid import ObjectId


class Grids(object):
    """
    This class is responsable to get grid infos
    """

    def __init__(self, connectionString):
        """
        Starts a mongodb client
        """
        # Create a mongoclient
        self.client = MongoClient(connectionString)
        # Connect to database
        self.db = self.client.sigaadb

    # override
    def set(self, grid, GraphPreReq, GraphCoReq):
        """
        Convert graphs to json, then, to string. After that, store it
        in database.
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
    def get(self, grid):
        """
        Get object then convert it to graph again

        Parameters
        ----------
        grid: (str) Equivalent grid number.

        Returns
        -------
        Tuple: (pre, co) Pre and corequisites (json file)

        Note
        ----
        If object don't exists, return (None,None)
        """
        # Get object
        obj = self.db.Grids.find_one({"grid": grid})
        # Check if exists
        if obj == None:
            # print(f'This object don\'t exists.')
            return None, None

        # Extract those params
        pre = obj["values"]["pre"]
        co = obj["values"]["co"]

        # Otherwise, convert it into graph again
        # pre = loads(obj["values"]["pre"])
        # co = loads(obj["values"]["co"])

        # To get back the graph
        pre = json_graph.node_link_graph(pre)
        co = json_graph.node_link_graph(co)
        # Return it
        return pre, co

    def __contains__(self, item):
        """
        Check if exists this item in dabatase
        """
        # Get object
        obj = self.db.Grids.find_one({"grid": item})
        # Check if exists
        return obj != None

    def __getitem__(self, key):
        """
        Get the object with this key
        """
        return self.get(key)

    def close(self):
        """
        Close mongo's connections
        """
        self.client.close()
