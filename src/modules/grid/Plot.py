# -*- coding: utf-8 -*-
# fluxogram
from typing import Dict, List, Tuple
from graphviz import Digraph
from os import sep as OSsep
import networkx as nx

# Random over list
# from secrets import choice

# Rand some hexa char
from os import urandom, system as RUN
from binascii import b2a_hex as randHex
from os import path, getcwd, unlink

from networkx.classes.reportviews import NodeView, OutEdgeView


class Colors(object):
    """
    A enum like to map a color palette in hexa.
    """
    node = "#BDC3C7"

    BlueBased = {
        "baby": "#BDC3C7"
    }
    """
    A color palletet based on blue
    """

    RedBased = {
        "wine": "#BD1C32",
        "lightenRed": "#FA3246",
        "darkPink": "#BD1C44",
        "darkRed": "#AF0019",
        "darkenRed": "#850014",
        "darkerRed": "#BB0019",
    }
    """
    A color pallette based on red
    """

    GreenBased = {
        "nature": "#4c8768"
    }
    """
    A color pallette based on green
    """

    @staticmethod
    def rand() -> str:
        """
        A static method to generate some random color.

        :Returns:
            A formatted hex color, e.g: "#3f0a9b"
        """
        return "#" + randHex(urandom(3)).decode("utf-8")


def weighted_graph(
    nodes: NodeView,
    edges: List[Tuple[str, str, Dict[str, float]]],
    filename: str = 'grid',
    outputDir: str = "out"
) -> None:
    """
    .. _graphviz: https://graphviz.org/

    Get a student view of grid fluxogram/graph.
    This function make a system call to `graphviz`_.

    :Args:
        - `nodes`: A list containing the nodes.
        - `edges`: A list containing the edges for this graph.

    :Kwargs:
        - `filename`: The name of the file to save (image name). DEFAULT: grid
        - `outputDir`: The directory to save. DEFAULT: out

    .. note::

        - The nodes must ne ordered by period of the class.
        - Usually, you can get an example graph in :meth:`modules.grid.Grid.get_grid`
    """

    # Construct a tree with xml grid
    nameFile = f"{filename}.dot"

    # Setting up digraph plot
    output = Digraph(
        engine='dot',  # 'neato',  # force position
        name=nameFile,
        filename=nameFile,
        directory=outputDir,
        format='svg',
        graph_attr={
            # 'concentrate': 'true',
            'rankdir': 'BT',
            'overlap': 'scale',  # force position
            # splines → polyline, ortho, true/spline, curved
            'splines': 'ortho',  # edge uppon vertix
            # 'margin': '0.5,0.5',
            'sep': '0.5',
        },
        node_attr={
            'pad': '1',
            'nodesep': '2',
            'ranksep': '2'
        }
    )

    # Set a variable that will be responsable to increment x or y variables
    oldPeriod = 1
    incX = incY = 0
    # Insert nodes
    for initials in nodes:
        # Get node
        node = nodes[initials]

        # Get period
        period = node['period']
        if period == 'Optativa':
            continue

        # Check if changed the period.
        if oldPeriod != period:
            incY = 0
            # Increment x padding
            incX += 1
            oldPeriod = period

        # default color
        nodeColor = Colors.node
        # Set node position
        strPos = '{0:.3}'.format(str(incX)) + ',' + "-{}!".format(incY)

        output.node(
            initials,
            initials,
            color='none',
            style='filled',  # 'striped',
            shape='rectangle',
            fillcolor=nodeColor,
            pos=strPos,
            **{  # Node atributes fixed size
                 'fixedsize': 'true',
                'width': '2',
                'height': '1'
            }
            # len='0.5'
            # weight='.5',
        )
        # Increment y padding
        incY += 1

    # In edges you can add other parameters like
    # > edge.attr['label'] = '5'
    # > edge.attr['weight'] = 5

    # Creating the edges for pre requisite graph
    for (u, v, data) in edges:
        weight = data['weight']
        output.edge(
            u,
            v,
            color=Colors.RedBased['wine'],
            label=str(weight)
        )

    # ! Due to an windows problem with the binaries you must to save and then, run
    # output.render(view=True, filename="output.svg", renderer='neato')
    output.save(directory=outputDir)
    input = path.join(path.abspath(getcwd()), outputDir, f"{filename}.dot")
    output = path.join(path.abspath(getcwd()), outputDir, filename)

    RUN(f"dot -Kneato -Tsvg {input} -o {output}.svg")

    # Remove old file
    unlink(input)


