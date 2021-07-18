import scrapy
from scrapy.utils.response import open_in_browser

from ..items import SigaaItem

class SigaaSpider(scrapy.Spider):
    # The sigaa system it's an Ajax, so
    #   - Need to get screen state of user
    #   - Modal panels etc

    # scrapy crawl sigaa -a user="CPF" -a pswd="PASSWORD" -a course="0192015"
    name = "grid"
    start_urls = ["https://sigaa.unifei.edu.br/sigaa/logar.do?dispatch=logOn"]

    def parse(self, response):
        # Executed when get response of start_urls
        # variable to save informations scrapped
        pass 

    #     self.items = SigaaItem()

    #     # Login into Sigaa
    #     self.logger.info("Login page loaded sucessfully")
    #     yield scrapy.FormRequest(
    #         url = SigaaSpider.start_urls[0],
    #         formdata = {
    #             "user.login":self.user,
    #             "user.senha":self.pswd
    #         }, callback=self.getStudentScore,
    #     )


    # def getStudentScore(self, response):
    #     # response = home screen
    #     self.logger.info("Logged successfully.")

    #     # Get Basic infos
    #     self.items['StartYearPeriod'] = response.xpath('//*[@id="agenda-docente"]/table/tbody/tr[6]/td[2]/text()')
    #     self.items['CurrentYearPeriod'] = response.xpath('//*[@id="info-usuario"]/p[1]/strong/text()')
    #     self.items['RA'] = response.xpath('//*[@id="agenda-docente"]/table/tbody/tr[1]/td[2]')
    #     self.items['Grid'] = self.course
    #     self.items['CourseName'] = self.xpath('//*[@id="agenda-docente"]/table/tbody/tr[2]/td[2]/text()').
    #     # Get hidden keys
    #     id = response.xpath('//*[@name="id"]/@value').get()
    #     viewstate = response.xpath('//*[@name="javax.faces.ViewState"]/@value').get()
        
    #     # Make request to get student notes
    #     yield scrapy.FormRequest(
    #         url = "https://sigaa.unifei.edu.br/sigaa/portais/discente/discente.jsf",
    #         formdata = {
    #             "menu:form_menu_discente": "menu:form_menu_discente",
    #             "id": id,
    #             "jscook_action": "menu_form_menu_discente_j_id_jsp_512348736_98_menu:A]#{ relatorioNotasAluno.gerarRelatorio }",
    #             "javax.faces.ViewState": viewstate
    #         }, callback=self.getStudentClasses,
    #     )
    

    # def getStudentClasses(self, response):
    #     # response = score screen
    #     self.logger.info("Score got with success")

    #     # Get student's classes
    #     yield scrapy.FormRequest(
    #         url = "https://sigaa.unifei.edu.br/sigaa/portais/discente/turmas.jsf", 
    #         callback=self.getSearchGridViewState,
    #     )


    # def getSearchGridViewState(self, response):
    #     # response = classes screen
    #     self.logger.info("Classes got with success")

    #     # Go to the page of grid search
    #     yield scrapy.FormRequest(
    #         url = "https://sigaa.unifei.edu.br/sigaa/geral/estrutura_curricular/busca_geral.jsf",
    #         callback=self.searchStudentCurriculum
    #     )

    # def searchStudentCurriculum(self, response):
    #     # response = grid search screen
    #     self.logger.info("Page of curriculum search loaded successfully.")

    #     # Get hidden key
    #     viewstate = response.xpath('//*[@id="javax.faces.ViewState"]/@value').get()

    #     # Make search
    #     yield scrapy.FormRequest(
    #         url ="https://sigaa.unifei.edu.br/sigaa/geral/estrutura_curricular/busca_geral.jsf",
    #         formdata = {
    #             "busca": "busca",
    #             "busca:curso": "0",
    #             "busca:matriz": "0",
    #             "busca:checkCodigo": "on",
    #             "busca:codigo": self.course,
    #             "busca:somenteAtivas": "on",
    #             "busca:j_id_jsp_585368531_679": "Buscar", # checkout later
    #             "javax.faces.ViewState": viewstate
    #         },callback=self.getStudentCurriculum
    #     )
        
    # def getStudentCurriculum(self, response):
    #     # response = grid search screen w/ results
    #     self.logger.info("Curriculum results got successfully")
    #     #open_in_browser(response)

    #     # Get hidden keys
    #     viewstate = response.xpath('//*[@id="javax.faces.ViewState"]/@value').get()
    #     # I believe that id in this case, represents the actual content to search for.
    #     id = response.xpath('//*[@id="resultado:relatorio"]/@onclick').get()
    #     b = id.rfind(":") + 2   # Begin position of id
    #     e = id.rfind("'}")      # Last position of id
    #     self.logger.info("Course id value: {}".format(id[b:e]))

    #     # Get curriculum report
    #     yield scrapy.FormRequest(
    #         url ="https://sigaa.unifei.edu.br/sigaa/graduacao/curriculo/lista.jsf",
    #         formdata = {
    #             "resultado": "resultado",
    #             "javax.faces.ViewState": viewstate,
    #             "resultado:relatorio": "resultado:relatorio",
    #             "id": id[b:e]
    #         },callback=self.getStudentViewCurriculum
    #     )

    # def getStudentViewCurriculum(self, response):
    #     # response = curriculum report screen
    #     self.logger.info("Curriculum grade.")
    #     open_in_browser(response)
