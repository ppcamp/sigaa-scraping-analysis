"""
This package have the classes needed to get
Sigaa scraping
"""

# Imports
# ------------------------------------------------------
# Clean \t\n. Used in get_Grid() and get_History()
import re as regex
# Current dir
from os.path import abspath

# Parser and tree for html
from bs4 import BeautifulSoup
# Webdriver used for automatization
from selenium import webdriver
# ENTER key
from selenium.webdriver.common.keys import Keys

# PDF
import textract

# logfile
from datetime import datetime


# Class
# ------------------------------------------------------
class BasicXml(object):
    """
    Class used to create a basic parsed XML file.
    This class creates a string that contains the file
    with special chars '[\t\n]', in anoter words,
    a parsed document
    """

    __out = '<?xml version="1.0" encoding="UTF-8"?>\n'
    __stack = []

    def _indent(self):
        """ Used to parse tags"""
        return '\t'*len(self.__stack)

    def create_tag(self, tagname, value):
        """
        Create a new tag

        Parameters
        ----------
        tagname: string
            Name desired for xml's tags.
        value: string
            Value to be placed inside,an empty value '',
            means that will have a break

        Example
        -------
        >> create_tag('html','Test') # <html>test
        >> create_tag('html','')
        >> create_tag('data','test') # <html>\n\t<data>test
        """
        self.__out += self._indent() + '<{}>'.format(tagname)
        self.__stack.append(tagname)

        if value == '':
            self.__out += '\n'
        else:
            self.__out += value
            self.end_tag()

    def end_tag(self):
        """
        Pop's out from stack, and close last tag

        Example
        -------
        >> end_tag() # </html> e.g.
        """
        tagname = self.__stack.pop()
        if self.__out[-1] == '\n':
            self.__out += self._indent()
        self.__out += '</{}>\n'.format(tagname)

    def __init__(self):
        """
        Ctr for this class, it clears the env variables when called
        """
        self.clear()

    def getXml(self):
        """
        Get XML string

        Returns
        -------
        result: string
            Returns the string containing the xml.

        Example
        -------
        >> getXml() # <html></html>
        """
        return self.__out

    def clear(self):
        """
        Clear environment variables

        Example
        -------
        >> clear() # reset default xml code to <?xml ...>
        """
        self.__out = '<?xml version="1.0" encoding="UTF-8"?>\n'
        self.__stack.clear()

    def toFile(self, name):
        """
        Create XML file. You must pass a name containing path to file.

        Example
        -------
        >> toFile('/home/user/tes.xml') # generate file 'tes.xml'
        """

        f = open(name, 'w', encoding='utf-8')

        if not f.closed:
            f.write(self.getXml())
            f.close()
            return True
        else:
            return False


