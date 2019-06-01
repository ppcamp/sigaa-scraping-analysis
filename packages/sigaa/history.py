from packages.sigaa.base import sigaaBase
from packages.sigaa.grid import GridScraping
# ==============================================================
# History
# ==============================================================


class HistoryScraping(sigaaBase):
    """
    This class provides a way to scrap from sigaa system,
    the student history.

    Note
    ----
        1. This class was created following the student view,
           i.e., all url's and methods was based on it.
        2. The pdf scraping wasn't chosen, 'cause the
           system's  generated pdf, didn't get good results.

    Parameters
    ----------
    headless: boolean value
        True to don't show chrome window

    """

    def __init__(self, **kwargs):
        sigaaBase.__init__(self, **kwargs)
        # History tree
        self._history = {}
        # xml.Element tree
        self._tree = None
        # Header's info
        self._yearActualPeriod = None  # Actual yearPeriod
        self._yearInPeriod = None  # Admission yearPeriod
        self._courseName = None  # Computer's Engineering
        self._studentId = None  # RA
        self._gridNumer = None  # 0192015 ECO2015

    def _getHeaderInfo(self, check):
        """
        (Private method): provides a way to get the following
        values:courseName,studentId,yearInPeriod,yearActualPeriod

        Parameters
        ----------
        check: Boolean value
            When pass 'True' the program won't search if it
            find some file with studentId name in xml folder.

        Example
        -------
        > self._getHeaderInfo('check') # won't search.
        """
        try:
            self._courseName = self._chrome_webdriver.find_element_by_css_selector(
                '#agenda-docente > table > tbody > tr:nth-child(2) > td:nth-child(2)').text

            self._studentId = self._chrome_webdriver.find_element_by_css_selector(
                '#agenda-docente > table > tbody > tr:nth-child(1) > td:nth-of-type(2)').text

            self._yearInPeriod = self._chrome_webdriver.find_element_by_css_selector(
                '#agenda-docente > table > tbody > tr:nth-child(6) > td:nth-child(2)').text

            self._yearActualPeriod = self._chrome_webdriver.find_element_by_css_selector(
                '#info-usuario > p.periodo-atual > strong').text

            nameFile = self._folder_xmlFiles + \
                'historico_{}.xml'.format(self._studentId)

            # If file exist AND flag 'check'
            # was passed, cancel search
            if check:
                if self.fileExist(nameFile):
                    self._logFile.write(
                        '[get_History]: Failure! File already exist')
                    return False
            else:
                self._logFile.write('[get_History]->HeadersInfo: Success!\n')
                return True
        except Exception as ex:
            self._logFile.write('[get_History]->HeadersInfo: Failure! {}: {}!\n'.format(
                type(ex).__name__, ex.args))
            return False

    def _getBasicsInfos(self, addBlock):
        """
        (Private method): it creates the columns in
        history dict. It will put values in:
        'nome','turma','ch'.

        Parameters
        ----------
        addBlock: boolean value
            When pass 'True' will create a block
            discipline that will contain only name from
            XXXX.1.

        Example
        -------
        > self._getBasicsInfos('addBlock') # create block
        """
        try:
            self._chrome_webdriver.get(self._url_discipline)
            soup = self.BeautifulSoup(
                self._chrome_webdriver.page_source, 'html5lib')
            soup = soup.find('table', class_='listagem')

            for i in soup.find_all('tr'):
                if i.get('class') is None or i.get('class')[0] == 'destaque':
                    continue

                itsigla = i.find('td').text
                itnome = itsigla[itsigla.find(' - ') + 3:]
                itsigla = itsigla[:itsigla.find(' -')]
                periodo = (i.find_previous('td', class_='periodo').text)
                itturma = i.find_next('td').find_next('td').text
                ch = (i.find_next('td').find_next(
                    'td').find_next('td')).text[:-1]

                if (periodo not in self._history):
                    self._history[periodo] = {
                        itsigla: {
                            'nome': itnome,
                            'turma': itturma,
                            'ch': ch
                        }
                    }
                else:
                    self._history[periodo].update({
                        itsigla: {
                            'nome': itnome,
                            'turma': itturma,
                            'ch': ch
                        }
                    })

                # adding Block discipline
                if addBlock:
                    if itsigla[-1] == '1' and itsigla[-2] == '.':
                        self._history[periodo].update({
                            itsigla[:-2]: {
                                'nome': itnome,
                            }
                        })

            self._logFile.write('[get_History]->Basis: Success!\n')
            return True
        except Exception as ex:
            self._logFile.write('[get_History]->Basis: Failure! {}: {}!\n'.format(
                type(ex).__name__, ex.args))
            return False

    def _getOthersInfos(self):
        """
        (Private method): search for 'resultados','faltas'
        and 'situacao'

        Example
        -------
        > self._getOthersInfos()
        """
        # clean string
        import re as regex
        try:
            # access notes with func cmItemMouseup
            self._chrome_webdriver.get(self._url_default)
            # script found that generates the page
            js_script = "try{cmItemMouseUp('menu_form_menu_discente_j_id_jsp_275447739_49_menu',1);}catch(e){}"
            self._chrome_webdriver.execute_script(js_script)
            soup = self.BeautifulSoup(
                self._chrome_webdriver.page_source, 'html5lib')

            # Search inside the soup tryin' to locate
            # 'faltas','situacao','sigla','resultado','periodo'
            for i in soup.find_all_next('tr', class_='linha'):
                sigla = i.find_next('td')
                resultado = sigla.find_next('td').find_next(
                    'td').find_next('td').find_next('td').find_next('td')
                faltas = resultado.find_next('td')
                situacao = faltas.find_next('td')

                sigla = sigla.text.replace(' ', '')
                sigla = regex.sub('[\n\t]', "", sigla)

                resultado = resultado.text.replace(' ', '')
                resultado = regex.sub('[\n\t]', "", resultado)

                faltas = faltas.text.replace(' ', '')
                faltas = regex.sub('[\n\t]', "", faltas)

                situacao = situacao.text.replace(' ', '')
                situacao = regex.sub('[\n\t]', "", situacao)

                periodo = regex.sub(r'\s', '', i.find_previous('caption').text)

                if sigla in self._history[periodo]:
                    self._history[periodo][sigla].update({
                        'resultado': resultado,
                        'faltas': faltas,
                        'situacao': situacao
                    })

            self._logFile.write('[get_History]->InfosHistory: Success!\n')
            return True
        except Exception as ex:
            self._logFile.write('[get_History]->InfosHistory: Failure! {}: {}!\n'.format(
                type(ex).__name__, ex.args))
            return False

    def _getPdfInfo(self):
        """
        (Private method): only used to get student's grid number

        Example
        -------
        > self._getPdfInfo()

        Note
        ----
        This method will probably be disabled. The cost to got grid number
        is too high, need too much libraries, and isn't optimum solution.
        """
        # check if file (pdf) exist in temp files, otherwise download it
        nameFile = self._folder_temp + \
            'historico_{}.pdf'.format(self._studentId)
        if not self.fileExist(nameFile):
            self._chrome_webdriver.get(self._url_default)
            # script found that download the pdf file
            js_script = "try{cmItemMouseUp('menu_form_menu_discente_j_id_jsp_275447739_49_menu',4);}catch(e){}"
            self._chrome_webdriver.execute_script(js_script)

        # Lib needed to scrap from pdf
        import textract
        # PDF (Getting grid)

        try:
            pt = textract.process(
                '{}historico_{}.pdf'.format(
                    self._folder_temp, self._studentId),
                method='pdftotext'
            )
            pt = pt.decode("UTF-8")
            pt = str(pt)
            pt = pt.split('\n')
            n = []

            for i in pt:
                if not i.strip():
                    continue
                else:
                    n.append(i)
            pt = '\n'.join(n)

            search = pt.find('Currículo:\n') + 11
            self._gridNumber = ''.join(
                [i for i in pt[search:pt.find('\n', search)] if i.isdigit()])
            # search = pt.find('Período Letivo Atual:\n') + 22
            # self._yearActualPeriod = pt[search:pt.find('\n', search)]

            self._logFile.write('[get_History]->PDF: Success!\n')
        except Exception as ex:
            self._logFile.write('[get_History]->PDF: Failure! {}: {}!\n'.format(
                type(ex).__name__, ex.args))

    def getHistory(self, check=False, addBlock=True, xml=False):
        """
        Set the history. This method assumes that
        you did _login with student account.\n
        You can pass argument 'xml' to generate file when finish.

        Parameters
        ----------
        check: Boolean value
            When pass 'True' the program won't search if it
            find some file with studentId name in xml folder.
        addBlock: boolean value
            When pass 'True' will create a block
            discipline that will contain only name from
            XXXX.1.
        xml: boolean value
            'True' to execute method 'toXmlFile'

        Example
        -------
        > get_history(check=False,addBlock=True) # 'toFluxogram()'

        """

        # Header's info
        if not self._getHeaderInfo(check):
            return False

        # Create basis with (Nome, sigla, CH, Turma)
        if not self._getBasicsInfos(addBlock):
            return False

        # Adding info to history (notas, faltas, situacao)
        if not self._getOthersInfos():
            return False

        # Searching for grid number
        if not self._getPdfInfo():
            return False

        # GENERATE XML
        if xml:
            self.toXmlFile(True)

    def _getTree(self):
        # XML
        from xml.etree import ElementTree as ET

        # increase every six months
        def aplus(j):
            def incrementyear(s): return (str(int(s[:-2]) + 1) + '.1')
            def incrementsem(s): return (s[:-1] + '2')
            return (incrementyear(j) if j[-1] == '2' else incrementsem(j))
        # used to calc frequency
        def freq(c, s): return str(round((int(c)-int(s))/int(c)*100))

        root = ET.Element('HistoricoCurricular')

        ET.SubElement(root, 'Curso').text = self._courseName
        ET.SubElement(root, 'Grade').text = self._gridNumber
        ET.SubElement(root, 'Matricula').text = self._studentId
        ET.SubElement(root, 'AnoPeriodoInicial').text = self._yearInPeriod
        ET.SubElement(
            root, 'AnoPeriodoAtual').text = self._yearActualPeriod

        fstLevel = ET.SubElement(root, 'Semestre')

        semestre = self._yearInPeriod
        while semestre != self._yearActualPeriod:
            sndLevel = ET.SubElement(fstLevel, 'A{}'.format(semestre))

            for sigla in self._history[semestre]:
                trdLevel = ET.SubElement(sndLevel, 'Disciplina')
                ET.SubElement(
                    trdLevel, 'Nome').text = self._history[semestre][sigla]['nome']

                ET.SubElement(trdLevel, 'Sigla').text = sigla

                if 'ch' in self._history[semestre][sigla]:
                    ET.SubElement(trdLevel, 'Frequencia').text = freq(
                        self._history[semestre][sigla]['ch'],
                        self._history[semestre][sigla]['faltas'])
                    ET.SubElement(
                        trdLevel, 'CH').text = self._history[semestre][sigla]['ch']

                ET.SubElement(
                    trdLevel, 'Nota').text = self._history[semestre][sigla]['resultado']

                ET.SubElement(
                    trdLevel, 'Situacao').text = self._history[semestre][sigla]['situacao']

            semestre = aplus(semestre)

        self._tree = ET.ElementTree(root)

    def toXmlFile(self, createTree=False):
        """
        Generate XML history file

        Example
        -------
        >> toXmlFile() # It creates a xml file, saving all infos.
        """

        if createTree:
            self._getTree()

        nameFile = self._folder_xmlFiles + \
            'historico_{}.xml'.format(self._studentId)

        if not self.fileExist(nameFile):
            try:
                self._tree.write(nameFile)
                self._logFile.write('[toXmlFile]: Success!\n')
            except Exception as ex:
                self._logFile.write('[toXmlFile]: Failure! {}: {}\n'.format(
                    type(ex).__name__, ex.args))
        else:
            self._logFile.write('[toXmlFile]: Failure! File already exists.\n')

    def toDiagram(self, search=True):
        """
        Get a student view of grid fluxogram.

        Parameters
        ----------
        search: boolean value
            'True' to do all history search.

        Note
        ----
        This method will do all search again by default, however
        if you disable, you must do 'getHistory()' before, else
        the program will fail, 'cause won't have values from
        _history dict.
        """

        if search:
            self.getHistory()

        # Check if course grid exist in xml folder
        # If grid doesn't exist, download it
        nameFile = self._folder_xmlFiles + self._courseCode + '.xml'
        if not self.fileExist(nameFile):
            searchGrid = GridScraping()  # (headless=True)
            searchGrid.login(user=self._userName, password=self._userPsswd)
            searchGrid.set_codCurso(self._courseCode)
            searchGrid.get_Grid()
            searchGrid.xml_Grid()
            searchGrid.quit_webdriver()

        # Construct a tree with xml grid
        import xml.etree.ElementTree as ET  # XML parser
        from os.path import abspath as abs  # path
        from graphviz import Digraph  # fluxogram

        # Construct a tree with xml grid
        root = ET.parse(nameFile).getroot()
        nameFile = self._studentId + '.dot'  # 2016001942.dot

        # edge pre color vector
        # due the number of pre requisites
        # it was necessary a color palette to discretize it
        # and facilitate the graph view, also the format svg
        # was chosen due blur when zoom the flags.
        colorVectorEdge = [
            '#FA5F6E', '#FA3246', '#FA253B', '#FA142B', '#BD1C32',
            '#BD0D25', '#AF0019', '#850014', '#840019', '#BB0019'
        ]

        # Setting up digraph plot
        graphDotOutput = Digraph(
            engine='neato',  # force position
            name=nameFile,
            filename=nameFile,
            directory=abs(''),
            format='svg',
            graph_attr={
                # 'concentrate': 'true',
                'rankdir': 'BT',
                'overlap': 'scale',  # force position
                # splines → polyline, ortho, true/spline, curved
                'splines': 'ortho',  # edge uppon vertix
                # 'margin': '0.5,0.5',
                'sep': '0.5',
            },
            node_attr={
                'pad': '1',
                'nodesep': '2',
                'ranksep': '2'
            }
        )

        auxX = ''
        incX = -1
        incY = None
        includedNodes = set()

        # Loop for nodes
        for disciplinas in root.findall('Disciplinas/'):
            # Searching for Disciplinas
            for disciplina in disciplinas.findall('.'):
                # Creating vertix
                if (auxX != disciplina.find('Periodo').text):
                    auxX = disciplina.find('Periodo').text
                    incX += 1
                    incY = 0
                if (auxX == 'Optativa'):
                    continue

                auxSigla = disciplina.find('Sigla').text
                nodeColor = '#BDC3C7'  # default color

                # Search for discipline and get the color
                # from last disciplines, i.e., if you be approved
                # by some discipline after you be reproved in
                # previous semester, it'll got approved color.
                for itPeriodo, _ in reversed(list(self._history.items())):
                    # skip if don't find in dict
                    if auxSigla not in self._history[itPeriodo]:
                        continue
                    situacaoMateria = self._history[itPeriodo][auxSigla]['situacao']
                    if (situacaoMateria == 'APROVADO'):
                        nodeColor = '#2ECC71'  # EMERALD
                    elif (situacaoMateria == 'REPROVADO'):
                        nodeColor = '#E74C3C'  # ALIZARIN
                    elif (situacaoMateria == '--'):
                        nodeColor = '#9B59B6'  # Amethyst
                    # break

                strPos = '{0:.3}'.format(str(incX)) + ',' + "-{}!".format(incY)

                graphDotOutput.node(
                    auxSigla,
                    auxSigla,
                    color='none',
                    style='filled',  # 'striped',
                    shape='rectangle',
                    fillcolor='{}'.format(nodeColor),
                    pos=strPos,
                    **{  # Node atributes fixed size
                        'fixedsize': 'true',
                        'width': '2',
                        'height': '1'
                    }
                    # len='0.5'
                    # weight='.5',
                )
                # this approach only worth cause the tree is in order
                includedNodes.add(auxSigla)
                incY += 1

                # Creating pre edges
                for pre in disciplina.findall('PreRequisitoTotal/Sigla'):
                    auxPre = pre.text
                    if auxPre in includedNodes:
                        graphDotOutput.edge(
                            auxPre, auxSigla, color=colorVectorEdge[int(auxX)-1])
                # Creating co edges
                for pre in disciplina.findall('CoRequisito/Sigla'):
                    auxPre = pre.text
                    if auxPre in includedNodes:
                        graphDotOutput.edge(
                            auxPre, auxSigla, color='black')

            # end disciplina loop
        # end disciplinas loop
        graphDotOutput.render(view=True)
