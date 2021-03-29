from typing import List, Optional
import plotly
from plotly.missing_ipywidgets import FigureWidget


def plot(
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

    # checking excential kwargs
    if all(("r1" is not None, "r1_name" is not None)):
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

    if all(("r2" is not None, "r2_name" is not None)):
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
