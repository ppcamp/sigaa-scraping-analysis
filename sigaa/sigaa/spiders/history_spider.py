import scrapy
from scrapy.utils.response import open_in_browser

import re
from ..items import SigaaItem

class SigaaSpider(scrapy.Spider):
    # The sigaa system it's an Ajax, so
    #   - Need to get screen state of user
    #   - Modal panels etc

    name = "history"
    start_urls = ["https://sigaa.unifei.edu.br/sigaa/logar.do?dispatch=logOn"]

    def parse(self, response):
        # Executed when get response of start_urls
        # variable to save informations scrapped
        self.items = SigaaItem()

        # Login into Sigaa
        self.logger.critical("Login page loaded sucessfully")
        yield scrapy.FormRequest(
            url = SigaaSpider.start_urls[0],
            formdata = {
                "user.login":self.user,
                "user.senha":self.pswd
            }, callback=self.home_screen,
        )


    def home_screen(self, response):
        # response = home screen
        self.logger.critical("Logged successfully.")

        # Get Basic infos
        self.items['CourseName'] = response.xpath('//*[@id="agenda-docente"]//tr[2]/td[2]/text()').get()
        self.items['CourseName'] = re.sub('\t', '', self.items['CourseName']) # Remove extra spaces
        self.items['CourseName'] = self.items['CourseName'].replace('\n',' ')[1:-2] # //
        self.items['CurrentYearPeriod'] = response.xpath('//*/p[1]/strong/text()').get()
        self.items['StartYearPeriod'] = response.xpath('//*/tr[6]/td[2]/text()').get()[1:]
        self.items['RA'] = response.xpath('//*[@id="agenda-docente"]//tr[1]/td[2]/text()').get()[1:-1]

        # Get hidden keys
        id = response.xpath('//*[@name="id"]/@value').get()
        viewstate = response.xpath('//*[@name="javax.faces.ViewState"]/@value').get()
    
        # Make request to get student notes
        yield scrapy.FormRequest(
            url = "https://sigaa.unifei.edu.br/sigaa/portais/discente/discente.jsf",
            formdata = {
                "menu:form_menu_discente": "menu:form_menu_discente",
                "id": id,
                "jscook_action": "menu_form_menu_discente_j_id_jsp_512348736_98_menu:A]#{ relatorioNotasAluno.gerarRelatorio }",
                "javax.faces.ViewState": viewstate
            }, callback=self.student_score,
        )
    

    def student_score(self, response):
        # response = score screen
        # open_in_browser(response)
        self.logger.critical("Score got with success")
        
        # Create "headers" for dicts
        _p = response.xpath('//td[1]/../../../caption/text()').getall()
        _p = [re.sub('\t|\n', '', i) for i in _p] # Remove extra spaces
        # Create semesters dict — Needed, after all, we update dict (not overlaping the olders)
        self.items['Semester'] = {}
        for i in _p:
            self.items['Semester'][i] = {}
        
        for i in response.xpath('//tr[@*]'):
            # Abbrev
            _a = i.xpath('./td[1]/text()').get()
            # Discipline name
            _n = re.sub('\t\n', '', i.xpath('./td[2]/text()').get()) # Remove extra spaces
            # Scores
            _s = re.sub('\t| |\n', '', i.xpath('./td[6]/text()').get()) # Remove extra spaces
            # Fouls
            _f = re.sub('\t| |\n', '', i.xpath('./td[7]/text()').get()) # Remove extra spaces
            # Situation
            _st = i.xpath('./td[8]/text()').get()
            # Period
            _p = re.sub(' |\n|\t', '', i.xpath('./td[1]/../../../caption/text()').get() )

            self.items['Semester'][_p].update({
                _a : {
                    'Name':_n,
                    'Score':_s,
                    'Fouls':_f,
                    'Situation':_st
                }
            })

        # Get student's classes
        yield scrapy.FormRequest(
            url = "https://sigaa.unifei.edu.br/sigaa/portais/discente/turmas.jsf", 
            callback=self.student_classes,
        )


    def student_classes(self, response):
        # response = classes screen
        self.logger.critical("Classes got with success")

        _p = ""
        for i in response.xpath('//tr[@class="linhaPar" or @class="linhaImpar" or @class="destaque no-hover"]'):
            # Check if it's a td with period
            if 'destaque no-hover' == i.xpath('./@class').get():
                _p = i.xpath('./td/text()').get()
                continue # Force to go to the next one
            # Abbrev
            _aux = i.xpath('./td[1]')
            _a = _aux.xpath('./text()').get()
            _a = _a[: _a.find(' ')] # Get only abbreviation
            # Class
            _c = i.xpath('./td[2]/text()').get()
            # Hours
            _h = i.xpath('./td[3]/text()').get()
            
            # self.logger.critical('V: |{}|\t|{}|{}|{}|'.format(_p,_a,_c,_h))
            self.items['Semester'][_p][_a].update({
                'Class': _c,
                'Hours':_h
            })

        # Returning dict
        yield self.items