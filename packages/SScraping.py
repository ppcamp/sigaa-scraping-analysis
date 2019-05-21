""" @package SScraping
This package have the classes needed to get
Sigaa scraping
"""

# Imports
# ------------------------------------------------------
# expressao regular para strings (limpeza de \t\n)
import re as regex
# diretorio atual
from os.path import abspath

# necessário para trabalhar com o html
from bs4 import BeautifulSoup
# automatiza nova guia do navegador em plano de fundo
from selenium import webdriver
# Tecla ENTER
from selenium.webdriver.common.keys import Keys

# pdf
import textract
# classe criada para gerar o XML

# log
from datetime import datetime


# Class
# ------------------------------------------------------
class BasicXml(object):
    """ Class used to create a basic parsed XML file.

    This class creates a string that contains the file
    with special chars '[\t\n]', in anoter words,
    a parsed document
    """

    __out__ = '<?xml version="1.0" encoding="UTF-8"?>\n'
    __stack__ = []

    def __indent__(self):
        """ Used to parse tags"""
        return '\t'*len(self.__stack__)

    def create_tag(self, tagname, value):
        """ Create a new tag
        @param tagname Name desired for xml's tags.
        @param value Value to be placed inside,an empty value '', means that will have a break
        """
        self.__out__ += self.__indent__() + '<{}>'.format(tagname)
        self.__stack__.append(tagname)

        if value == '':
            self.__out__ += '\n'
        else:
            self.__out__ += value
            self.end_tag()

    def end_tag(self):
        """ Pop's out from stack, and close last tag"""
        tagname = self.__stack__.pop()
        if self.__out__[-1] == '\n':
            self.__out__ += self.__indent__()
        self.__out__ += '</{}>\n'.format(tagname)

    def __init__(self):
        """Ctr for this class, it clears the env variables when called"""
        self.clear()

    def getXml(self):
        """ Return XML string"""
        return self.__out__

    def clear(self):
        """ Clear environment variables"""
        self.__out__ = '<?xml version="1.0" encoding="UTF-8"?>\n'
        self.__stack__.clear()

    def toFile(self, name):
        """ Create XML file
        You must pass a name containing path to file."""

        f = open(name, 'w', encoding='utf-8')

        if not f.closed:
            f.write(self.getXml())
            f.close()
            return True
        else:
            return False
# ------------------------------------------------------


