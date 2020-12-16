# -*- coding: utf-8 -*-
# fluxogram
from graphviz import Digraph
from os import sep as OSsep
import networkx as nx

# Random over list
# from secrets import choice

# Rand some hexa char
from os import urandom, system as RUN
from binascii import b2a_hex as randHex
from os import path, getcwd, unlink


class Colors(object):
    """
    Color palette in hexa.
    """
    node = "#BDC3C7"

    BlueBased = {
        "baby": "#BDC3C7"
    }
    RedBased = {
        "wine": "#BD1C32",
        "lightenRed": "#FA3246",
        "darkPink": "#BD1C44",
        "darkRed": "#AF0019",
        "darkenRed": "#850014",
        "darkerRed": "#BB0019",
    }
    GreenBased = {
        "nature": "#4c8768"
    }

    @staticmethod
    def rand():
        """
        Generate some random color.
        """
        return randHex(urandom(6))


def only_grid(nodes, pre, co, filename='grid'):
    """
    Get a student view of grid fluxogram.

    Note
    ----
    The nodes must ne ordered by period of the class.
    """

    # Construct a tree with xml grid
    nameFile = f"{filename}.dot"
    outputDir = "out"

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
    output.save(directory="out")
    input = path.join(path.abspath(getcwd()), outputDir, f"{filename}.dot")
    output = path.join(path.abspath(getcwd()), outputDir, filename)

    RUN(f"dot -Kneato -Tsvg {input} -o {output}.svg")

    # Remove old file
    unlink(input)


class DotFile(object):
    """
    A class used to generate dot files.
    """
    # Command used to generate png image
    # neato -Tpng 2016001942.dot -o teste.png

    def __init__(self):
        self._outputFile = "digraph {\n\trankdir=TB;\n"

    def node(self, nodeName, label, color, fillcolor, style, shape, pos):
        """
        Insert string used to create a node.

        Parameters
        ----------
        nodeName: string
            Name used to make connections.
        label: string
            Name showed in graph.
        color: string
            Border color.
        fillcolor: string
            Fill color.
        pos: string
            Inch absolute position.
        shape: string
            Form shape
        style: string
            Form style, i.e., filled or striped

        Example
        -------
        >> insert(
            'CEI039','CEI039', 'black', 'white',
            '4,0!', 'rectangle', 'filled')
        """

        auxiliarStr = '\t{} [label="{}" color="{}" fillcolor="{}" pos="{}" shape="{}" style="{}"]\n'.format(
            nodeName, label, color, fillcolor, pos, shape, style)

        self._outputFile += auxiliarStr

    def edge(self, father, son, style, color):
        """
        Create connection

        Parameters
        ----------
        father: string
            'From' node
        son: string
            'To' node

        Example
        -------
        >> edge('A','B') # A→B
        """
        aux = '\t' + father + ' -> ' + son + \
            ' [style={}, color={}]\n'.format(style, color)
        self._outputFile += aux

    def _endOfInput(self):
        self._outputFile += '\n}'

    def getDot(self, nameFile):
        """
        Gerate dot file.

        Parameters
        ----------
        nameFile: string
            Name to save dot's file.

        Example
        -------
        >> getDot('/home/ppcamp/Desktop/test.dot')
        """
        self._endOfInput()
        with open(nameFile, 'w') as f:
            f.write(self._outputFile)
