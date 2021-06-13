# -*- coding: utf-8 -*-

"""
This module contains some usefull functions to iterate over competencies graphs.

It contains:
- A function to create the competecies graphs
- A function to iterate over these created graphs and calculate the propagated value

Todo
----
Missing loggers for:

- _get_period_classes
- _competence_not_exist_in
- _get_competence_weight
- _generate_competency_graphs
- DFS.generate_graphs
- DFS._get_weight
- DFS.__dfs_walk
- DFS.__dfs_walk
- BFS.generate_graphs
- BFS._get_weight
- BFS.__dfs_walk
- BFS.__dfs_walk


Missing tests for:

- __get_period
- _competence_not_exist_in
- _get_competence_weight
- _generate_competency_graphs
- DFS.generate_graphs
- DFS._get_weight
- DFS.__dfs_walk
- DFS.__dfs_walk
- BFS.generate_graphs
- BFS._get_weight
- BFS.__dfs_walk
- BFS.__dfs_walk
"""

# imports
from networkx import DiGraph
from typing import Dict, Final, Generator, List, Tuple
from networkx.classes.digraph import DiGraph
from pandas.core.frame import DataFrame
import logging
from copy import deepcopy

# configuring logger
logger = logging.getLogger(__name__)

# A função poderá ser chamada recursivamente 1000x (default)
# sys.setrecursionlimit(1000)


def __get_period() -> Generator[int, None, None]:
    """
    Computes the current period

    :Yields:
        A value [0,10] for every period
    """
    p: int = 0
    while p < 10:
        p += 1
        yield p


def _get_period_classes(nodes: DiGraph, periodo: int) -> List[str]:
    """
    Get all class acronyms for a given `periodo`.

    :Args:
        - `nodes`: a DiGraph containing graphs and edges
        - `periodo`: current grade period. Bettween [1,10]. See :meth:`get_periodo`


    :Returns:
        A List containing all classes for a given `periodo`.
    """
    return [sigla for sigla, data in nodes.nodes(data=True) if data['period'] == str(periodo)]  # type:ignore


def _competence_not_exist_in(out: DataFrame, materias_atuais: List[str], competencia: str) -> bool:
    """
    Check if exist some value (edge) to some `competencia` in a given list of period, `materias_atuais`.

    :Args:
        - `materias_atuais`: list of class acronyms for a some period. Check it out :meth:`get_periodo`
        - `competencia`: competency to be analysed. E.g: 'BAC01'

    :Returns:
        True if there's none class in this period with this competency.
    """
    return sum([out.loc[i][competencia] for i in materias_atuais]) == 0  # type: ignore


def _get_competence_weight(
        out: DataFrame,
        materias_atuais: List[str],
        competencia: str,
        materia: str,
        roundp: int = 4,
        normalize_period: bool = True) -> float:
    """
    Get the class weight normalized by total amount of classes in a given semester.
    The maximum value that a given competency can have is 1 (100%).

    .. math:: \\frac{\\text{competency}_k}{\\sum_{i=0}^N \\text{competency}_i}

    Important
    ---------
        This module only calculate the equivalent percentual in terms of maximum compenty values\
        in a given semester.

    :Args:
        - `materias_atuais`: list of classes in the current period. Check :meth:`get_materias`
        - `competencia`: competency to be analized.
        - `materia`: class acronym to get the edge weight.

    :Kwargs:
        - `roundp`: The number of decimal places used to round

    :Returns:
        A stipulated weight rounded by `roundp` decimal places.
    """
    total: float = 1.0
    if normalize_period:
        total = sum([out.loc[i][competencia]  # type: ignore
                    for i in materias_atuais])
    return round(out.loc[materia][competencia]/total, roundp)  # type:ignore


