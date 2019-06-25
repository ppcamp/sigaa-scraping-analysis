# ===========================================
# Coordenator view
#
# Note: this view consider also when you got
# reproved once, before pass through.
# ===========================================

def coordView():
    """
    This function assumes that you already have
    the grid xml's inside folder 'xml_files',

    Note
    ----
    This method use grids inside xml folder to
    generate grids view to all histories in folder.
    """
    from graphviz import Digraph  # fluxogram
    from os.path import abspath as abs  # path
    import lxml.etree as ET  # XML parser
    from os.path import abspath
    from os import listdir
    import re as regex

    _folder_project = abspath('') + '/'
    _folder_temp = _folder_project + 'xml_files/'

    # get all histories in xml folder
    histories = [i for i in listdir(
        _folder_temp) if regex.match('[historico_]', i)]

    # dict that will hold the grids numbers
    gridsNumbers = {}
    # dict that will hold the trees from lxml
    studentsData = {}

    # order those histories by grid key
    for i in histories:
        tree = ET.parse(_folder_temp + i)
        root = tree.getroot()

        aux = root.find('Grade').text
        if aux not in gridsNumbers:
            gridsNumbers[aux] = []
        # RA only
        ra = i[10:-4]
        gridsNumbers[aux].append(ra)

        studentsData[ra] = root

    # Construct a tree with xml grid


    for grid in gridsNumbers:
        # Construct a tree with xml grid
        root = ET.parse(_folder_temp + grid + '.xml').getroot()

        nameFile = grid + '_coordView'
        # edge pre color vector
        # due the number of pre requisites
        # it was necessary a color palette to discretize it
        # and facilitate the graph view, also the format svg
        # was chosen due blur when zoom the flags.
        colorVectorEdge = [
            '#FA5F6E', '#FA3246', '#FA253B', '#FA142B', '#BD1C32',
            '#BD0D25', '#AF0019', '#850014', '#840019', '#BB0019'
        ]

        # Setting up digraph plot
        graphDotOutput = Digraph(
            engine='neato',  # force position
            name=nameFile,
            filename=nameFile,
            directory=abs(''),
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

        auxX = ''
        incX = -1
        incY = None
        includedNodes = set()

        for disciplinas in root.findall('Disciplinas/'):
            # Searching for Disciplinas
            for disciplina in disciplinas.findall('.'):
                # Creating vertix
                if (auxX != disciplina.find('Periodo').text):
                    auxX = disciplina.find('Periodo').text
                    incX += 1
                    incY = 0
                if (auxX == 'Optativa'):
                    continue

                auxSigla = disciplina.find('Sigla').text

                nodeColor = '#BDC3C7'  # default color

                # STUDENTS percents
                percentApproved = 0
                percentReproved = 0
                percentDoing = 0
                percent100 = 0

                for studentId in gridsNumbers[grid]:
                    n = "//Sigla[text()[contains(.,'{}')]]/../Situacao".format(auxSigla)
                    for i in studentsData[studentId].xpath(n):
                        if (i.text == 'APROVADO'):
                            percentApproved += 1
                        elif (i.text == 'REPROVADO'):
                            percentReproved += 1
                        elif (i.text == '--'):
                            percentDoing += 1

                        percent100 += 1

                strPos = '{0:.3}'.format(str(incX)) + ',' + "-{}!".format(incY)

                def getPercent(p, n):
                    """
                    Lambda function used to return percent

                    Parameters
                    ----------
                    p: integer
                        Amount to calculate.
                    n: integer
                        Total amount.

                    Example
                    -------
                    > getPercent(1,5)
                    """
                    return str(p/n) if n > 0 else '0'

                # if nobody did yet
                if percent100 == 0:
                    sfillcolor = nodeColor
                else:
                    sfillcolor = '{};{}:{};{}:{};{}'.format(
                        '#2ECC71', getPercent(percentApproved, percent100),
                        '#E74C3C', getPercent(percentReproved, percent100),
                        '#9B59B6', getPercent(percentDoing, percent100))

                graphDotOutput.node(
                    auxSigla,
                    auxSigla,
                    color='none',
                    style='striped',
                    shape='rectangle',
                    fillcolor=sfillcolor,
                    pos = strPos,
                    **{  # Node atributes fixed size
                        'fixedsize': 'true',
                        'width': '2',
                        'height': '1'
                    }
                    # len='0.5'
                    # weight='.5',
                )
                # this approach only worth cause the tree is in order
                includedNodes.add(auxSigla)
                incY += 1

                # Creating pre edges
                for pre in disciplina.findall('PreRequisitoTotal/Sigla'):
                    auxPre=pre.text
                    if auxPre in includedNodes:
                        graphDotOutput.edge(
                            auxPre, auxSigla, color = colorVectorEdge[int(auxX)-1])
                # Creating co edges
                for pre in disciplina.findall('CoRequisito/Sigla'):
                    auxPre=pre.text
                    if auxPre in includedNodes:
                        graphDotOutput.edge(
                            auxPre, auxSigla, color = 'black')
            # end disciplina loop
        # end disciplinas loop
        graphDotOutput.render(view = True)
