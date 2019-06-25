# -*- coding: utf-8 -*-


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
        aux = '\t' + father + ' -> ' + son + ' [style={}, color={}]\n'.format(style, color)
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
