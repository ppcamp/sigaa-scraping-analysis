# from packages.others.dotFile import DotFile
from packages.sigaa.history import HistoryScraping

# File
paa = HistoryScraping()

# Login with RA and psswd
paa.login(user='12638891665', password='Sigaa*0223')

# DO fluxogram
paa.toDiagram()
paa.quit_webdriver()