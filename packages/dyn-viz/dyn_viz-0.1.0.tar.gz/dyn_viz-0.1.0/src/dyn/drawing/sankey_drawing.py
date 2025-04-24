"""This module defines the utilities needed to draw a sankey diagram.

It is based on module :mod:`plotly.graph_objects`.
"""
import random

import plotly.graph_objects as go
from dyn.core.communities import Membership, Tcommlist
from dyn.core.community_graphs import EvolvingCommunitiesGraph
from plotly.colors import (
    colorscale_to_colors,
    get_colorscale,
    sample_colorscale,
)

from dyn.drawing.sankey_optimization import SankeyOptimizer

__all__ = ["draw_sankey", "plot_sankey", "save_sankey"]


class SankeyPlot:
    """Class used to draw sankey diagram.

    :param sankey: sankey diagram
    :param colormap:
        colormap to use for the nodes (one color per evolving community will be
        sampled)

    .. note::
        Static community won't have the exact correct size as the visual size
        depends on the flows.
        The only way to have the correct sizes is to represent the *void* nodes
        in the sankey, but it renders the plot confusing.
    """

    def __init__(
        self, graph: EvolvingCommunitiesGraph, colormap: str = "jet"
    ) -> None:
        self.graph = graph
        self.color_scale = get_colorscale(colormap)
        # Remove nodes not belonging to communities (e.g 'void')
        to_remove = set()
        for n in self.graph.nodes:
            if "evolvingCommunity" not in self.graph.nodes[n]:
                to_remove.add(n)
        for n in to_remove:
            self.graph.remove_node(n)

        # Initialize sankey plots attributes
        self.label = []  # label of each node
        self.color = []  # x position of each node
        self.x = []  # x position of each node
        self.y = []  # y position of each node

        self.source = []  # source of each flow
        self.target = []  # target of each flow
        self.value = []  # size of each flow
        self.link_color = []  # color for each links

        # populate all those attributes
        self.prepare_plot()

    @staticmethod
    def _tweak_value(x: float) -> float:
        """Tweak position of node on figure to avoid position bugs.

        :param x:
        :return: a value different of ``0`` and ``1``
        """
        if x == 0:
            return 0.001
        if x == 1:
            return 0.999
        return x

    def prepare_plot(self) -> None:
        """Compute attributes necessary to draw Sankey diagram"""
        self.label = list(self.graph.nodes)
        indexes = {n: self.label.index(n) for n in self.label}
        y_dict = {
            n: SankeyPlot._tweak_value(i / len(self.graph.snapshot_nodes(t)))
            for t in self.graph.snapshots
            for i, n in enumerate(
                sorted(self.graph.snapshot_nodes(t), key=lambda k: indexes[k])
            )
        }
        self.x = [
            SankeyPlot._tweak_value(
                self.graph.node_snapshot(n) / (self.graph.max_snapshot)
            )
            for n in self.label
        ]
        self.y = [y_dict[n] for n in self.label]

        communities = list(self.graph.communities)
        color_samples = (
            sample_colorscale(
                self.color_scale,
                len(communities),
            )
            if len(communities) > 1
            else [colorscale_to_colors(self.color_scale)[0]]
        )
        random.shuffle(color_samples)
        colors = {
            comm: color
            for comm, color in zip(
                self.graph.communities,
                color_samples,
            )
        }
        self.color = [colors[self.graph.node_community(n)] for n in self.label]

        for n1, n2, flow in self.graph.edges(data="flow"):
            self.source.append(indexes[n1])
            self.target.append(indexes[n2])
            self.value.append(flow)
            self.link_color.append("rgba(127, 127, 127, 0.3)")

    def draw(self) -> go.Figure:
        """Draw sankey diagram on a new figure.

        :return: the drawn figure
        """
        return go.Figure(
            data=go.Sankey(
                arrangement="snap",
                node=dict(
                    label=self.label,
                    x=self.x,
                    y=self.y,
                    color=self.color,
                ),
                link=dict(
                    source=self.source,
                    target=self.target,
                    value=self.value,
                    color=self.link_color,
                ),
            )
        )

    def plot(self) -> None:
        """Plot the sankey diagram and show it."""
        fig = self.draw()
        fig.show()

    def save_image(self, plot_file: str, *args, **kwargs):
        """Save sankey diagram as an image.

        :param plot_file:
        :param args:
            any positional arguments passed to
            :meth:`plotly.graph_objects.Figure.write_image`
        :param kwargs:
            any keyword arguments passed to
            :meth:`plotly.graph_objects.Figure.write_image`

        .. seealso::
            `Plotly graph_objects.Figure.write_image doc <https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html#plotly.graph_objects.Figure.write_image>`_
                Documentation of the :meth:`plotly.graph_objects.Figure.write_html` method
        """  # noqa: E501
        fig = self.draw()
        fig.write_image(plot_file, *args, **kwargs)

    def save_html(self, plot_file: str, *args, **kwargs):
        """Save sankey diagram as a html page.

        :param plot_file:
        :param args:
            any positional arguments passed to
            :meth:`plotly.graph_objects.Figure.write_html`
        :param kwargs:
            any keyword arguments passed to
            :meth:`plotly.graph_objects.Figure.write_html`

        .. seealso::
            `Plotly graph_objects.Figure.write_html doc <https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html#plotly.graph_objects.Figure.write_html>`_
                Documentation of the :meth:`plotly.graph_objects.Figure.write_html` method
        """  # noqa: E501
        fig = self.draw()
        fig.write_html(plot_file, *args, **kwargs)


