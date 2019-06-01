# ========================================
# Coordenator class
# ========================================


# from os.path import abspath as abs
from xml.etree import ElementTree as ET
from packages.sigaa.base import sigaaBase
from packages.sigaa.grid import GridScraping

class Coord(sigaaBase):
    def getFromXml(self, nameFile):
        tree = ET.parse(nameFile)
        print (tree)