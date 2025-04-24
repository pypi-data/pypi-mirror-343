"""This script is used to draw sankey diagrams from .gml files.

Load sankey diagram and draw it in a file.

.. code:: bash

    python main_draw_sankey.py OUT_DIR
        [--sankey FILE | --sankey-folder FOLDER]
        [--community ID1 [--community ID2 [ ... ]]] | --all-communities]
        [[--optimizer {GA,HA,SA} ] [--optimizer-time TIME] | --no-optimizer]
        [--colormap COLORMAP]

    OUT_DIR is the directory where sankey will be drawn.

    Inputs:
    * --sankey FILE               FILE is the .gml sankey file ot tcommlist
    * --sankey-folder FOLDER      FOLDER contains the .gml sankey diagrams or tcommlists to draw
    * --community ID              ID of a community to draw (can be set multiple times).
                                  In this case, set communities are drawn in their own file.
    * --all-communities           All communities are drawn in their own file.
    * --optimizer {GA,HA,SA}      Set sankey optimizer algorithm (in the absence of config file)
    * --optimizer-time TIME       Set max optimization time (in the absence of config file)
    * --no-optimizer              Disable the optimization process if flag present
                                  (supersedes config file)
    * --colormap COLORMAP         Set plotly colormap for sankey drawing (in the absence of config file)
"""  # noqa: E501
import argparse
import logging
from os import listdir, makedirs
from os.path import isdir, join

from dyn.core.community_graphs import EvolvingCommunitiesGraph
from dyn.core.files_io import load_graph, load_tcommlist

from .sankey_drawing import SankeyDrawer

LOGGER = logging.getLogger(__name__)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "plot_folder", type=str, help="folder to save the figures"
    )
    parser.add_argument(
        "--sankey", type=str, help="GML Sankey file or tcommlist to plot"
    )
    parser.add_argument(
        "--sankey-folder",
        type=str,
        help="folder that contains GML Sankey files or tcommlists to plot",
    )
    parser.add_argument(
        "--community",
        type=str,
        help="a specific community name to plot. "
        "Each new community must be after a flag",
        action="append",
    )
    parser.add_argument(
        "--all-communities",
        action="store_true",
        help="if this argument is True, then all communities are extracted "
        "separately",
    )
    parser.add_argument(
        "-a",
        "--optimizer",
        type=str,
        default="SA",
        choices=["GA", "HA", "SA"],
        help="optimization algorithm (ignored if config file provided)",
    )
    parser.add_argument(
        "--optimizer-time",
        type=float,
        default=30,
        help="allocated time for sankey optimization process (s) "
        "(ignored if config file provided)",
    )
    parser.add_argument(
        "--no-optimizer",
        action="store_true",
        help="if this argument is True, no plot optimization is used"
        "(saves time, supersedes --optimizer and config file)",
    )
    parser.add_argument(
        "--colormap",
        type=str,
        default="jet",
        help="colormap used to color evolving communities"
        "(from plotly colormaps, ignored if config file provided)",
    )
    parser.add_argument(
        "-l", "--log", help="Activate logging INFO level.", action="store_true"
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="Activate logging DEBUG level.",
        action="store_true",
    )

    args = parser.parse_args()

    LOG_FORMAT = (
        "[%(asctime)s] [%(levelname)8s] --- %(message)s "
        "(%(filename)s:%(lineno)s)"
    )
    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    elif args.log:
        logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    # Preparation
    if not isdir(args.plot_folder):
        makedirs(args.plot_folder)

    communities_to_plot = []

    # Process plot options
    config = {}
    config["optimizer"] = {}
    config["optimizer"]["algo"] = args.optimizer
    config["optimizer"]["time_max"] = args.optimizer_time
    config["colormap"] = args.colormap

    if args.no_optimizer:
        config.pop("optimizer", None)

    # A whole folder has to be plot
    if args.sankey_folder:
        graphs_to_plot = []

        for file in listdir(args.sankey_folder):
            *filename, extension = file.split(".")
            filename = ".".join(filename)

            # Checke that the file is a graph file
            if extension == "gml":
                graph = EvolvingCommunitiesGraph.from_graph(
                    load_graph(join(args.sankey_folder, file))
                )
            elif extension == "tcommlist":
                graph = load_tcommlist(
                    join(args.sankey_folder, file)
                ).community_flow_graph
            else:
                continue

            this_community = graph.graph["community"]

            # The Sankey is not associated with a community
            if this_community == "all":
                continue

            # Some communities are asked for but not this one
            if args.community and this_community not in args.community:
                if len(graphs_to_plot) == len(args.community):
                    break

                continue

            graphs_to_plot.append(graph)

        # Plot the selected communities
        for graph in graphs_to_plot:
            community_id = graph.graph["community"]
            plot_file = join(args.plot_folder, f"{community_id}.html")
            SankeyDrawer(graph, **config).save_html(plot_file)

    # if a single file is given to plot
    elif args.sankey:
        graph = EvolvingCommunitiesGraph.from_graph(load_graph(args.sankey))
        *filename, extension = args.sankey.split(".")
        if extension == "gml":
            graph = EvolvingCommunitiesGraph.from_graph(
                load_graph(args.sankey)
            )
        elif extension == "tcommlist":
            graph = load_tcommlist(args.sankey).community_flow_graph
        else:
            LOGGER.error(
                "sankey argument can only be either a GML or tcommlist file"
            )
            exit(1)

        if args.all_communities:
            communities_to_plot = graph.communities

        elif args.community:
            communities_to_plot = args.community

        # If the whole graph is asked to be drown, we do it and quit
        if not communities_to_plot:
            plot_file = join(args.plot_folder, "sankey.html")
            SankeyDrawer(graph, **config).save_html(plot_file)
            exit()

        for community in communities_to_plot:
            if community not in graph.communities:
                LOGGER.debug(f"community {community} not found")
                continue

            nodes = graph.community_nodes[community]
            subgraph = EvolvingCommunitiesGraph.from_graph(
                graph.subgraph(nodes)
            )
            subgraph.graph["community"] = community
            plot_file = join(args.plot_folder, f"{community}.html")
            SankeyDrawer(subgraph, **config).save_html(plot_file)
