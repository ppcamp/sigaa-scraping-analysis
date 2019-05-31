# from packages.others.dotFile import DotFile
from packages.sigaa.history import HistoryScraping
paa = HistoryScraping()
paa.login(user='', password='')
paa.get_History()
paa.quit_webdriver()
# paa.xml_History()
paa.diagram_History()
