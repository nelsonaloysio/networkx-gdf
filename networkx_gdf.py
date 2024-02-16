from io import StringIO
from abc import abstractmethod
from typing import Optional, Union

import networkx as nx
import pandas as pd

TYPES = {
    "VARCHAR": str,
    "INT": int,
    "LONG": int,
    "FLOAT": float,
    "DOUBLE": float,
    "BOOLEAN": bool,
}

QUOTES = {
    "single": "'",
    "double": '"',
}

M = 2**31


class GDF():

    @abstractmethod
    def __init__(self):
        """ Abstract method for "DIY" implementations. """

    @staticmethod
    def read_gdf(
        path: str,
        directed: Optional[bool] = None,
        multigraph: Optional[bool] = None,
        node_attr: Optional[Union[list, bool]] = None,
        edge_attr: Optional[Union[list, bool]] = None,
    ) -> nx.Graph:
        """ Returns a NetworkX graph object from a Geographic Data File. """
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
                    return pd.read_csv(StringIO(content), quotechar=char, **params)

                except Exception as e:
                    exception += f"\n  {type(e).__name__}: {str(e).rstrip()} ({quote} quotes)"

            raise Exception("unable to read data from file considering both single"
                            f"and double quotes as text delimiter.{exception}")

        # Gather node and edge definitions.
        with open(path, "r") as f:
            nodes, edges = f.read().split("nodedef>", 1)[-1].split("edgedef>", 1)
            nodedef, edgedef = get_def(nodes), get_def(edges)

        # Build node and edge list assuming single or double quotes as text delimiters.
        nodes = get_list(nodes, names=list(nodedef.keys()), dtype=nodedef, header=0, index_col="name")
        edges = get_list(edges, names=list(edgedef.keys()), dtype=edgedef, header=0)

        # Read directed attribute from data if found.
        if directed is None and "directed" in edges.columns:
            if len(edges["directed"].unique()) > 1:
                raise NotImplementedError(
                    "Graphs with both directed and undirected edges are not supported.\n"
                    "Please manually set the 'directed' parameter to True or False to supress this error."
                )
            directed = edges["directed"][0]
            edges.drop("directed", axis=1, inplace=True)

        # Allow multiple edges among nodes if found.
        if multigraph is None:
            multigraph = 1 != edges[[source, target]].value_counts(ascending=True).unique()[-1]

        # Node and edge attributes to consider.
        node_attr = nodes.columns.tolist()\
                    if node_attr in (True, None) else (node_attr or [])

        edge_attr = [_ for _ in edges.columns if _ not in (source, target)]\
                    if edge_attr in (True, None) else (edge_attr or [])

        # Initialize graph object with determined type.
        G = getattr(nx, f"{'Multi' if multigraph else ''}{'Di' if directed else ''}Graph")()

        # Add nodes and edges to graph.
        G.add_nodes_from(list(zip(nodes.index,
                                  nodes.to_dict(orient="records"))))

        G.add_edges_from(list(zip(edges[source],
                                  edges[target],
                                  edges.loc[:, edge_attr].to_dict(orient="records"))))

        # Assign weight to edges.
        if not multigraph:
            weight = pd\
                .DataFrame({"source": edges[source],
                            "target": edges[target],
                            "weight": edges["weight"] if "weight" in edges.columns else 1})\
                .groupby(["source", "target"])\
                .sum("weight")\
                .squeeze("columns")

            if not weight.min() == 1 == weight.max():
                nx.set_edge_attributes(G, weight, "weight")

        return G

    @staticmethod
    def write_gdf(
        G: nx.Graph,
        path: str,
        node_attr: Optional[Union[list, bool]] = None,
        edge_attr: Optional[Union[list, bool]] = None,
    ) -> None:
        types = {value.__name__: key for key, value in TYPES.items()}

        def get_type(series):
            """ Add attribute type to column names. """
            dtype = f"{types.get(series.dtype.__str__().lower().rstrip('0123456789'), 'VARCHAR')}"
            if dtype == "LONG" and all(-M <= m < M for m in (series.min(), series.max())):
                return "INT"
            if dtype == "DOUBLE" and series.astype(str).apply(str.__len__).max() <= 8:
                return "FLOAT"
            return dtype

        def get_columns(df):
            """ Add attribute type to column names. """
            return [f"{column} {get_type(df[column])}" for column in df.columns.tolist()]

        def get_nodes(G):
            """ Build node list with attributes. """
            nodes = pd\
                .DataFrame(
                    dict(G.nodes(data=True)).values(),
                    index=G.nodes(),
                )
            nodes.index.name = f"nodedef>name {get_type(nodes.index)}"

            if node_attr not in (True, None):
                nodes = nodes.loc[:, (node_attr if node_attr else [])]

            nodes.columns = get_columns(nodes)
            return nodes

        def get_edges(G):
            """ Build edge list with attributes. """
            edges = nx.to_pandas_edgelist(G)
            edges.columns = ["edgedef>node1", "node2"] + edges.columns[2:].tolist()

            if edge_attr not in (True, None):
                edges = edges.loc[:, edges.columns[:2].tolist() + (edge_attr if edge_attr else [])]

            if "directed" not in edges.columns and G.is_directed():
                edges["directed"] = G.is_directed()

            edges.columns = get_columns(edges)
            return edges

        # Write nodes and edges to GDF file.
        get_nodes(G).to_csv(path, index=True, quotechar="'", mode="w")
        get_edges(G).to_csv(path, index=False, quotechar="'", mode="a")


read_gdf = GDF.read_gdf
write_gdf = GDF.write_gdf
