# from packages.others.dotFile import DotFile
from packages.sigaa.history import HistoryScraping

# File
paa = HistoryScraping()

# Login with RA and psswd
paa.login(user='RA', password='SENHA')

# DO fluxogram
paa.toDiagram()
paa.quit_webdriver()