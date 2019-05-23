# ==============================================================
# sigaaBase (login and window)
# ==============================================================

class sigaaBase(object):
    """
    Class used to do scraping from
    UNIFEI's SIGAA system.
    """
    # Imports
    # ===============================================
    # ENTER key
    from selenium.webdriver.common.keys import Keys
    # Webdriver used for automatization
    from selenium import webdriver
    # logFile
    from datetime import datetime
    # Current dir
    from os.path import abspath
    # Parser and tree for html
    from bs4 import BeautifulSoup
    # ================================================

    _url_login = "https://sigaa.unifei.edu.br/sigaa/verTelaLogin.do"
    _url_component = "https://sigaa.unifei.edu.br/sigaa/geral/componente\
_curricular/busca_geral.jsf"
    _url_grid = "https://sigaa.unifei.edu.br/sigaa/geral/estrutura\
_curricular/busca_geral.jsf"
    _url_discipline = "https://sigaa.unifei.edu.br/sigaa/portais/discente/\
turmas.jsf"
    _url_default = "https://sigaa.unifei.edu.br/sigaa/portais/discente/\
discente.jsf"

    _folder_project = abspath('') + '/'
    _folder_webdriver = _folder_project + 'webdriver/chromedriver'
    _folder_temp = _folder_project + '.temp_files/'
    _folder_xmlFiles = _folder_project + 'xml_files/'
    _folder_logs = _folder_project + 'logs/'

    def __init__(self, **kwargs):
        self._courseCode = '0192015'  # ECO-2015.1 by default
        self._userName = ''
        self._userPsswd = ''

        # Webdriver
        self.chrome_options = self.webdriver.ChromeOptions()
        # default location for linux
        self.chrome_options.binary_location = "/usr/bin/google-chrome"
        # path to chromedriver
        self.chrome_webdriver_path = self._folder_project + \
            '/webdriver/chromedriver'
        # set folder to '.temp_files' in project folder
        self.chrome_options.add_experimental_option(
            "prefs",
            {
                'download.default_directory': self._folder_temp,
                'download.prompt_for_download': False
            }
        )
        # Pass headless=True to hide the window
        if(kwargs):
            if (('headless' in kwargs) and kwargs['headless']):
                self.chrome_options.add_argument('--headless')
        # Window
        self._chrome_webdriver = self.webdriver.Chrome(
            executable_path=self.chrome_webdriver_path,
            options=self.chrome_options)

        # LOGFILE
        l = self.datetime.now()
        logName = '{}-{}-{}_{}-{}.txt'.format(l.year,
                                              l.month, l.day, l.hour, l.minute)
        self._logFile = open('{}{}'.format(
            self._folder_logs, logName), 'a', encoding='utf8')

    def set_user(self, userName):
        """
        Set user's system.

        Parameters
        ----------
        _userName: string
            User name used to login in sigaa's system.

        Example
        -------
        >> set_user('123')
        """
        self._userName = userName
        self._logFile.write('[set_user]: Success!\n')

    def set_psswd(self, userPsswd):
        """
        Set password used for user

        Parameters
        ----------
        _userPsswd: string
            User password to login.

        Example
        -------
        >> set_psswd('456')
        """
        self._userPsswd = userPsswd
        self._logFile.write('[set_psswd]: Success!\n')

    def set_codCurso(self, courseCode):
        """
        Set course code

        Parameters
        ----------
        courseCode: string
            Number's course.

        Example
        -------
        >> set_codCurso('0192015')
        """
        self._courseCode = courseCode
        self._logFile.write('[set_codCurso]: Success!\n')

    def quit_webdriver(self):
        """
        Close window used for autotization.

        Example
        -------
        >> quit_webdriver()
        """
        self._chrome_webdriver.quit()
        self._logFile.write('[Quit_webdriver]: Success!\n')

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
        user= '_userName'
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

        if (not self._userName or not self._userPsswd):
            self._logFile.write(
                '[login]: Failure. It must have an _userName and psswd\n')
            return False

        try:
            # Accessing url
            self._chrome_webdriver.get(self._url_login)

            # Find element
            user_name = self._chrome_webdriver.find_element_by_name(
                "user.login")
            # Clean field
            user_name.clear()
            # Send content to field
            user_name.send_keys(self._userName)

            user_pwd = self._chrome_webdriver.find_element_by_name(
                "user.senha")
            user_pwd.clear()
            user_pwd.send_keys(self._userPsswd)

            user_pwd.send_keys(self.Keys.ENTER)

            if (self._chrome_webdriver.current_url != self._url_default):
                raise Exception('loginError', 'Wrong _userName or password')

            self._logFile.write('[login]: Success!\n')

        except Exception as ex:
            self._logFile.write('[login]: Failure! {}: {}\n'.format(
                type(ex).__name__, ex.args))
