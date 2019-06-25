# from packages.others.dotFile import DotFile
from packages.sigaa.history import HistoryScraping

# File
paa = HistoryScraping()

# Login with RA and psswd
paa.login(user='CPF', password='SENHA')

# DO fluxogram
paa.toDiagram(nsgrid='0192015')
paa.toXmlFile()
paa.quit_webdriver()