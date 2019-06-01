# from packages.others.dotFile import DotFile
from packages.sigaa.history import HistoryScraping

# File
paa = HistoryScraping()

# Login with RA and psswd
paa.login(user='USER', password='PSSWD')

# DO fluxogram
paa.toDiagram(nsgrid='0192015')
paa.quit_webdriver()