def _generate_competency_graphs(
        out: DataFrame,
        nodes: DiGraph,
        isBFS: bool = False,
        roundp: int = 4) -> Dict[str, DiGraph]:
    """
    Create graphs for each *competence* inside `competencias`. See :ref:`figure graph web`

    Args
    ----
    `out`:
        A dataframe mapping columns (competency) to rows (classes)
    `nodes`:
        A DiGraph containing all nodes (classes) already inserted

    Keyword Args
    ------------
    `isBFS`:
        when settled, it will divide the weight by the number of vertices outcoming of the node.
    `roundp`:
        the number of decimal places to use

    Returns
    -------
    Dict[str, DiGraph]
        A dictionary mapping competency to graphs equivalent

    Example
    -------
    >>> from modules.grid import Grid
    >>> from modules.grid import Competence
    >>> # get grid
    >>> nodes, _ = Grid.get_grid(
    ...     '0192015',
    ...     CONNECTION_STRING
    ... )
    >>> # Removendo os vértices (conexões, que nates eram os pré requisitos)
    >>> nodes.remove_edges_from(list(nodes.edges()))
    >>> # Realiza a média dos arquivos de competências
    >>> out:Final[pd.DataFrame] = Skillset.merge_data(_csvs)
    >>> # obtém a soma de cada coluna
    >>> _column_sum = out.apply(np.sum, axis=0)
    >>> # normaliza pelo maior valor cada coluna
    >>> for col in out.columns:
    ...    out.loc[:, col] /= _column_sum[col]
    >>> # arredondando
    >>> out = out.round(4)
    >>> # removing
    >>> # Removendo os nós que não constam naquela planilha
    >>> nos_para_remocao:List[str] = [no for no in list(nodes.nodes()) if no not in out.index.to_list()]
    >>> nodes.remove_nodes_from(nos_para_remocao)
    >>> grafos = Competence.generate_competency_graphs
    >>> grafos
    {
       'Matemática e física': <networkx.classes.digraph.DiGraph at 0x1fa0afe2430>,
       'Lóg., algor. teoria e estrura de dados.': <networkx.classes.digraph.DiGraph at 0x1fa0afe2fd0>,
       'Ling. e parad.': <networkx.classes.digraph.DiGraph at 0x1fa0afe24c0>,
       'PAA': <networkx.classes.digraph.DiGraph at 0x1fa0afe2b50>,
       'Conf. plataformas para softwares e serviços': <networkx.classes.digraph.DiGraph at 0x1fa0afe2730>,
       'Arquiteturas de computadores': <networkx.classes.digraph.DiGraph at 0x1fa0afe2d90>,
       'Seg. de sis. de comp.': <networkx.classes.digraph.DiGraph at 0x1fa0afe2a60>,
       'Engenharia de software': <networkx.classes.digraph.DiGraph at 0x1fa0afe2e20>,
       'Inteligência artificial': <networkx.classes.digraph.DiGraph at 0x1fa0afe2400>,
       'Desenvolvimento Web e Mobile': <networkx.classes.digraph.DiGraph at 0x1fa0afe2f40>,
       'Sistemas microprocessados': <networkx.classes.digraph.DiGraph at 0x1fa0afe2d60>,
       'Redes de computadores': <networkx.classes.digraph.DiGraph at 0x1fa0afe2340>,
       'Software para sistemas de comunicação': <networkx.classes.digraph.DiGraph at 0x1fa0afe22e0>,
       'Conhec. em sist. de aut.': <networkx.classes.digraph.DiGraph at 0x1fa0afe2670>,
       'Gerenciar projetos e sistemas de computação': <networkx.classes.digraph.DiGraph at 0x1fa0afe2f70>,
       'Engenharia-econômica': <networkx.classes.digraph.DiGraph at 0x1fa0afe2ee0>,
       'Compreender e resolver problemas': <networkx.classes.digraph.DiGraph at 0x1fa0afe20a0>,
       'Autoaprendizado': <networkx.classes.digraph.DiGraph at 0x1fa0afe2880>,
       'Criatividade e Inovação': <networkx.classes.digraph.DiGraph at 0x1fa0afe2c70>,
       'Comunicação oral e escrita': <networkx.classes.digraph.DiGraph at 0x1fa0afe2820>,
       'Língua inglesa': <networkx.classes.digraph.DiGraph at 0x1fa0afe2130>,
       'Empreender e exercer liderança': <networkx.classes.digraph.DiGraph at 0x1fa0afe29d0>,
       'Trabalho em equipe': <networkx.classes.digraph.DiGraph at 0x1fa0afe2220>
    }

    Caution
    -------
    Usually, the `out` param is equal to 1 foreach column sum. It means that, at the end of the course\
        a student can have, **at maximum**, 100% of a given competence.
    """
    # Obtêndo o nome de cada coluna (será utilizada no grafo novo) ...
    # ... Equivale às competências que foram encontradas (não zeradas nos csvs) ...
    # ... Serão todas as competências dos alunos
    competencias: Final[List[str]] = out.columns.to_list()  # type: ignore

    # Instância que irá ter todos os objetos de grafos indexados pelas competências
    grafos: Dict[str, DiGraph] = {}

    # Obtêm as matérias do período seguinte (ou do próximo) que tiver ...
    # ... este requisito, gerando conexões entre essas disciplinas
    logger.debug('-'*100)
    logger.debug('Creating competency graphs')
    for competencia in competencias:
        logger.debug(f'--> {competencia}')

        # Instancia um novo grafo (baseado no grafo que já possui os nós) ...
        # ... para essa competência
        grafos[competencia]: DiGraph = nodes.copy()  # type: ignore

        # últimas matérias que possuem esta competência
        last: List[str] = []

        # Itera essa competência para os próximos períodos
        periodo: int = 0
        for periodo in __get_period():
            logger.debug(f'\tPeriod: {periodo}')

            # Obtêm a lista de todas as matérias do período atual
            materias_periodo_atual: List[str] = _get_period_classes(
                nodes, periodo)
            logger.debug(f'\t\tCurrent classes: [{materias_periodo_atual}]')

            # Se maior igual à zero, nenhuma das matérias do período ...
            # ...possui valor para essa competência
            if _competence_not_exist_in(out, materias_periodo_atual, competencia):
                # portanto, pode pular esta disciplina
                continue
            logger.debug(
                '\t\tExist classes for this competence in this period')

            # Lista para armazenar todos os nós de matérias que possuem o ...
            # ... mesmo requisito nos próximos períodos
            materias_herdeiras: List[str] = []

            # Itera sobre os próximos períodos
            prox_periodo: int = periodo
            logger.debug(
                '\t\tSearching for this competence in the futures periods')
            while prox_periodo < 10:
                prox_periodo += 1

                # Obtêm a lista de todas as matérias do período atual
                materias_proximo_periodo: List[str] = _get_period_classes(
                    nodes, prox_periodo)
                logger.debug(
                    f'\t\t\t[{prox_periodo}] : Classes -> {materias_proximo_periodo}')

                # Verifica se neste período possui alguma matéria que herda aquela competência
                if _competence_not_exist_in(out, materias_proximo_periodo, competencia):
                    continue
                logger.debug(
                    '\t\t\tExist classes for this competence in this period')

                # Caso encontre alguma matéria neste período coloca ela na ...
                # ... lista de materias que irão herdar a competência
                for i in materias_proximo_periodo:
                    if out.loc[i][competencia] > 0:  # type: ignore
                        materias_herdeiras.append(i)
                        last = deepcopy(materias_herdeiras)
                logger.debug(f'\t\t\t\tClasses: [{materias_herdeiras}]')
                # Força a saída deste loop
                break

            logger.debug('\t\tStop searching for future classes')

            # Para cada matéria atual que possui a competência e cada ...
            # ... matéria futura que irá herdar, realiza a "junção"
            logger.debug(
                '\t\tCreating the edges for this graph for each class of this period that has this competence')
            for materia_atual in materias_periodo_atual:
                # Verifica se a matéria "possui esta competência
                if out.loc[materia_atual][competencia] == 0:  # type: ignore
                    continue
                # o peso é calculado sobre as matérias de um dado período
                peso: float = _get_competence_weight(
                    out,
                    materias_periodo_atual,
                    competencia,
                    materia_atual,
                    roundp=roundp)
                logger.debug(
                    f'\t\t\tThe class "{materia_atual}" has {peso} of weight')

                # se for BFS, divide o peso pela quantidade de nós
                qnt_materias: int = len(materias_herdeiras)
                # print(f"{peso} - {qnt_materias} ", end="")
                if isBFS and qnt_materias > 0:
                    peso: float = round(peso/qnt_materias, roundp)
                # print(f"-> {peso} : {materia_atual}", end="\n\n")

                # adiciona as arestas
                logger.debug(
                    f'\t\t\tAdding the edges for: {materias_herdeiras}')

                # cria a aresta
                for materia_herdeira in materias_herdeiras:
                    grafos[competencia].add_edge(
                        materia_atual,
                        materia_herdeira,
                        weight=peso)

        logger.debug(f'Stop walking over periods for {competencia}')

        # adiciona o último nó
        grafos[competencia].add_node('Fim/Formou', period=periodo+1)
        logger.debug('Adding the last node "Fim/Formou"')
        logger.debug(f'Last value is: {last}')
        if last:
            logger.debug(f"{competencia}. ")
            for materia_atual in last:
                # o peso é calculado sobre as matérias de um dado período
                peso: float = _get_competence_weight(
                    out,
                    last,
                    competencia,
                    materia_atual,
                    roundp=roundp)
                grafos[competencia].add_edge(
                    materia_atual,
                    'Fim/Formou',
                    weight=peso)

        # se existir apenas uma única matéria (em todo o curso) ...
        # ... que possua esta competência, ela irá ter uma ligação de 100% com "Fim/Formou"
        else:
            # verificando se existe pelo menos uma disciplina com essa competência
            materia_atual = out.where(out == 1.0).dropna(
                how='all').index.tolist()
            if materia_atual:
                logger.debug(
                    f'In this dataframe exist only one class assigned to this competence ({competencia})')
                # adiciona a única matéria que tem uma determinada competência e liga ao final
                grafos[competencia].add_edge(
                    materia_atual[0],
                    'Fim/Formou',
                    weight=1.0)

            else:
                logger.debug(
                    f'In the {competencia} column, there is no class assigned to it.')

    logger.debug('-'*100)
    return grafos


