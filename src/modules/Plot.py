from typing import List
import pandas as pd
import plotly
import plotly.express as px
from plotly.missing_ipywidgets import FigureWidget
import logging as logger


def spider_plot(
    categories: List[str],
    show: bool = True,
    r1: List[float] = None,
    r1_name: str = None,
    r2: List[float] = None,
    r2_name: str = None
) -> FigureWidget:
    """
    Does spider plot. Accept at max 2 elements.
    By default, it assumes that only are possible values between 0..1

    :Args:
        - `categories`: A list with name strings that will be used as labels

    :Kwargs:
        - `r1`: List[Float] Mapped values following `categories` order
        - `r1_name`: (str) Name of this section
        - `show`: *OPTIONAL* if settled will not show the figure at end
        - `r2`: *OPTIONAL*. List[Float] Mapped values following `categories` order
        - `r2_name`: *OPTIONAL*. (str) Name of this section

    :Returns:
      - A figure plotly object (only access by ipykernel)
    """

    logger.debug("Starting a new plot")
    # checking excential kwargs
    if all(("r1" == None, "r1_name" == None)):
        raise Exception(
            "You must pass at least one graph, i.e, r1:List and r1_name")

    import plotly.graph_objects as go

    fig: FigureWidget = plotly.graph_objects.Figure()  # type: ignore

    fig.add_trace(go.Scatterpolar(
        r=r1,
        theta=categories,
        fill='toself',
        name=r1_name
    ))  # type: ignore

    if all((r2 != None, r2_name != None)):
        fig.add_trace(go.Scatterpolar(
            r=r2,
            theta=categories,
            fill='toself',
            name=r2_name
        ))  # type: ignore

    # update figure object
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True
    )

    # show this object
    if show:
        fig.show()

    # and return it
    return fig


def parallel_plot(
    df: pd.DataFrame,
    column_color: str,
    s: int = 0,
    e: int = 5,
    show: bool = True,
    color_scale: List[str] = px.colors.diverging.Tealrose,
    width: int = 1200,
    height: int = 620
) -> FigureWidget:
    """
    Realize a parallel plot. A parallel plot is a plot similar to line plt.
    Check it out the `parallel plot`_ documentation.

    :Args:
        - `df`: The dataframe object to be plotted
        - `column_color`: The name of the column that holds the float equivalent number to be colored.\
            This column should hold ranges like 0.0..3.0

    :Kwargs:
        - `s`: start column to be plotted. *REMEBER* to include the column_color in this range.
        - `e`: end column
        - `show`: show the figure after generated
        - `color_scale`: it's a range of hexadecimal colors.\
            The default value is `plotly.express.colors.diverging.Tealrose`
        - `width`: the figure width
        - `height`: the figure height

    :Returns:
        A generated figure object

    .. _parallel plot: https://plotly.com/python/parallel-coordinates-plot/
    """
    # convert to list
    cols = df.columns.tolist()

    # cria um novo dataframe usando somente o range estipulado
    _d = df[cols[s:e]]

    fig: FigureWidget = px.parallel_coordinates(
        _d,
        color=column_color,
        width=width, height=height,
        color_continuous_scale=color_scale,
        color_continuous_midpoint=2,
    )  # type: ignore

    # exibe a figura
    if show:
        fig.show()

    return fig


def pie_plot(
    df: pd.DataFrame,
    col: str,
    threshold: float = 0.08,
    show: bool = False
) -> FigureWidget:
    """
    Generates a pie plot for a given dataframe.

    :Args:
        - `df`: A pandas dataframe object like
        - `col`: The column to be analysed

    :Kwargs:
        - `threshold`: The value that used to group elements in this column
        - `show`: If setled, show the generated plot too

    :Returns:
        A `plotly.Figure`
    """
    # removendo linhas onde essa competência não existe
    df = df.query(f"`{col}` > 0")
    # juntando índices com peso menor que threshold
    _index = df.loc[df[col] < threshold, col].index  # type:ignore
    # substituindo esses índices, gerando um "índice compartilhado"
    df.index = df.index.map(lambda x: "Outras" if x in _index else x)

    # gerando as anotações
    a = list(_index)
    a = [a[i:i+10] for i in range(0, len(a), 10)]
    annotation = "Outras: "
    for l in a:
        annotation += ','.join(l)
        annotation += '<br>'

    fig = px.pie(
        df,
        names=df.index,
        values=col,
        title=f"Distribuição da competência: {col}")

    # adicionando o nome das matérias ocultadas
    fig.add_annotation(
        x=0, y=-0.27,
        text=annotation,
        showarrow=False)

    # fig.update_layout(showlegend=True)
    if show:
        fig.show()

    return fig


def bar_plot(
    df: pd.DataFrame,
    col: str,
    show: bool = False,
    filename: str = '',
) -> FigureWidget:
    """
    Generates a bar plot.

    :Args:
        - `df`: A dataframe object to be plotted
        - `col`: The column to be analysed

    :Kwargs:
        - `show`: Flag to force the figure to be shown
        - `filename`: A path to store the image. It must contains the extension too.

    :Returns:
        The figure object of the image created

    .. seealso::

        `See more on Pyplot exporting image <https://plotly.com/python/static-image-export>`_
    """
    logger.debug(f"Starting a new bar_plot: {filename}")
    # removendo linhas onde essa competência não existe
    df = df.query(f"`{col}` > 0")

    fig: FigureWidget = px.bar(
        df,
        x=df.index,
        y=col,
        text=col)  # type: ignore

    fig.update_traces(textposition='outside')

    if filename:
        logger.debug(f"Generating image files for {filename}")
        fig.write_image(filename)

    if show:
        logger.debug('Showing image for')
        fig.show()

    return fig