class SScraping(object):
    """ Class used to do scraping from
    UNIFEI's SIGAA system """

    __url_login__ = "https://sigaa.unifei.edu.br/sigaa/verTelaLogin.do"
    __url_componente__ = "https://sigaa.unifei.edu.br/sigaa/geral/componente_curricular/busca_geral.jsf"
    __url_grade__ = "https://sigaa.unifei.edu.br/sigaa/geral/estrutura_curricular/busca_geral.jsf"
    __url_turma__ = "https://sigaa.unifei.edu.br/sigaa/portais/discente/turmas.jsf"
    __url_default__ = "https://sigaa.unifei.edu.br/sigaa/portais/discente/discente.jsf"

    __pasta_projeto__ = abspath('') + '/'
    __pasta_webdriver__ = __pasta_projeto__ + 'webdriver/chromedriver'
    __pasta_temp__ = __pasta_projeto__ + '.temp_files/'
    __pasta_xml_files__ = __pasta_projeto__ + 'xml_files/'
    __pasta_logs__ = __pasta_projeto__ + 'logs/'

    def __init__(self, **kwargs):
        self.codCurso = '0192015'  # Retorna ECO-2015.1 por padrão
        self.userName = ''
        self.userPsswd = ''
        self.grade = ''
        self.anoperiodoatual = ''  # obtem no pdf
        self.anoperiodoinicial = ''  # obtem no pdf
        self.curso = ''

        # Grid
        self.cname_cod = []
        self.cname_p = []
        self.cname_n = []
        self.cname_pre = {}
        self.cname_co = {}

        # History
        self.historico = {}

        # Webdriver
        # variavel de opcoes
        self.chrome_options = webdriver.ChromeOptions()
        # default for linux
        self.chrome_options.binary_location = "/usr/bin/google-chrome"
        # caminho do arquivo chromedriver
        self.chrome_webdriver_path = self.__pasta_projeto__ + \
            '/webdriver/chromedriver'
        # configura o chrome para salvar na pasta '.temp_files' do projeto,
        self.chrome_options.add_experimental_option(
            "prefs",
            {
                'download.default_directory': self.__pasta_temp__,
                'download.prompt_for_download': False
            }
        )
        # Passe headless=True para ocultar a janela
        if(kwargs):
            if (('headless' in kwargs) and kwargs['headless']):
                self.chrome_options.add_argument('--headless')
        # Window
        self.chrome_webdriver = webdriver.Chrome(
            executable_path=self.chrome_webdriver_path, options=self.chrome_options)

        # LOGFILE
        l = datetime.now()
        logName = '{}-{}-{}_{}-{}.txt'.format(l.year,
                                              l.month, l.day, l.hour, l.minute)
        self.log = open('{}{}'.format(
            self.__pasta_logs__, logName), 'a', encoding='utf8')

        # XML OUTPUT
        self.to_xml = BasicXml()

    def set_user(self, userName):
        """ Set user's system """
        self.userName = userName
        self.log.write('[set_user]: Success!\n')

    def set_psswd(self, userPsswd):
        """ Set password used for user """
        self.userPsswd = userPsswd
        self.log.write('[set_psswd]: Success!\n')

    def set_codCurso(self, codCurso):
        """ Set course code """
        self.codCurso = codCurso
        self.log.write('[set_codCurso]: Success!\n')

    def set_chromeBinary(self, binLoc):
        """ Set location for chrome binary location
            by default, the value is used for default
            *.deb install
        """
        self.chrome_options.binary_location = binLoc
        self.log.write('[set_chromeBinary]: Success!\n')

    def quit_webdriver(self):
        """ Close window used for autotization """
        self.chrome_webdriver.quit()
        self.log.write('[Quit_webdriver]: Success!\n')

    def fileExist(self, name):
        """ Check if XML file exist
        You must pass a name with path to file'"""

        try:
            f = open(name, 'r')
            f.close()
            return True
        except:
            return False

    def login(self, **kwargs):
        """ Try to login in Unifei's sigaa
        user='UserName'
        password='Password'sUser'
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
            # acessando url
            self.chrome_webdriver.get(self.__url_login__)

            # encontra elemento
            user_name = self.chrome_webdriver.find_element_by_name(
                "user.login")
            # limpa o campo
            user_name.clear()
            # envia o conteudo de name para o campo
            user_name.send_keys(self.userName)

            user_pwd = self.chrome_webdriver.find_element_by_name("user.senha")
            user_pwd.clear()
            user_pwd.send_keys(self.userPsswd)

            user_pwd.send_keys(Keys.ENTER)

            if (self.chrome_webdriver.current_url != self.__url_default__):
                raise Exception('loginError', 'Wrong username or password')

            self.log.write('[login]: Success!\n')

        except Exception as ex:
            self.log.write('[login]: Failure! {}: {}\n'.format(
                type(ex).__name__, ex.args))

    def get_Grid(self, *argv):
        # Buscando Grade
        try:
            self.chrome_webdriver.get(self.__url_grade__)
            self.chrome_webdriver.find_element_by_id('busca:codigo').clear()
            self.chrome_webdriver.find_element_by_id(
                'busca:checkCodigo').click()
            box = self.chrome_webdriver.find_element_by_id('busca:codigo')
            box.send_keys(self.codCurso)
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
            # Montando Dicionarios
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
            # for i, j, k in zip(self.cname_cod, self.cname_n, self.cname_p):
            #     print(i, k, j)

            # Busca pre requisito
            for i, j in zip(self.cname_cod, self.cname_p):
                # Dessa forma NÃO procura pre e co para
                # materias optativas
                if j == "Optativa":
                    continue

                self.chrome_webdriver.get(self.__url_componente__)
                self.chrome_webdriver.find_element_by_name(
                    'formBusca:checkCodigo').click()

                box = self.chrome_webdriver.find_element_by_name(
                    'formBusca:j_id_jsp_433775776_860')
                box.clear()
                box.send_keys(i)
                box.send_keys(Keys.ENTER)  # shows 'listagem'

                # Bloco
                box = self.chrome_webdriver.find_elements_by_xpath(
                    '//a[@title=\'Relatório para impressão\' ]')
                if len(box) == 3:
                    box[1].click()
                elif len(box) == 1:
                    box[0].click()

                pre = (self.chrome_webdriver.find_element_by_xpath(
                    '//th[text()[contains(.,\'Pré-Requisitos:\')]]/following-sibling::td')).text
                co = (self.chrome_webdriver.find_element_by_xpath(
                    '//th[text()[contains(.,\'Co-Requisitos:\')]]/following-sibling::td')).text
                # Tamanho minimo é a palavra OU
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
        """ Generate XML grid file """
        aux = '{}{}_{} - {}.xml'.format(
            self.__pasta_xml_files__, self.codCurso, self.curso, self.grade)

        if not self.fileExist(aux):
            self.to_xml.clear()
            self.to_xml.create_tag('Grade', '')
            self.to_xml.create_tag('Curso', self.curso)
            self.to_xml.create_tag('Ano', self.ano)
            self.to_xml.create_tag('NDisciplinas',
                                   str(len(self.cname_cod)))  # considera todas as disciplinas oferecidas

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

                # if len(codes_names[i]['parciais']) > 0:
                #     to_xml.create_tag('PreRequisitoParcial','')
                #     for j in codes_names[i]['parciais']:
                #         to_xml.create_tag('Sigla',j)
                #     to_xml.end_tag()

                if cod in self.cname_co and self.cname_co[cod]:
                    self.to_xml.create_tag('CoRequisito', '')
                    for j in self.cname_co[cod]:
                        self.to_xml.create_tag('Sigla', j)
                    self.to_xml.end_tag()

                self.to_xml.end_tag()  # Fim da tag disciplina
            self.to_xml.end_tag()  # fim da tag disciplinaS
            self.to_xml.end_tag()  # fim da tag Grade

            ll = self.__pasta_xml_files__ + \
                '{}_{} - {}.xml'.format(self.codCurso, self.curso, self.ano)

            self.to_xml.toFile(ll)
            self.log.write('[xml_Grid]: Success!\n')
        else:
            self.log.write('[xml_Grid]: Failure! File already exist\n')

    def get_History(self, *argv):
        """ Set the history. This method assumes that
        you did login with student account.\n
        You can pass argument 'xml' to generate file when finish."""
        # Header's info
        try:
            self.curso = self.chrome_webdriver.find_element_by_css_selector(
                '#agenda-docente > table > tbody > tr:nth-child(2) > td:nth-child(2)').text
            self.matricula = self.chrome_webdriver.find_element_by_css_selector(
                '#agenda-docente > table > tbody > tr:nth-child(1) > td:nth-of-type(2)').text
            self.anoperiodoinicial = self.chrome_webdriver.find_element_by_css_selector(
                '#agenda-docente > table > tbody > tr:nth-child(6) > td:nth-child(2)').text

            aux = self.__pasta_xml_files__ + \
                'historico_{}.xml'.format(self.matricula)

            # If file exist, cancel search
            if self.fileExist(aux):
                self.log.write('[get_History]: Failure! File already exist')
                return False
            else:
                self.log.write('[get_History]->HeadersInfo: Success!\n')
        except Exception as ex:
            self.log.write('[get_History]->HeadersInfo: Failure! {}: {}!\n'.format(
                type(ex).__name__, ex.args))

        # Create basis with (Nome, sigla, CH, Turma)
        try:
            self.chrome_webdriver.get(self.__url_turma__)
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

                if (periodo not in self.historico):
                    self.historico[periodo] = {
                        itsigla: {
                            'nome': itnome,
                            'turma': itturma,
                            'ch': ch
                        }
                    }

                else:
                    self.historico[periodo].update({
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
            self.chrome_webdriver.get(self.__url_default__)
            # script encontrado que gerou a página
            js_script = "try{cmItemMouseUp('menu_form_menu_discente_j_id_jsp_275447739_49_menu',1);}catch(e){}"
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
                if (sigla in self.historico[periodo]):
                    self.historico[periodo][sigla].update({
                        'resultado': resultado,
                        'faltas': faltas,
                        'situacao': situacao
                    })

            self.log.write('[get_History]->InfosHistory: Success!\n')
        except Exception as ex:
            self.log.write('[get_History]->InfosHistory: Failure! {}: {}!\n'.format(
                type(ex).__name__, ex.args))

        # verifica se o arquivo do historico(pdf) existe na temp
        # Senao, baixa
        aux = self.__pasta_temp__ + 'historico_{}.pdf'.format(self.matricula)
        if not self.fileExist(aux):
            self.chrome_webdriver.get(self.__url_default__)
            # script encontrado que gerou a página
            js_script = "try{cmItemMouseUp('menu_form_menu_discente_j_id_jsp_275447739_49_menu',4);}catch(e){}"
            self.chrome_webdriver.execute_script(js_script)

        # PDF (Getting grid and currently period)
        try:
            pt = textract.process(
                '{}historico_{}.pdf'.format(
                    self.__pasta_temp__, self.matricula),
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
            self.grade = ''.join(
                [i for i in pt[search:pt.find('\n', search)] if i.isdigit()])
            search = pt.find('Período Letivo Atual:\n') + 22
            self.anoperiodoatual = pt[search:pt.find('\n', search)]

            self.log.write('[get_History]->PDF: Success!\n')
        except Exception as ex:
            self.log.write('[get_History]->PDF: Failure! {}: {}!\n'.format(
                type(ex).__name__, ex.args))

        # GENERATE XML
        if argv[0] == 'xml':
            self.xml_History()

    def xml_History(self):
        """ Generate xml history file """
        aux = self.__pasta_xml_files__ + \
            'historico_{}.xml'.format(self.matricula)

        def incrementyear(s): return (str(int(s[:-2]) + 1) + '.1')
        def incrementsem(s): return (s[:-1] + '2')
        # incrementa semestralmente
        def aplus(s): return (incrementyear(
            s) if s[-1] == '2' else incrementsem(s))

        nano = self.anoperiodoinicial
        for i in range(1, int(self.anoperiodoatual)):
            nano = aplus(nano)
        # muda para que apareca o ano no estilo 20XX.Y ao invés de K
        self.anoperiodoatual = nano

        if not self.fileExist(aux):
            self.to_xml.clear()
            self.to_xml.create_tag('HistoricoCurricular', '')
            self.to_xml.create_tag('Curso', self.curso)
            self.to_xml.create_tag('Grade', self.grade)
            self.to_xml.create_tag('Matricula', self.matricula)
            self.to_xml.create_tag('AnoPeriodoInicial', self.anoperiodoinicial)
            self.to_xml.create_tag('AnoPeriodoAtual', self.anoperiodoatual)
            self.to_xml.create_tag('Semestre', '')

            # usado para calcular a frequencia
            def freq(c, s): return str(round((int(c)-int(s))/int(c)*100))

            semestre = self.anoperiodoinicial
            while True:  # Do ...while
                self.to_xml.create_tag('A{}'.format(semestre), '')
                for sigla in self.historico[semestre]:
                    self.to_xml.create_tag('Disciplina', '')
                    self.to_xml.create_tag(
                        'Nome', self.historico[semestre][sigla]['nome'])
                    self.to_xml.create_tag('Sigla', sigla)
                    self.to_xml.create_tag('Frequencia', freq(
                        self.historico[semestre][sigla]['ch'],
                        self.historico[semestre][sigla]['faltas']))
                    self.to_xml.create_tag(
                        'Nota', self.historico[semestre][sigla]['resultado'])
                    self.to_xml.create_tag(
                        'CH', self.historico[semestre][sigla]['ch'])
                    self.to_xml.create_tag(
                        'Situacao', self.historico[semestre][sigla]['situacao'])
                    self.to_xml.end_tag()  # Fim disciplina
                self.to_xml.end_tag()  # fim A`periodo`

                if (semestre == self.anoperiodoatual):
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