class DFS:
    """
    An object created to encapsulate all elements and calls that are used in DFS.

    .. versionadded:: 0.0.9
    """

    @staticmethod
    def generate_graphs(
            out: DataFrame,
            nodes: DiGraph) -> Dict[str, DiGraph]:
        """
        A method used to create a simple graph which, in the end of dfs :meth:`walk`, will be the sum of 1.

        Args
        ----
        `out`:
            The dataframe that makes the correlation for subject and its competence
        `nodes`:
            The base graph, which contains all the needed nodes.


        Returns
        -------
        Dict[str, DiGraph]
            A dictionary mapping each competence to a given graph (:class:`networkx` object)


        .. _figure graph web:

        .. figure:: _static/img/graph_example_desenvolvimento_web.png
            :width: 700
            :alt: Graph example - Desenvolvimento Web
            :align: center

            Graph example - Desenvolvimento Web

        In the image above, the values of `out` are:


        .. csv-table::
            :header: "Period", "Acronym/Subject", "Sum", "New value"
            :widths: 1,1,1,1
            :align: center

            1, "HUMI01", 0.0435
            1, "MATI01", 0.0870
            1, "MATI02", 0.0870
            2, "ECOI04", 0.0870
            4, "ECOI09", 0.2174
            4, "MATI04", 0.1304
            5, "ECOI11", 0.1304
            5, "ECOI14", 0.0435
            9, "ECOI25", 0.1739

        However, due to the normalization made for each period:

        .. math:: \\forall \\text{ period | } \\text{subject}_i = \\frac{\\text{current_subject_value}_i}{\\sum_{n=0}^N\\text{current_subject_value}_n}


        For the period 1:

        .. math::

            \\sum\\left(\\text{HUMI01}+\\text{MATI01}+\\text{MATI02}\\right) = 0.2175 \\
            \\therefore \\
            \\text{HUMI01} = \\frac{0.0435}{0.2175} = 0.2

        Doing so, we have:


        .. csv-table::
            :header: "Period", "Acronym/Subject", "Sum", "New value"
            :widths: 1,1,1,1
            :align: center

            1, "HUMI01", , 0.2
            1, "MATI01", 0.2175, 0.4
            1, "MATI02", , 0.4
            2, "ECOI04", 0.0870, 1.0
            4, "ECOI09", 0.3478, 0.6251
            4, "MATI04", , 0.3749
            5, "ECOI11", 0.1739, 0.7499
            5, "ECOI14", , 0.250
            9, "ECOI25", 0.1739, 1.0

        Tip
        ---

        1. Propagate the **current value** (acumulated * subject * edge) to the next node.
        2. Sum all returns of children nodes. Doing so, at the end, the value should be between [0,1].

        Note
        ----
        .. image:: _static/img/perceptron_view.jpg
            :width: 500
            :align: left

        **Why don't use perceptron approach?**

        **R.:** Perceptron classifies as 0 or 1 (activate or not the layer), doing so, we will not have
        the "percentual reference" in the end.

        Todo
        ----
        According to *Giovani*, we can have a perceptron passing a value between those.
        """
        return _generate_competency_graphs(out, nodes)

    @staticmethod
    def _get_weight(
            notas: Dict[str, float],
            materia: str,
            peso: float,
            acumulado: float,
            roundp: int = 4) -> float:
        """
        Calculate the class scores for graph propagation.

        Args
        ----
        `notas`:
            dictionary mapping a class acronym to an given score
        `materia`:
            class acronym to be analysed
        `peso`:
            A calculated percentual in terms of competency in a given semester.\
                See more at :meth:`_get_competence_weight`.
        `acumulado`:
            a propagated `peso` over a graph.

        Keyword Args
        ------------
        `roundp`:
            The number of decimal places used to round

        Returns
        -------
        float
            The calculated value plus `acumulado` multiplied by `peso`

        Tip
        ---
        Used in graph propagation

        .. math:: x =
            \\begin{cases}
                \\text{acumulado}\\cdot\\text{peso}, \\text{[1]} \\\\
                \\left(\\frac{\\text{notas[materia]}}{10}\\cdot\\text{acumulado}\\right)\\cdot\\text{peso},\\text{[2]} \\\\
            \\end{cases}

        Attention
        ---------

        - If student didn't pass yet: send only the current `acumulado` multiplied by `peso` to the next period
        - If student has a score to this subject: multiply the current `acumulado` by `peso` and by `subject value`
        """
        # Caso o aluno não tenha feito a matéria ainda, propaga apenas o acumulado pelo peso
        if materia not in notas:
            return round(acumulado * peso, roundp)
        # Caso já tenha feito a matéria, calcula pelo peso e retorna mais o acumulado
        return round((notas[materia]/10 * acumulado)*peso, roundp)

    @staticmethod
    def __dfs_walk(
            notas: Dict[str, float],
            grafo: DiGraph,
            materia: str,
            acumulado: float = 1.0) -> float:
        """
        A recursive walk over competency graph

        Args
        ----
        `notas`:
            A dictionary mapping a class acronym to an value.\
                Usually, this value will be the highest student's score to this class.
        `grafo`:
            A graph equivalent to some competency.
        `materia`:
            A name for a given node.
        `acumulado`:
            The propagated value until some point

        Returns
        -------
        float
            The propageted `acumulado` value over it's childrens/leafs.

        Important
        ---------
            This approach, calculate the propagated value before walk trough graph, \
            which means that we don't need to create a new node, since that the calculus is made in\
            nodes, not in transitions
        """
        total: float = 0

        # Anda sobre os filhos
        logger.debug(
            f'\t\t\t{materia} -> {[i for i in grafo.successors(materia)]}')

        # atingiu o fim (última folha "Fim/Formou") do grafo
        if not list(grafo.successors(materia)):
            logger.debug('\t\tReached a leaf (Fim/Formou)')
            return acumulado

        logger.debug(f'\t\tCurrent acumulated: {acumulado}')
        for filho in grafo.successors(materia):
            # Obtém o peso da aresta que manda para o filho
            peso = grafo[materia][filho]['weight']
            # Obtém a nota (acumulada) que será enviada para o filho
            novo_acumulado: float = DFS._get_weight(
                notas, materia, peso, acumulado)
            logger.debug(
                f'\t\t({materia}, {filho} | w={peso}) New Acumulated: {novo_acumulado}')
            # Caminha para este filho
            total += DFS.__dfs_walk(notas, grafo, filho, novo_acumulado)
            logger.debug(f'\t\tTOTAL: {total}')

        # Retorna o valor acumulado (dos filhos até ela)
        return total

    @staticmethod
    def walk(
            grafos: Dict[str, DiGraph],
            notas: Dict[str, float]) -> Dict[str, float]:
        """
        Walk over all competences(graphs), propagating the current value
        over each semester.

        Args
        ----
        `grafos`:
            A dictionary mapping competences to graphs equivalent.
        `notas`:
            A dictionary mapping class acronym to a given score.

        Returns
        -------
        Dict[str, float]
            A dictionary mapping competency to a calculated and propagated value.

        Example
        -------
        >>> from modules.grid import Competence
        >>> from modules import Score
        >>> import json
        >>> grafos = Competence.BFS.generate_graphs(out, nodes)
        >>> student_grid: str = path.join('..','assets','parsed_scores','2016001942.json')
        >>> # obtém o histórico de um único estudante
        >>> student_grid: json = Score.read_json(student_grid)
        # Does some boring stuffs to handle and map a given class to an value ...
        >>>
        >>> # ... (usully, the greatest one for a subject)
        >>> # notas
        >>> # anda sobre o grafo para o(s) aluno(s)
        >>> notas_aluno = Competence.DFS.walk(grafos, notas)

        Important
        ---------
        This function calculates the sum propagated over all "subgraphs" that can exist in a single DiGraph.\
            For example, take a look in the figure (:ref:`figure graph web`). In this figure, we have 3 \
                independent subgraphs (We are assuming that, HUMI01|MATI01|MATI02 are indepedent graphs \
                    since they are not directly connected with each other). For those situations, this \
                        method sum the output of all subgraphs.

        Note
        ----
        This function runs the :meth:`modules.grid.Competence.__dfs_walk` for \
            all competences. Bellow you can check the **manual debugging** for this method.

        .. image:: _static/img/graph_example_devweb_debug_1.png
            :width: 290
            :alt: Graph example - Desenvolvimento Web debug#1
            :align: left

        .. image:: _static/img/graph_example_devweb_debug_2.png
            :width: 290
            :alt: Graph example - Desenvolvimento Web debug#2
            :align: right
        """
        logger.debug('-'*100)
        logger.debug('Walking over graphs')

        # Dicionário que irá conter o valor sobre cada competência
        notas_aluno: Dict[str, float] = {}
        # Itera sobre as competências
        for competencia, grafo in grafos.items():
            # ∀ competência, encontra a primeira matéria que possui ela
            edges: List[Tuple[str, str]] = list(grafo.edges())  # type: ignore
            nodes: Dict[str, str] = dict(grafo.nodes(data='period'))

            # Uma vez que o grafo foi montado em ordem cronológica, ...
            # ... sabemos que as arestas estarão em ordem crescente por período
            fst_materia: str = edges[0][0]
            fst_periodo: str = nodes[fst_materia]

            # deve pegar as primeiras disciplinas deste periodo
            # Para isso, pega todas as disciplinas do período de fst_materia
            materias_do_periodo: List[str] = [
                k for k, v in nodes.items() if v == fst_periodo]
            # filtra elas com base naquelas que existem arestas saindo delas (que têm filhos)
            materias_grafos: List[str] = [
                k for k in materias_do_periodo if list(grafo.successors(k))]

            # Em seguida, anda no seu grafo e obtêm o valor iterado sobre as notas ...
            # ... ou seja, a soma das notas propagadas
            logger.debug(f'\tCompetence {competencia} - Walking')

            # chama o dfs para cada subgrafo independente
            resultado: float = 0
            for materias in materias_grafos:
                resultado += DFS.__dfs_walk(notas, grafo, materias)

            logger.debug(f'\tCompetence: {competencia} = {resultado}')
            # valor das notas iteradas sobre o grafo de uma competência "N"
            notas_aluno[competencia] = resultado
            logger.debug('-'*50)
        logger.debug('-'*100)
        # Notas do aluno propagadas no grafo de competência
        return notas_aluno


