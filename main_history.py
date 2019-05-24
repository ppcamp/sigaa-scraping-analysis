from packages.sigaa.history import HistoryScraping

paa = HistoryScraping()
paa.login(user='12638891665', password='Sigaa*0223')
paa.get_History()
paa.xml_History()
paa.quit_webdriver()