# =============================================================================
# CLass SScrapping
# =============================================================================
class SScraping(object):
    """
    Class used to do scraping from
    UNIFEI's SIGAA system.
    """

    __ur_login = "https://sigaa.unifei.edu.br/sigaa/verTelaLogin.do"
    __url_component = "https://sigaa.unifei.edu.br/sigaa/geral/componente\
_curricular/busca_geral.jsf"
    __url_grid = "https://sigaa.unifei.edu.br/sigaa/geral/estrutura\
_curricular/busca_geral.jsf"
    __url_discipline = "https://sigaa.unifei.edu.br/sigaa/portais/discente/\
turmas.jsf"
    __url_default = "https://sigaa.unifei.edu.br/sigaa/portais/discente/\
discente.jsf"

    __folder_project = abspath('') + '/'
    __folder_webdriver = __folder_project + 'webdriver/chromedriver'
    __folder_temp = __folder_project + '.temp_files/'
    __folder_xmlFiles = __folder_project + 'xml_files/'
    __folder_logs = __folder_project + 'logs/'

    def __init__(self, **kwargs):
        self.courseNumber = '0192015'  # ECO-2015.1 by default
        self.userName = ''
        self.userPsswd = ''
        self.gridNumber = ''
        self.actualYearNumber = ''  # Got in pdf
        self.initialYearNumber = ''  # Got in pdf
        self.curso = ''

        # Grid
        self.cname_cod = []
        self.cname_p = []
        self.cname_n = []
        self.cname_pre = {}
        self.cname_co = {}

        # History
        self.history = {}

        # Webdriver
        self.chrome_options = webdriver.ChromeOptions()
        # default location for linux
        self.chrome_options.binary_location = "/usr/bin/google-chrome"
        # path to chromedriver
        self.chrome_webdriver_path = self.__folder_project + \
            '/webdriver/chromedriver'
        # set folder to '.temp_files' in project folder
        self.chrome_options.add_experimental_option(
            "prefs",
            {
                'download.default_directory': self.__folder_temp,
                'download.prompt_for_download': False
            }
        )
        # Pass headless=True to hide the window
        if(kwargs):
            if (('headless' in kwargs) and kwargs['headless']):
                self.chrome_options.add_argument('--headless')
        # Window
        self.chrome_webdriver = webdriver.Chrome(
            executable_path=self.chrome_webdriver_path,
            options=self.chrome_options)

        # LOGFILE
        l = datetime.now()
        logName = '{}-{}-{}_{}-{}.txt'.format(l.year,
                                              l.month, l.day, l.hour, l.minute)
        self.log = open('{}{}'.format(
            self.__folder_logs, logName), 'a', encoding='utf8')

        # XML OUTPUT
        self.to_xml = BasicXml()

        # Cleaning variables unused

    def set_user(self, userName):
        """
        Set user's system.

        Parameters
        ----------
        userName: string
            User name used to login in sigaa's system.

        Example
        -------
        >> set_user('123')
        """
        self.userName = userName
        self.log.write('[set_user]: Success!\n')

    def set_psswd(self, userPsswd):
        """
        Set password used for user

        Parameters
        ----------
        userPsswd: string
            User password to login.

        Example
        -------
        >> set_psswd('456')
        """
        self.userPsswd = userPsswd
        self.log.write('[set_psswd]: Success!\n')

    def set_codCurso(self, courseNumber):
        """
        Set course code

        Parameters
        ----------
        courseNumber: string
            Number's course.

        Example
        -------
        >> set_codCurso('0192015')
        """
        self.courseNumber = courseNumber
        self.log.write('[set_codCurso]: Success!\n')

    def set_chromeBinary(self, binLoc):
        """
        Set location for chrome binary location
        by default, the value is used for default
        *.deb install

        Parameters
        ----------
        binLoc: string
            Set global path to chrome binary location.

        Example
        -------
        >> set_chromeBinary('/usr/bin/')
        """
        self.chrome_options.binary_location = binLoc
        self.log.write('[set_chromeBinary]: Success!\n')

    def quit_webdriver(self):
        """
        Close window used for autotization.

        Example
        -------
        >> quit_webdriver()
        """
        self.chrome_webdriver.quit()
        self.log.write('[Quit_webdriver]: Success!\n')

    def fileExist(self, name):
        """
        Check if XML file exist. You must pass a name with path to file

        Parameters
        ----------
        name: string
            Pass a name to check if file exist.

        Example
        -------
        >> fileExist('/home/user/Desktop/f.xml')
        """
        try:
            f = open(name, 'r')
            f.close()
            return True
        except:
            return False

    def login(self, **kwargs):
        """
        Try to login in Unifei's sigaa.

        Parameters
        ----------
        user= 'UserName'
            Simulates set_user('123')
        password= 'Password\'sUser'
            Simulates set_psswd('456')

        Example
        -------
        >> login() # just login
        >> login(user='123', password='456') # pass values and then login.
        """
        if(kwargs):
            if (('user' in kwargs) and ('password' in kwargs)):
                self.set_user(kwargs['user'])
                self.set_psswd(kwargs['password'])

        if (not self.userName or not self.userPsswd):
            self.log.write(
                '[login]: Failure. It must have an userName and psswd\n')
            return False

        try:
            # Accessing url
            self.chrome_webdriver.get(self.__ur_login)

            # Find element
            user_name = self.chrome_webdriver.find_element_by_name(
                "user.login")
            # Clean field
            user_name.clear()
            # Send content to field
            user_name.send_keys(self.userName)

            user_pwd = self.chrome_webdriver.find_element_by_name("user.senha")
            user_pwd.clear()
            user_pwd.send_keys(self.userPsswd)

            user_pwd.send_keys(Keys.ENTER)

            if (self.chrome_webdriver.current_url != self.__url_default):
                raise Exception('loginError', 'Wrong username or password')

            self.log.write('[login]: Success!\n')

        except Exception as ex:
            self.log.write('[login]: Failure! {}: {}\n'.format(
                type(ex).__name__, ex.args))

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
        try:
            self.chrome_webdriver.get(self.__url_grid)
            self.chrome_webdriver.find_element_by_id('busca:codigo').clear()
            self.chrome_webdriver.find_element_by_id(
                'busca:checkCodigo').click()
            box = self.chrome_webdriver.find_element_by_id('busca:codigo')
            box.send_keys(self.courseNumber)
            box.send_keys(Keys.ENTER)
            self.chrome_webdriver.find_element_by_id(
                'resultado:relatorio').click()
            soup = BeautifulSoup(self.chrome_webdriver.page_source, 'html5lib')

            self.log.write('[get_Grid]->Buscando: Success!\n')
        except Exception as ex:
            self.log.write('[get_Grid]->Buscando: Failure! {}: {}\n'.format(
                type(ex).__name__, ex.args))
            return False

        try:
            # Creating dicts
            self.ano = (soup.select(
                '#relatorio > table > tbody > tr:nth-of-type(5) > td')[0].text)
            self.ano = self.ano.replace(' ', '')
            self.curso = (soup.select(
                '#relatorio > table > tbody > tr:nth-of-type(2) > td')[0].text)
            self.curso = self.curso[:self.curso.find(' - ')]
            self.cname_cod = []
            self.cname_p = []
            self.cname_n = []
            self.cname_pre = {}
            self.cname_co = {}
            for i in soup.find_all('tr', class_='componentes'):
                cod = i.find_all('td')[0].text
                p = i.find_previous('tr', class_='tituloRelatorio').text
                n = i.find_all('td')[1].text
                n = regex.sub('[\t\n]', '', n)
                p = regex.sub('[\t\n]', '', p)
                n = n[:n.rfind(' - ')]
                aux = regex.search('[\d]+', p)

                p = 'Optativa'
                if (aux is not None):
                    p = aux.group()

                self.cname_cod.append(cod)
                self.cname_n.append(n)
                self.cname_p.append(p)

            # Searching pre and co requisites
            for i, j in zip(self.cname_cod, self.cname_p):
                # Don't search 'Optativa' pre requisite
                if j == "Optativa":
                    continue

                self.chrome_webdriver.get(self.__url_component)
                self.chrome_webdriver.find_element_by_name(
                    'formBusca:checkCodigo').click()

                box = self.chrome_webdriver.find_element_by_name(
                    'formBusca:j_id_jsp_433775776_860')
                box.clear()
                box.send_keys(i)
                box.send_keys(Keys.ENTER)

                # Block
                box = self.chrome_webdriver.find_elements_by_xpath(
                    '//a[@title=\'Relatório para impressão\' ]')
                if len(box) == 3:
                    box[1].click()
                elif len(box) == 1:
                    box[0].click()

                pre = (self.chrome_webdriver.find_element_by_xpath(
                    '//th[text()[contains(.,\'Pré-Requisitos:\')]]/\
                        following-sibling::td')).text
                co = (self.chrome_webdriver.find_element_by_xpath(
                    '//th[text()[contains(.,\'Co-Requisitos:\')]]/\
                        following-sibling::td')).text

                # Minimum word's size its |OU|
                pre = regex.findall('[\w\d]{3,}', pre)
                co = regex.findall('[\w\d]{3,}', co)

                self.cname_pre[i] = pre
                self.cname_co[i] = co

            self.log.write('[get_Grid]->Requisitos: Success!\n')
        except Exception as ex:
            self.log.write('[get_History]->PDF: Failure! {}: {}!\n'.format(
                type(ex).__name__, ex.args))

        # GENERATE XML
        if argv[0] == 'xml':
            self.xml_Grid()

    def xml_Grid(self):
        """
        Generate XML grid file

        Example
        -------
        >> xml_Grid() # It creates a xml file, saving all infos.
        """
        aux = '{}{}_{} - {}.xml'.format(
            self.__folder_xmlFiles, self.courseNumber, self.curso,
            self.gridNumber)

        if not self.fileExist(aux):
            self.to_xml.clear()
            self.to_xml.create_tag('gridNumber', '')
            self.to_xml.create_tag('Curso', self.curso)
            self.to_xml.create_tag('Ano', self.ano)
            # It counts all disciplines, i.e., 'Optional' and 'Obrigatory'
            self.to_xml.create_tag('NDisciplinas',
                                   str(len(self.cname_cod)))

            self.to_xml.create_tag('Disciplinas', '')
            for cod, nome, per in zip(self.cname_cod,
                                      self.cname_n, self.cname_p):
                self.to_xml.create_tag('Disciplina', '')

                self.to_xml.create_tag('Nome', nome)
                self.to_xml.create_tag('Sigla', cod)
                self.to_xml.create_tag('Periodo', per)

                if cod in self.cname_pre and self.cname_pre[cod]:
                    self.to_xml.create_tag('PreRequisitoTotal', '')
                    for j in self.cname_pre[cod]:
                        self.to_xml.create_tag('Sigla', j)
                    self.to_xml.end_tag()

                if cod in self.cname_co and self.cname_co[cod]:
                    self.to_xml.create_tag('CoRequisito', '')
                    for j in self.cname_co[cod]:
                        self.to_xml.create_tag('Sigla', j)
                    self.to_xml.end_tag()

                self.to_xml.end_tag()  # End disciplina
            self.to_xml.end_tag()  # End disciplinaS
            self.to_xml.end_tag()  # End gridNumber

            ll = self.__folder_xmlFiles + '{}_{} - {}.xml'.format(
                self.courseNumber, self.curso, self.ano)

            self.to_xml.toFile(ll)
            self.log.write('[xml_Grid]: Success!\n')
        else:
            self.log.write('[xml_Grid]: Failure! File already exist\n')