class BFS:
    """
    An object created to encapsulate all elements and calls that are used in DFS.

    .. versionadded:: 0.0.8
    """

    @staticmethod
    def generate_graphs(
            out: DataFrame,
            nodes: DiGraph) -> Dict[str, DiGraph]:
        """
        A method used to create a simple graph which, in the end of dfs :meth:`walk`, will be the sum of 1.

        Args
        ----
        `out`:
            The dataframe that makes the correlation for subject and its competence
        `nodes`:
            The base graph, which contains all the needed nodes.


        Returns
        -------
        Dict[str, DiGraph]
            A dictionary mapping each competence to a given graph (:class:`networkx` object)


        .. _figure graph web 2:

        .. figure:: _static/img/graph_example_desenvolvimento_web_2.png
            :width: 700
            :alt: Graph example - Desenvolvimento Web
            :align: center

            Graph example - Desenvolvimento Web

        In the image above, the values of `out` are:


        .. csv-table::
            :header: "Period", "Acronym/Subject", "Original/Out value"
            :widths: 1,1,1
            :align: center

            1, "HUMI01", 0.0435
            1, "MATI01", 0.0870
            1, "MATI02", 0.0870
            2, "ECOI04", 0.0870
            4, "ECOI09", 0.2174
            4, "MATI04", 0.1304
            5, "ECOI11", 0.1304
            5, "ECOI14", 0.0435
            9, "ECOI25", 0.1739

        However, due to the normalization made for each period:

        .. math:: \\forall \\text{ period | } \\text{subject}_i = \\frac{\\text{current_subject_value}_i}{\\sum_{n=0}^N\\text{current_subject_value}_n}


        Important
        ---------
        The :math:`\\sum` of each period is equal to 1.0. E.g: \
            :math:`\\sum\\text{period}_1 = HUMI01\\cdot0.2 + MATI01\\cdot0.4 + MATI02\\cdot0.4 \\equiv 1.0`



        For the period 1:

        .. math::

            \\sum\\left(\\text{HUMI01}+\\text{MATI01}+\\text{MATI02}\\right) = 0.2175 \\
            \\therefore \\
            \\text{HUMI01} = \\frac{0.0435}{0.2175} = 0.2

        Doing so, we have:


        .. csv-table::
            :header: "Period", "Acronym/Subject", "Sum", "New value"
            :widths: 1,1,1,1
            :align: center

            1, "HUMI01", , 0.2
            1, "MATI01", 0.2175, 0.4
            1, "MATI02", , 0.4
            2, "ECOI04", 0.0870, 1.0
            4, "ECOI09", 0.3478, 0.6251
            4, "MATI04", , 0.3749
            5, "ECOI11", 0.1739, 0.7499
            5, "ECOI14", , 0.250
            9, "ECOI25", 0.1739, 1.0

        Tip
        ---

        1. Propagate the **current value** (acumulated * subject * edge) to the next node.
        2. Sum all returns of children nodes. Doing so, at the end, the value should be between [0,1].

        Note
        ----
        .. image:: _static/img/perceptron_view.jpg
            :width: 500
            :align: left

        **Why don't use perceptron approach?**

        **R.:** Perceptron classifies as 0 or 1 (activate or not the layer), doing so, we will not have
        the "percentual reference" in the end.

        Todo
        ----
        According to *Giovani*, we can have a perceptron passing a value between those.

        Caution
        -------
        This method also assumes that, for each period, the maximum obtained value propagated will be 100%. It means that, for\
                each period, the percentual values are normalized.
        """
        return _generate_competency_graphs(out, nodes, isBFS=True)

    @staticmethod
    def _get_weight(
            notas: Dict[str, float],
            materia: str,
            accumulated: float) -> float:
        """
        Returns the the subject multiplied by its accumulated.

        Args
        ----
        `notas`:
            A dictionary mapping class acronym to a given score.
        `materia`:
            The subject that will be searched for
        `accumulated`:
            The accumulated of this period


        Returns
        -------
        float
            The equivalent result of the operation

        Attention
        ---------
        If there's no `materia` in `notas`, the returned value will be 0
        """
        if materia not in notas:
            return 0
        return notas[materia]/10 * accumulated

    @staticmethod
    def walk(
            grafos: Dict[str, DiGraph],
            notas: Dict[str, float],
            roundp: int = 2) -> Dict[str, float]:
        """
        Walk over all competences(graphs), propagating the current value
        over each semester.

        :Complexity: :math:`\\mathcal{O}(n^4)`

        Args
        ----
        `grafos`:
            A dictionary mapping competences to graphs equivalent.
        `notas`:
            A dictionary mapping class acronym to a given score.

        Keyword Args
        ------------
        `roundp`:
            The number of decimal places used when rounding.

        Returns
        -------
        Dict[str, float]
            A dictionary mapping competency to a calculated and propagated value.

        Example
        -------
        >>> from modules.grid import Competence
        >>> from modules import Score
        >>> import json
        >>> grafos = Competence.BFS.generate_graphs(out, nodes)
        >>> student_grid: str = path.join('..','assets','parsed_scores','2016001942.json')
        >>> # obtém o histórico de um único estudante
        >>> student_grid: json = Score.read_json(student_grid)
        # Does some boring stuffs to handle and map a given class to an value ...
        >>>
        >>> # ... (usully, the greatest one for a subject)
        >>> # notas
        >>> # anda sobre o grafo para o(s) aluno(s)
        >>> notas_aluno = Competence.BFS.walk(grafos, notas)


        Caution
        -------
        Usually, the code uses the maximum number of available decimal places \
            to float precision. However, in the end of the code, the output is\
                rounded by `roundp`.

        Important
        ---------

        - The accumulated is multiplied by each competence in the current period
        - The accumulated is equivalent to the sum of the previous period
        - When the **sum** of the current period is 0, the accumulated won't change \
            (it just skip the current period). For example, in these situations:
            - When the student hasn't taken the subject yet
            - When the student's score is equal to 0
        """
        logger.debug('-'*100)
        logger.debug('Walking over graphs')

        # Dicionário que irá conter o valor sobre cada competência
        notas_aluno: Dict[str, float] = {}

        # Itera sobre as competências
        for competencia, grafo in grafos.items():
            # encontra todos os nós e arestas do grafo. Isso é necessário
            nodes: Dict[str, str] = dict(grafo.nodes(data='period'))

            logger.debug(f'\tCompetence "{competencia}" - Walking')
            # acumulado do período
            a: float = 1.0
            logger.debug(f'\tACUMULATED = {a}')
            # anda sobre todos os periodos
            for p in range(1, 10):
                logger.debug(f'\t\t{p}:')
                materias = filter(lambda k: nodes[k] == str(p), nodes)
                # somatório de todas as disciplinas do periodo * aresta que saem delas
                s: float = 0.0
                # Calcula para cada matéria do periodo
                for m in materias:
                    # filhos
                    f: List[str] = list(grafo.successors(m))
                    # se não tiver filhos, pula
                    if not f:
                        continue
                    # nota_do_aluno * acumulado_propagado
                    n: float = BFS._get_weight(notas, m, a)
                    logger.debug(f'\t\t\t{m}:{n} -> Successors: {f}')
                    s += sum(map(lambda x: n * grafo[m][x]['weight'], f))
                # somente altera o acumulado se ouve somatório (filhos)
                if s > 0.0:
                    a = s
                logger.debug(f'\t\tACUMULATED = {a}.  SUM = {s}')
            # notas do aluno é o acumulado
            notas_aluno[competencia] = round(a, roundp)

        return notas_aluno
