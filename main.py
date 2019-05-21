from packages.SScraping import SScraping as Sigaa

# paa = Sigaa(headless=True)
paa = Sigaa()
paa.login(user='12638891665', password='Sigaa*0223')

paa.set_codCurso('0202010')
paa.get_Grid('xml')
# paa.get_Grid('xml') is equal to ...
#   .. paa.get_Grid()
#   .. paa.xml_Grid()
# paa.get_History('xml')

paa.quit_webdriver()