# =============================================================================
# History
# =============================================================================

    def get_History(self, *argv):
        """ Set the history. This method assumes that
        you did login with student account.\n
        You can pass argument 'xml' to generate file when finish."""
        # Header's info
        try:
            self.curso = self.chrome_webdriver.find_element_by_css_selector(
                '#agenda-docente>table>tbody>tr:nth-child(2)>\
                td:nth-child(2)').text
            self.matricula =\
                self.chrome_webdriver.find_element_by_css_selector(
                    '#agenda-docente>table>tbody>tr:nth-child(1)>td:nth-of-\
                type(2)').text
            self.initialYearNumber = \
                self.chrome_webdriver.find_element_by_css_selector('#agenda-\
                docente>table>tbody>tr:nth-child(6)>td:nth-child(2)').text

            aux = self.__folder_xmlFiles + \
                'historico_{}.xml'.format(self.matricula)

            # If file exist, cancel search
            if self.fileExist(aux):
                self.log.write('[get_History]: Failure! File already exist')
                return False
            else:
                self.log.write('[get_History]->HeadersInfo: Success!\n')
        except Exception as ex:
            self.log.write('[get_History]->HeadersInfo: Failure! {}: {}!\n'
                           .format(type(ex).__name__, ex.args))

        # Create basis with (Nome, sigla, CH, Turma)
        try:
            self.chrome_webdriver.get(self.__url_discipline)
            soup = BeautifulSoup(self.chrome_webdriver.page_source, 'html5lib')
            soup = soup.find('table', class_='listagem')

            for i in soup.find_all('tr'):  # , class_='linhaPar'):
                # escape from tr' that are not importants to us
                if i.get('class') is None or i.get('class')[0] == 'destaque':
                    continue
                itsigla = i.find('td').text
                itnome = itsigla[itsigla.find(' - ') + 3:]
                itsigla = itsigla[:itsigla.find(' -')]
                periodo = (i.find_previous('td', class_='periodo').text)
                itturma = i.find_next('td').find_next('td').text
                ch = (i.find_next('td').find_next(
                    'td').find_next('td')).text[:-1]

                if (periodo not in self.history):
                    self.history[periodo] = {
                        itsigla: {
                            'nome': itnome,
                            'turma': itturma,
                            'ch': ch
                        }
                    }

                else:
                    self.history[periodo].update({
                        itsigla: {
                            'nome': itnome,
                            'turma': itturma,
                            'ch': ch
                        }
                    })
            self.log.write('[get_History]->Basis: Success!\n')
        except Exception as ex:
            self.log.write('[get_History]->Basis: Failure! {}: {}!\n'.format(
                type(ex).__name__, ex.args))

        # Adding info to history (notas, faltas, situacao)
        try:
            # acessa as notas pela func cmItemMouseup
            self.chrome_webdriver.get(self.__url_default)
            # script encontrado que gerou a página
            js_script = "try{cmItemMouseUp('menu_form_menu_discente_j_id_jsp_\
                275447739_49_menu',1);}catch(e){}"
            self.chrome_webdriver.execute_script(js_script)
            soup = BeautifulSoup(self.chrome_webdriver.page_source, 'html5lib')
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

                periodo = regex.sub('\s', '', i.find_previous('caption').text)

                # considera apenas materias (exclui resultado dos blocos)
                if (sigla in self.history[periodo]):
                    self.history[periodo][sigla].update({
                        'resultado': resultado,
                        'faltas': faltas,
                        'situacao': situacao
                    })

            self.log.write('[get_History]->InfosHistory: Success!\n')
        except Exception as ex:
            self.log.write('[get_History]->InfosHistory: Failure! {}: {}!\n\
                           '.format(type(ex).__name__, ex.args))

        # verifica se o arquivo do history(pdf) existe na temp
        # Senao, baixa
        aux = self.__folder_temp + 'historico_{}.pdf'.format(self.matricula)
        if not self.fileExist(aux):
            self.chrome_webdriver.get(self.__url_default)
            # script encontrado que gerou a página
            js_script = "try{cmItemMouseUp('menu_form_menu_discente_j_id_jsp_\
                275447739_49_menu',4);}catch(e){}"
            self.chrome_webdriver.execute_script(js_script)

        # PDF (Getting grid and currently period)
        try:
            pt = textract.process(
                '{}historico_{}.pdf'.format(
                    self.__folder_temp, self.matricula),
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
            self.gridNumber = ''.join(
                [i for i in pt[search:pt.find('\n', search)] if i.isdigit()])
            search = pt.find('Período Letivo Atual:\n') + 22
            self.actualYearNumber = pt[search:pt.find('\n', search)]

            self.log.write('[get_History]->PDF: Success!\n')
        except Exception as ex:
            self.log.write('[get_History]->PDF: Failure! {}: {}!\n'.format(
                type(ex).__name__, ex.args))

        # GENERATE XML
        if argv[0] == 'xml':
            self.xml_History()

    def xml_History(self):
        """ Generate xml history file """
        aux = self.__folder_xmlFiles + \
            'historico_{}.xml'.format(self.matricula)

        def incrementyear(s): return (str(int(s[:-2]) + 1) + '.1')

        def incrementsem(s): return (s[:-1] + '2')

        # incrementa semestralmente
        def aplus(s): return (incrementyear(
            s) if s[-1] == '2' else incrementsem(s))

        nano = self.initialYearNumber
        for i in range(1, int(self.actualYearNumber)):
            nano = aplus(nano)
        # muda para que apareca o ano no estilo 20XX.Y ao invés de K
        self.actualYearNumber = nano

        if not self.fileExist(aux):
            self.to_xml.clear()
            self.to_xml.create_tag('HistoricoCurricular', '')
            self.to_xml.create_tag('Curso', self.curso)
            self.to_xml.create_tag('gridNumber', self.gridNumber)
            self.to_xml.create_tag('Matricula', self.matricula)
            self.to_xml.create_tag('initialYearNumber', self.initialYearNumber)
            self.to_xml.create_tag('actualYearNumber', self.actualYearNumber)
            self.to_xml.create_tag('Semestre', '')

            # usado para calcular a frequencia
            def freq(c, s): return str(round((int(c)-int(s))/int(c)*100))

            semestre = self.initialYearNumber
            while True:  # Do ...while
                self.to_xml.create_tag('A{}'.format(semestre), '')
                for sigla in self.history[semestre]:
                    self.to_xml.create_tag('Disciplina', '')
                    self.to_xml.create_tag(
                        'Nome', self.history[semestre][sigla]['nome'])
                    self.to_xml.create_tag('Sigla', sigla)
                    self.to_xml.create_tag('Frequencia', freq(
                        self.history[semestre][sigla]['ch'],
                        self.history[semestre][sigla]['faltas']))
                    self.to_xml.create_tag(
                        'Nota', self.history[semestre][sigla]['resultado'])
                    self.to_xml.create_tag(
                        'CH', self.history[semestre][sigla]['ch'])
                    self.to_xml.create_tag(
                        'Situacao', self.history[semestre][sigla]['situacao'])
                    self.to_xml.end_tag()  # Fim disciplina
                self.to_xml.end_tag()  # fim A`periodo`

                if (semestre == self.actualYearNumber):
                    break
                semestre = aplus(semestre)
            self.to_xml.end_tag()  # Semestre
            self.to_xml.end_tag()  # HistoricoCurricular

            try:
                self.to_xml.toFile(aux)
                self.log.write('[xml_History]: Success!\n')
            except Exception as ex:
                self.log.write('[xml_History]: Failure! {}: {}\n'.format(
                    type(ex).__name__, ex.args))
        else:
            self.log.write('[xml_History]: Failure! File already exist\n')
