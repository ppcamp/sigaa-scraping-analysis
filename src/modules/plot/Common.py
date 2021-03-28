from typing import List
import plotly
from plotly.missing_ipywidgets import FigureWidget
from traitlets.traitlets import Float


def plot(categories: List[str], **kwargs) -> FigureWidget:
    """
    Does spider plot. Accept at max 2 elements.
    By default, it assumes that only are possible values between 0..1

    :Parameters:
      - `categories`: A list with name strings that will be used as labels
      - `kwargs["show"]`: OPTIONAL if settled will not show the figure at end
      - `kwargs["r1"]`: List[Float] Mapped values following `categories` order
      - `kwargs["r1_name"]`: (str) Name of this section
      - `kwargs["r2"]`: *OPTIONAL*. List[Float] Mapped values following `categories` order
      - `kwargs["r2_name"]`: *OPTIONAL*. (str) Name of this section

    :Returns:
      - A figure plotly object (only access by ipykernel)
    """

    # checking excential kwargs
    if all(("r1" not in kwargs, "r1_name" not in kwargs)):
        raise Exception(
            "You must pass at least one graph, i.e, r1:List and r1_name")

    import plotly.graph_objects as go

    fig: FigureWidget = plotly.graph_objects.Figure()  # type: ignore

    fig.add_trace(go.Scatterpolar(
        r=kwargs["r1"],
        theta=categories,
        fill='toself',
        name=kwargs["r1_name"]
    ))  # type: ignore

    if all(("r2" in kwargs, "r2_name" in kwargs)):
        fig.add_trace(go.Scatterpolar(
            r=kwargs["r2"],
            theta=categories,
            fill='toself',
            name=kwargs["r2_name"]
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
    if "show" not in kwargs:
        fig.show()
    else:
        if kwargs["show"]:
            fig.show()

    # and return it
    return fig