def only_grid(nodes, pre, co, filename='grid', outputDir="out") -> None:
    """
    Get a student view of grid fluxogram. This plot bot edges, pre and co requisite.
    It run a system call to `graphviz`_.

    :Args:
        - `nodes`: A list containing the nodes.
        - `pre`: A list containing the edges for this graph.
        - `co`: A list containing the edges for this graph.

    :Kwargs:
        - `filename`: The name of the file to save (image name). DEFAULT: grid
        - `outputDir`: The directory to save. DEFAULT: out

    .. note::

        The nodes must be ordered by period of the class.
    """

    # Construct a tree with xml grid
    nameFile = f"{filename}.dot"

    # Setting up digraph plot
    output = Digraph(
        engine='dot',  # 'neato',  # force position
        name=nameFile,
        filename=nameFile,
        directory=outputDir,
        format='svg',
        graph_attr={
            # 'concentrate': 'true',
            'rankdir': 'BT',
            'overlap': 'scale',  # force position
            # splines → polyline, ortho, true/spline, curved
            'splines': 'ortho',  # edge uppon vertix
            # 'margin': '0.5,0.5',
            'sep': '0.5',
        },
        node_attr={
            'pad': '1',
            'nodesep': '2',
            'ranksep': '2'
        }
    )

    # Set a variable that will be responsable to increment x or y variables
    oldPeriod = 1
    incX = incY = 0
    # Insert nodes
    for initials in nodes:
        # Get node
        node = nodes[initials]

        # Get period
        period = node['period']
        if period == 'Optativa':
            continue

        # Check if changed the period.
        if oldPeriod != period:
            incY = 0
            # Increment x padding
            incX += 1
            oldPeriod = period

        # default color
        nodeColor = Colors.node
        # Set node position
        strPos = '{0:.3}'.format(str(incX)) + ',' + "-{}!".format(incY)

        output.node(
            initials,
            initials,
            color='none',
            style='filled',  # 'striped',
            shape='rectangle',
            fillcolor=nodeColor,
            pos=strPos,
            **{  # Node atributes fixed size
                 'fixedsize': 'true',
                'width': '2',
                'height': '1'
            }
            # len='0.5'
            # weight='.5',
        )
        # Increment y padding
        incY += 1

    # In edges you can add other parameters like
    # > edge.attr['label'] = '5'
    # > edge.attr['weight'] = 5

    # Creating the edges for pre requisite graph
    for origin, destination in pre:
        output.edge(origin, destination, color=Colors.RedBased['wine'])

    # Creating the edges for co requisite graph
    for origin, destination in co:
        output.edge(origin, destination, color='black')

    # ! Due to an windows problem with the binaries you must to save and then, run
    # output.render(view=True, filename="output.svg", renderer='neato')
    output.save(directory=outputDir)
    input = path.join(path.abspath(getcwd()), outputDir, f"{filename}.dot")
    output = path.join(path.abspath(getcwd()), outputDir, filename)

    RUN(f"dot -Kneato -Tsvg {input} -o {output}.svg")

    # Remove old file
    unlink(input)


class DotFile(object):
    """
    A class used to generate dot files.

    Check it out more infos in the `graphviz documentation`_

    .. _graphviz documentation: https://graphviz.org/doc/info/attrs.html
    """
    # Command used to generate png image
    # neato -Tpng 2016001942.dot -o teste.png

    def __init__(self):
        self._outputFile = "digraph {\n\trankdir=TB;\n"

    def node(
            self,
            nodeName: str,
            label: str,
            color: str,
            fillcolor: str,
            style: str,
            shape: str,
            pos: str
    ):
        """
        Insert string used to create a node.

        :Args:
            - `nodeName`: Name used to make connections.
            - `label`: Name showed in graph.
            - `color`: Border color.
            - `fillcolor`: Fill color.
            - `pos`: Inch absolute position.
            - `shape`: Form shape
            - `style`: Form style, i.e., filled or striped

        :Example:
            .. code-block:: python
                :linenos:

                dotfile = DotFile()
                dotfile.insert( 'CEI039','CEI039', 'black', 'white', '4,0!', 'rectangle', 'filled')
        """

        auxiliarStr = '\t{} [label="{}" color="{}" fillcolor="{}" pos="{}" shape="{}" style="{}"]\n'.format(
            nodeName, label, color, fillcolor, pos, shape, style)

        self._outputFile += auxiliarStr

    def edge(self, father: str, son: str, style: str, color: str):
        """
        Create connection

        :Parameters:
            - `father`: 'From' node
            - `son`: 'To' node
            - `style`: edge style.
            - `color`: edge color.

        :Example:
            .. code-block:: python
                :linenos:

                a = DotFile()
                a.edge('A','B') # create a connection A→B
        """
        aux = '\t' + father + ' -> ' + son + \
            ' [style={}, color={}]\n'.format(style, color)
        self._outputFile += aux

    def _endOfInput(self):
        """
        Finish this file
        """
        self._outputFile += '\n}'

    def getDot(self, filename: str):
        """
        Gerate dot file.

        :Args:
            - `filename`: Name to save dot's file.

        :Example:
            .. code-block:: python
                :linenos:

                a = DotFile()
                a.getDot('/home/ppcamp/Desktop/test.dot')
        """
        self._endOfInput()
        with open(filename, 'w') as f:
            f.write(self._outputFile)
