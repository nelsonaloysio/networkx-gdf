from io import StringIO
from abc import abstractmethod
from csv import QUOTE_MINIMAL
from typing import Optional, Union

import networkx as nx
import pandas as pd

TYPES = {
    "VARCHAR": str,
    "INT": int,
    "FLOAT": float,
    "DOUBLE": float,
    "BOOLEAN": bool,
}

QUOTES = {
    "single": "'",
    "double": '"',
}


class GDF(object):

    @abstractmethod
    def __init__(self):
        """ Abstract method for "DIY" implementations. """

    @staticmethod
    def read_gdf(
        path: str,
        directed: Optional[bool] = None,
        multigraph: Optional[bool] = None,
        node_attr: Optional[Union[list, bool]] = True,
        edge_attr: Optional[Union[list, bool]] = True,
    ) -> nx.Graph or nx.DiGraph or nx.MultiGraph or nx.MultiDiGraph:
        """
        Returns a NetworkX graph object from Graph Data File.
        """
        source, target = "node1", "node2"

        def get_def(content):
            return {
                field[0]:
                    TYPES.get(field[1], str) if len(field) > 1 else str
                for field in [
                    tuple(_.rsplit(" ", 1))
                    for _ in content.split("\n", 1)[0].split(">", 1)[-1].split(",")
                ]
            }

        def get_list(content, **params):
            exception = ""

            for quote, char in QUOTES.items():
                try:
                    return pd.read_csv(StringIO(content),
                                       quotechar=char,
                                       escapechar="\\",
                                       na_filter=False,
                                       **params)

                except Exception as e:
                    exception += f"\n{type(e).__name__}: {str(e).rstrip()} ({quote} quotes)"

            raise Exception("unable to read data from file considering both single "
                            f"and double quotes as text delimiter.{exception}")

        # Gather node and edge definitions.
        with open(path, "r") as f:
            nodes, edges = f.read().split("nodedef>", 1)[-1].split("edgedef>", 1)
            nodedef, edgedef = get_def(nodes), get_def(edges)

        # Build node and edge list assuming single or double quotes as text delimiters.
        nodes = get_list(nodes, names=list(nodedef.keys()), dtype=nodedef, header=0, index_col="name")
        edges = get_list(edges, names=list(edgedef.keys()), dtype=edgedef, header=0)

        # Read 'directed' attribute from data if found.
        if directed is None and "directed" in edges.columns:
            directed = bool(edges["directed"][0])

            if edges["directed"].unique().shape[0] > 1:
                raise NotImplementedError(
                    "Graphs with both directed and undirected edges are not supported, "
                    "please specify `directed=False` or `directed=True`.")

        # Allow multiple edges among nodes if found.
        if multigraph is None and edges[[source, target]].duplicated().any():
            multigraph = True

        # Object type to build graph with.
        create_using = nx.DiGraph() if directed else nx.Graph()
        if multigraph:
            create_using = nx.MultiDiGraph() if directed else nx.MultiGraph()

        # Edge attributes to consider.
        if edge_attr is True:
            edge_attr = [_ for _ in edges.columns if _ not in [source, target] +
                         (["directed"] if edges["directed"].unique().shape[0] == 1 else [])]

        # Convert edge list to graph.
        G = nx.convert_matrix\
              .from_pandas_edgelist(edges,
                                    source=source,
                                    target=target,
                                    edge_attr=edge_attr or None,
                                    create_using=create_using)

        # Add any missing nodes not within edge list.
        G.add_nodes_from(nodes.index)

        # Assign attributes to nodes in graph.
        for attr in (list(nodes.columns) if node_attr == True else (node_attr or [])):
            nx.set_node_attributes(G, nodes[attr], attr)

        return G

    @staticmethod
    def write_gdf(
        G: nx.Graph,
        path: str,
        node_attr: Optional[Union[list, bool]] = True,
        edge_attr: Optional[Union[list, bool]] = True,
    ) -> None:
        """
        Writes a NetworkX graph object to Graph Data File.
        """
        types = {value.__name__: key for key, value in TYPES.items()}

        def get_columns(df):
            """ Add attribute type to column names. """
            return [f"{key} {types.get(value.__str__().lower().rstrip('0123456789'), 'VARCHAR')}"
                    for key, value in df.dtypes.to_dict().items()]

        def get_nodes(G):
            """ Build node list with attributes. """
            nodes = pd.DataFrame(dict(G.nodes(data=True)).values(),
                                 index=G.nodes())

            if node_attr not in (True, None):
                nodes = nodes.loc[:, (node_attr if node_attr else [])]

            nodes.columns = get_columns(nodes)
            nodes.index.name = "nodedef>name VARCHAR"
            return nodes.fillna("")

        def get_edges(G):
            """ Build edge list with attributes. """
            edges = nx.to_pandas_edgelist(G)
            edges.columns = ["edgedef>node1", "node2"] + edges.columns[2:].tolist()

            if edge_attr not in (True, None):
                edges = edges.loc[:, edges.columns[:2].tolist() + (edge_attr if edge_attr else [])]

            if "directed" not in edges.columns:
                edges["directed"] = True if G.is_directed() else False

            edges.columns = get_columns(edges)
            return edges.fillna("")

        get_nodes(G).to_csv(path,
                            index=True,
                            quoting=QUOTE_MINIMAL,
                            quotechar="'",
                            escapechar="\\",
                            mode="w")

        get_edges(G).to_csv(path,
                            index=False,
                            quoting=QUOTE_MINIMAL,
                            quotechar="'",
                            escapechar="\\",
                            mode="a")


read_gdf = GDF.read_gdf
write_gdf = GDF.write_gdf
