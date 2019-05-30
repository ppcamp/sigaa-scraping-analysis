from packages.others.dotFile import DotFile

# XML parser
import xml.etree.ElementTree as ET
from os.path import abspath as abs

nameFile = "/home/ppcamp/Documents/Git/projects/sig-scraping/xml_files/0192015.xml"

studentId = '2016001942'

# Construct a tree with xml grid
root = ET.parse(nameFile).getroot()
nameFile = studentId + '.dot'  # 2016001942.dot

# Inverse tree (Transposte or tree⁻¹)
tree = {}

graphDotOutput = DotFile()

auxX = ''
incX = -2
incY = None

for disciplinas in root.findall('Disciplinas/'):
    for disciplina in disciplinas.findall('.'):
        auxSigla = disciplina.find('Sigla').text

        if (auxX != disciplina.find('Periodo').text):
            auxX = disciplina.find('Periodo').text
            incX += 2
            incY = 0

        strPos = '{0:.3}'.format(str(incX)) + ',' + "-{}!".format(incY)
        # {0:.3}!'.format(incX)
        graphDotOutput.node(
            auxSigla,
            auxSigla,
            'black',
            'white',
            'filled',  # 'striped',
            'rectangle',
            strPos
        )
        incY += 2

        # print("Disciplina: {}".format(auxSigla))
        for pre in disciplina.findall('PreRequisitoTotal/Sigla'):
            auxPre = pre.text
            graphDotOutput.edge(auxPre, auxSigla, 'bold','red')

        """ print(13*"-----")
        for pre in disciplina.findall('PreRequisitoTotal/Sigla'):
            auxPre = pre.text
            graphDotOutput.edge(auxPre, auxSigla)
 """

graphDotOutput.getDot(nameFile)
