# -*- coding: utf-8 -*-

"""
This module is responsable to open the sigaa system and then scrapy if don't find the course in mongodb database.

Todo
----
Missing loggers for:

- :meth:`scrapping_grid`
"""


# Debug
# from IPython.core.display import display, HTML
# Handle cookie and requests
from typing import Tuple
from networkx.classes.digraph import DiGraph
from requests import Session
# Parse html file
from lxml import html
# Loads the credentials file
from json import load
# Replace empowering
import re
# Conver string to dict
import json
# Graph
import networkx as nx


def scrapping_grid(courseCode: str) -> Tuple[DiGraph, DiGraph]:
    """
    Load the credentials under `src/certs/credentials.json` file,
    logon into sigaa's system and then, scrap it, retriving a new graph to a certain
    grid string

    Args
    ----
    `courseCode`:
        Course number, e.g, "0192015"

    Returns
    -------
    Tuple[DiGraph, DiGraph]
        A tuple with (pre,co) requisite graphs equivalents to this courseCode

    Note
    ----
    We only add the graph the connection

    Caution
    -------
    This graph ain't check for equivalency. It means that when using student's history, you'll problably need to check for equivalency too.
    """
    # Load credentials json
    with open('./certs/credentials.json') as file:
        credentials = load(file)

    # URL's used in scrapping
    urls = {
        'Login': 'https://sigaa.unifei.edu.br/sigaa/logar.do?dispatch=logOn',
        'Main': 'https://sigaa.unifei.edu.br/sigaa/portais/discente/discente.jsf',
        'SearchResult': 'https://sigaa.unifei.edu.br/sigaa/geral/estrutura_curricular/busca_geral.jsf',
        'SearchList': 'https://sigaa.unifei.edu.br/sigaa/graduacao/curriculo/lista.jsf',
        'Component': 'https://sigaa.unifei.edu.br/sigaa/geral/componente_curricular/busca_geral.jsf'
    }

    # Create a graph
    Graph: DiGraph = nx.DiGraph()

    #S = Session()
    with Session() as S:
        # *  Login into system
        loginConfig = {
            "width": "1366",
            "height": "768",
            "urlRedirect": "",
            "subsistemaRedirect": "",
            "acao": "",
            "acessibilidade": ""
        }
        r = S.post(urls['Login'], {**credentials, **loginConfig}).text

        # Get hidden inputs
        tree = html.fromstring(r)
        data = {
            "menu:form_menu_discente": "menu:form_menu_discente",
            "id": tree.xpath('//*[@id="menu:form_menu_discente"]/input[@name="id"]'),
            "jscook_action": tree.xpath('//*[@id="menu:form_menu_discente"]/div/@id')[0] + ':A]#{ curriculo.popularBuscaGeral }',
            "javax.faces.ViewState": tree.xpath('//*[@id="menu:form_menu_discente"]/input[@name="javax.faces.ViewState"]/@value')[0],
        }

        # Going to searching grid page
        r = S.post(urls['Main'], data).text

        # Get hidden inputs
        tree = html.fromstring(r)
        data = {
            "busca": "busca",
            "busca:curso": "0",
            "busca:matriz": "0",
            "busca:checkCodigo": "on",
            "busca:codigo": courseCode,
            "{}".format(tree.xpath('//*[@value="Buscar"]/@name')[0]): "Buscar",
            "javax.faces.ViewState": tree.xpath('//*[@name="javax.faces.ViewState"]/@value')[0]
        }

        # Does the search
        r = S.post(urls['SearchResult'], data).text
        r = S.get(urls['SearchList']).text
        # Get hidden infos
        tree = html.fromstring(r)

        # iF grid didn't exist, throw error
        try:
            id = tree.xpath('//*[@id="resultado"]//input[1]/@value')[1]
        except Exception as err:
            raise Exception(f'The grid {courseCode} wasn\'t found.')

        data = {
            "resultado": "resultado",
            "{}".format(tree.xpath('//*[@id="resultado"]//input[1]/@name')[1]): id,
            "javax.faces.ViewState": tree.xpath('//*[@id="javax.faces.ViewState"]/@value')[0],
            "resultado:relatorio": 'resultado:relatorio',
            "id": id
        }

        # Get grid output
        r = S.post(urls['SearchList'], data).text

        # * Get grid
        # Add nodes in graph
        # Create Tree
        tree = html.fromstring(r)

        # List all lists all school subjects and description also (period or optional or complementary)
        for it in tree.xpath('//*[@class="componentes" or @class="tituloRelatorio"]'):
            # Filter: Check if is a divider or a row itself (class or period)
            if it.xpath('@class')[0] == 'tituloRelatorio':
                # Get period
                period: str = it.find('td').text
                # Removing spaces
                period: str = re.sub(r'[\t\n]', '', period)
                # Change the text
                if period == 'Componentes Optativos':
                    period = 'Optativa'
                elif period == 'Componentes Complementares':
                    period = 'Complementar'
                else:
                    # Get number only
                    period: str = period[:period.find('º')].strip()
                # skip to avoid programming issues
                continue

            # Get the code of the initials of grid class
            initials = it.findall('td')[0].text

            # Get class name
            className = it.findall('td')[1].text
            # Get the amount of hours in the classroom
            time = it.findall('td')[2].xpath('text()')[0]
            # Get the amount of hours in laboratory
            labTime = it.findall('td')[2].xpath('text()')[1]

            # Removing extra chars
            # Removing spaces
            className = re.sub(r'[\t\n]', '', className)
            labTime = re.sub(r'[\t\n]', '', labTime)
            time = re.sub(r'[\t\n]', '', time)
            # Removing extra information 'bout time spent in this class
            className = className[:className.rfind(' - ')]
            # Getting only the number that represents the max hours spent
            labTime = labTime[:labTime.find('h')]
            time = time[:time.find('h')]
            # Fix a problem with char "" --> '-'
            className = className.replace('', '-')

            # Debugging
            # print(f'Periodo: |{period}|\t Sigla: |{initials}|\tNome: |{className}|')

            # Add into graph
            Graph.add_node(initials,
                           # Create a node with those extra informations
                           period=period,  # type: ignore
                           className=className,
                           # Laboratory (Practical and Theory)
                           time=time,
                           labTime=labTime)

        # * Create a graph for pre and co requisite
        GraphCoReq: DiGraph = Graph.copy()  # type:ignore
        GraphPreReq: DiGraph = Graph

        # * Get edges
        # Search for pre and co requisite. They will be used to generate two graphs of connections
        # Iterate over graph elements
        for initials, data in GraphPreReq.nodes(data=True):  # type: ignore
            # Skip if is a optional discipline
            if data['period'] == 'Optativa':
                continue
            # Otherwise...

            # Debugging:
            # print(f'Key: {initials}, period: {data["period"]}')

            # Goes to main page
            r = S.get(urls['Main']).text

            # Get hidden infos
            tree = html.fromstring(r)
            data = {
                'menu:form_menu_discente': 'menu:form_menu_discente',
                'id': tree.xpath('//*[@id="menu:form_menu_discente"]/input[@name="id"]/@value')[0],
                'jscook_action': tree.xpath('//*[@id="menu:form_menu_discente"]/div/@id')[0] + ':A]#{ componenteCurricular.popularBuscaDiscente }',
                'javax.faces.ViewState': tree.xpath('//*[@name="javax.faces.ViewState"]/@value')[0]
            }

            # Goes to search page
            r = S.post(urls['Main'], data).text

            # Get hidden infos
            tree = html.fromstring(r)
            data = {
                'formBusca': 'formBusca',
                'formBusca:checkNivel': 'on',
                'formBusca:checkCodigo': 'on',
                'formBusca:form:idPreRequisito': '',
                'formBusca:form:nomeDisciplinaPreRequisito': '',
                'formBusca:form2:idCoRequisito': '',
                'formBusca:form2:nomeDisciplinaCoRequisito': '',
                'formBusca:form3:idEquivalencia': '',
                'formBusca:form3:nomeDisciplinaEquivalencia': '',
                'formBusca:Data_Inicial': '',
                'formBusca:dataFim': '',
                'formBusca:unidades': '0',
                'formBusca:tipos': '0',
                'formBusca:modalidades': '0',
                'formBusca:btnBuscar': 'Buscar',
                tree.xpath('//*[@name="formBusca"]/table/tbody/tr[1]/td[3]/select/@name')[0]: 'G',
                tree.xpath('//*[@name="formBusca"]/table/tbody/tr[2]/td[3]/input/@name')[0]: initials,
                tree.xpath('//*[@name="formBusca"]/table/tbody/tr[3]/td[3]/input/@name')[0]: '',
                'javax.faces.ViewState': tree.xpath('//*[@name="javax.faces.ViewState"]/@value')[0]
            }

            # Search for this initial
            r = S.post(urls['Component'], data).text

            # Get hidden infos
            tree = html.fromstring(r)
            formName = tree.xpath(
                '//table[starts-with(@class,"listagem")]//form/@name')[0]
            link = tree.xpath(
                '//a[@title="Relatório para impressão"]/@onclick')[0]
            data = json.loads(
                link[link.rfind('{'):link.find('}')+1].replace('\'', '\"'))
            data[formName] = formName
            data['javax.faces.ViewState'] = tree.xpath(
                '//*[@name="javax.faces.ViewState"]/@value')[0]

            # Goes to response page
            r = S.post(urls['Component'], data).text

            # Extracting infos
            tree = html.fromstring(r)

            # Get Pre requisite (list)
            preRequisite = tree.xpath(
                '//th[text()[contains(.,"Pré-Requisitos:")]]/following-sibling::td/acronym/text()')
            # Get Co requisite (list)
            coRequisite = tree.xpath(
                '//th[text()[contains(.,"Co-Requisitos:")]]/following-sibling::td/acronym/text()')

            # Check if element is a node, if so, create graph
            for i in preRequisite:
                # If element is present in graph
                if i in GraphPreReq:
                    # Create edges
                    GraphPreReq.add_edge(i, initials)
            for i in coRequisite:
                # If element is present in graph
                if i in GraphCoReq:
                    # Create edges
                    GraphCoReq.add_edge(i, initials)

    return GraphPreReq, GraphCoReq