class SankeyDrawer(SankeyPlot):
    """This class represents a sankey drawing with an optional optimizer.

    :param graph: community flow graph
    :param optimizer:
        configuration of sankey optimizer
    :param colormap: name of plotly colormap chosen

    .. seealso::
        :class:`dyn.drawing.sankey_optimization.SankeyOptimizer`
            Class used to optimize the sankey before plotting

        :class:`SankeyPlot`
            Class used to effectively plot the sankey diagram
    """

    def __init__(
        self,
        graph: EvolvingCommunitiesGraph,
        optimizer: dict = None,
        colormap: str = "jet",
    ) -> None:
        self.optimizer = (
            None if optimizer is None else SankeyOptimizer(graph, **optimizer)
        )
        graph = graph if self.optimizer is None else self.optimizer.run()
        super().__init__(graph, colormap)


def _init_sankey(
    graph: Tcommlist | EvolvingCommunitiesGraph,
    optimizer_kwargs: dict = None,
    colormap: str = "jet",
) -> SankeyDrawer:
    """Initialize a sankey drawer.

    :param graph: either a tcommlist or a community flow graph
    :param optimizer_kwargs:
        configuration of sankey optimizer (no optimization if absent)
        it consists the keyworded arguments fed to
        :class:`dyn.drawing.sankey_optimization.SankeyOptimizer`
    :param colormap:
    :return: sankey drawer
    """
    graph = (
        Membership.from_tcommlist(graph).community_graph
        if isinstance(graph, Tcommlist)
        else graph
    )
    return SankeyDrawer(graph, optimizer_kwargs, colormap)


def draw_sankey(
    graph: Tcommlist | EvolvingCommunitiesGraph,
    optimizer_kwargs: dict = None,
    colormap: str = "jet",
) -> go.Figure:
    """Draw sankey and return it.

    :param graph: either a tcommlist or a community flow graph
    :param optimizer_kwargs:
        configuration of sankey optimizer (no optimization if absent)
        it consists the keyworded arguments fed to
        :class:`dyn.drawing.sankey_optimization.SankeyOptimizer`
    :param colormap:
    :return: drawn sankey image
    """
    return _init_sankey(graph, optimizer_kwargs, colormap).draw()


def plot_sankey(
    graph: Tcommlist | EvolvingCommunitiesGraph,
    optimizer_kwargs: dict = None,
    colormap: str = "jet",
):
    """Plot sankey.

    :param graph: either a tcommlist or a community flow graph
    :param optimizer_kwargs:
        configuration of sankey optimizer (no optimization if absent)
        it consists the keyworded arguments fed to
        :class:`dyn.drawing.sankey_optimization.SankeyOptimizer`
    :param colormap:
    """
    _init_sankey(graph, optimizer_kwargs, colormap).plot()


def save_sankey(
    graph: Tcommlist | EvolvingCommunitiesGraph,
    output_file: str,
    *args,
    optimizer_kwargs: dict = None,
    colormap: str = "jet",
    **kwargs,
):
    """Draw and save sankey to an image or html file.

    :param graph: either a tcommlist or a community flow graph
    :param output_file:
    :param optimizer_kwargs:
        configuration of sankey optimizer (no optimization if absent)
        it consists the keyworded arguments fed to
        :class:`dyn.drawing.sankey_optimization.SankeyOptimizer`
    :param colormap:

    .. note::
        Remaining positional and key-worded arguments are supplied to
        :meth:`plotly.graph_objects.Figure.save_html` (for a html file) or
        :meth:`plotly.graph_objects.Figure.save_image` (for an image file).
    """
    drawer = _init_sankey(graph, optimizer_kwargs, colormap)
    if output_file.endswith(".html"):
        drawer.save_html(output_file, *args, **kwargs)
    else:
        drawer.save_image(output_file, *args, **kwargs)
