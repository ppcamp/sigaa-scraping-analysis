from packages.sigaa.base import sigaaBase
# ==============================================================
# Grid
# ==============================================================


class GridScraping(sigaaBase):

    def __init__(self, **kwargs):
        sigaaBase.__init__(self, **kwargs)

        # Grid
        self._yearBase = None
        self._grid_Cod = None
        self._grid_Period = None
        self._grid_Name = None
        self._grid_Prerequisite = None
        self._grid_Corequisite = None
        self._courseName = None

    def get_Grid(self, *argv):
        """
        Get informations to mount grid.

        Parameters
        ----------
        'xml': argument
            You can pass a 'xml' to auto generate file when finish.

        Example
        -------
        >> get_Grid() # mount grid internal var
        >> get_Grid('xml') # also generates a file.
        """
        # Used in get_Grid()
        import re as regex

        try:
            self._chrome_webdriver.get(self._url_grid)
            self._chrome_webdriver.find_element_by_id('busca:codigo').clear()
            self._chrome_webdriver.find_element_by_id(
                'busca:checkCodigo').click()
            box = self._chrome_webdriver.find_element_by_id('busca:codigo')
            box.send_keys(self._courseCode)
            box.send_keys(self.Keys.ENTER)
            self._chrome_webdriver.find_element_by_id(
                'resultado:relatorio').click()
            soup = self.BeautifulSoup(
                self._chrome_webdriver.page_source, 'html5lib')

            self._logFile.write('[get_Grid]->Buscando: Success!\n')
        except Exception as ex:
            self._logFile.write('[get_Grid]->Buscando: Failure! {}: {}\n'.format(
                type(ex).__name__, ex.args))
        try:
            # Creating dicts
            self._yearBase = (soup.select(
                '#relatorio > table > tbody > tr:nth-of-type(5) > td')[0].text)
            self._yearBase = self._yearBase.replace(' ', '')
            self._courseName = (soup.select(
                '#relatorio > table > tbody > tr:nth-of-type(2) > td')[0].text)
            self._courseName = self._courseName[:self._courseName.find(' - ')]
            self._grid_Cod = []
            self._grid_Period = []
            self._grid_Name = []
            self._grid_Prerequisite = {}
            self._grid_Corequisite = {}
            for i in soup.find_all('tr', class_='componentes'):
                cod = i.find_all('td')[0].text
                p = i.find_previous('tr', class_='tituloRelatorio').text
                n = i.find_all('td')[1].text
                n = regex.sub(r'[\t\n]', '', n)
                p = regex.sub(r'[\t\n]', '', p)
                n = n[:n.rfind(' - ')]
                aux = regex.search(r"[\d]+", p)

                p = 'Optativa'
                if (aux is not None):
                    p = aux.group()

                if (cod not in self._grid_Cod):
                    self._grid_Cod.append(cod)
                    self._grid_Name.append(n)
                    self._grid_Period.append(p)

            nameFile = '{}{}_{}.xml'.format(
                self._folder_xmlFiles, self._courseCode, self._courseName)

            if self.fileExist(nameFile):
                raise Exception('searchError', 'File already exist')

            # Starting counting
            # countPreCo = 0

            # Searching pre and co requisites
            for i, j in zip(self._grid_Cod, self._grid_Period):
                # countPreCo += 1
                # Don't search 'Optativa' pre requisite
                if j == "Optativa":
                    continue

                self._chrome_webdriver.get(self._url_component)
                self._chrome_webdriver.find_element_by_name(
                    'formBusca:checkCodigo').click()

                box = self._chrome_webdriver.find_element_by_name(
                    'formBusca:j_id_jsp_433775776_860')
                box.clear()
                box.send_keys(i)
                box.send_keys(self.Keys.ENTER)

                # Block
                box = self._chrome_webdriver.find_elements_by_xpath(
                    '//a[@title=\'Relatório para impressão\' ]')
                if len(box) == 3:
                    box[1].click()
                elif len(box) == 1:
                    box[0].click()

                pre = (self._chrome_webdriver.find_element_by_xpath(
                    '//th[text()[contains(.,\'Pré-Requisitos:\')]]/\
                        following-sibling::td')).text
                co = (self._chrome_webdriver.find_element_by_xpath(
                    '//th[text()[contains(.,\'Co-Requisitos:\')]]/\
                        following-sibling::td')).text

                # Minimum word's size its |OU|
                pre = regex.findall(r'[\w\d]{3,}', pre)
                co = regex.findall(r'[\w\d]{3,}', co)

                self._grid_Prerequisite[i] = pre
                self._grid_Corequisite[i] = co

                # Couting percentile
                # percentile = int((countPreCo*100)/len(self._grid_Cod))
                # print('Percent: {}%'.format(percentile))

            self._logFile.write('[get_Grid]->Requisitos: Success!\n')
        except Exception as ex:
            self._logFile.write('[get_History]->PDF: Failure! {}: {}!\n'.format(
                type(ex).__name__, ex.args))

        # GENERATE XML
        if (len(argv) > 0):
            if argv[0] == 'xml':
                self.xml_Grid()

    def xml_Grid(self):
        """
        Generate XML grid file

        Example
        -------
        >> xml_Grid() # It creates a xml file, saving all infos.
        """
        # XML
        from xml.etree import ElementTree as ET

        nameFile = '{}{}_{}.xml'.format(
            self._folder_xmlFiles, self._courseCode, self._courseName)

        if not self.fileExist(nameFile):
            root = ET.Element('A{}'.format(self._courseCode))
            ET.SubElement(root, 'Curso').text = self._courseName
            ET.SubElement(root, 'Ano').text = self._yearBase
            # It counts all disciplines, i.e., 'Optional' and 'Obrigatory'
            ET.SubElement(root, 'NDisciplinas').text = str(len(self._grid_Cod))

            secondLevel = ET.SubElement(root, 'Disciplinas')
            for cod, nome, per in zip(self._grid_Cod,
                                      self._grid_Name, self._grid_Period):

                thirdLevel = ET.SubElement(secondLevel, 'Disciplina')
                ET.SubElement(thirdLevel, 'Nome').text = nome
                ET.SubElement(thirdLevel, 'Sigla').text = cod
                ET.SubElement(thirdLevel, 'Periodo').text = per

                if cod in self._grid_Prerequisite and self._grid_Prerequisite[cod]:
                    fourthLevel = ET.SubElement(
                        thirdLevel, 'PreRequisitoTotal')
                    for j in self._grid_Prerequisite[cod]:
                        ET.SubElement(fourthLevel, 'Sigla').text = j

                if cod in self._grid_Corequisite and self._grid_Corequisite[cod]:
                    fourthLevel = ET.SubElement(thirdLevel, 'CoRequisito')
                    for j in self._grid_Corequisite[cod]:
                        ET.SubElement(fourthLevel, 'Sigla').text = j

            tree = ET.ElementTree(root)
            tree.write(nameFile)

            self._logFile.write('[xml_Grid]: Success!\n')
        else:
            self._logFile.write('[xml_Grid]: Failure! File already exist\n')
