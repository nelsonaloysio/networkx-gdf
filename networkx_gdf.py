from io import StringIO
from abc import abstractmethod
from typing import Optional, Union

import networkx as nx
import pandas as pd

TYPES = {
    "VARCHAR": str,
    "INT": int,
    "DOUBLE": float,
    "FLOAT": float,
    "BOOLEAN": bool,
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
    ) -> nx.Graph:
        """ Returns a NetworkX graph object from a Geographic Data File. """
        source, target = "node1", "node2"

        def get_def(content):
            return {
                field[0]:
                    TYPES.get(field[1], str)
                for field in [
                    tuple(_.rsplit(" ", 1))
                    for _ in content.split("\n", 1)[0].split(">", 1)[-1].split(",")
                ]
            }

        # Gather node and edge definitions.
        with open(path, "r") as f:
            nodes, edges = f.read().split("nodedef>", 1)[-1].split("edgedef>", 1)
            nodedef, edgedef = get_def(nodes), get_def(edges)
            nodes = pd.read_csv(StringIO(nodes), names=list(nodedef.keys()), dtype=nodedef, header=0, index_col="name")
            edges = pd.read_csv(StringIO(edges), names=list(edgedef.keys()), dtype=edgedef, header=0)

        # Read directed attribute from data if found.
        if directed is None and "directed" in edges.columns:
            directed = edges["directed"][0]

            if len(edges["directed"].unique()) > 1:
                raise NotImplementedError("Graphs with both directed and undirected edges are not supported.")

        # Allow multiple edges among nodes if found.
        if multigraph is None:
            multigraph = 1 != edges[[source, target]].value_counts(ascending=True).unique()[-1]

        # Object type to build graph with.
        create_using = nx.DiGraph() if directed else nx.Graph()
        if multigraph:
            create_using = nx.MultiDiGraph() if directed else nx.MultiGraph()

        # List of edge attributes.
        if edge_attr is True:
            edge_attr = [_ for _ in edges.columns.tolist() if _ not in (source, target)]

        # Consider edge weights.
        if not multigraph and "weight" not in edges.columns:
            edge_attr = ["weight"] + (edge_attr if edge_attr else [])
            weights = edges[[source, target]].value_counts()

            with pd.option_context("mode.chained_assignment", None):
                edges["weight"] = [weights.loc[x, y] for x, y in zip(edges[source], edges[target])]

        # Convert edge list to graph.
        G = nx\
            .convert_matrix\
            .from_pandas_edgelist(
                edges,
                source=source,
                target=target,
                edge_attr=list(edges.columns)[2:] if edge_attr == True else (edge_attr or None),
                create_using=create_using
        )

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
    ):
        types = {value.__name__: key for key, value in TYPES.items()}

        def get_columns(df):
            """ Add attribute type to column names. """
            return [f"{key} {types.get(value.__str__().rstrip('0123456789'), 'VARCHAR')}"
                    for key, value in df.dtypes.to_dict().items()]

        def get_nodes(G):
            """ Build node list with attributes. """
            nodes = pd\
                .DataFrame(
                    dict(G.nodes(data=True)).values(),
                    index=G.nodes(),
                )\
                .astype(
                    int,
                    errors="ignore"
                )
            nodes.index.name = "nodedef>name VARCHAR"

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

            edges.columns = get_columns(edges)
            return edges

        # Write nodes and edges to GDF file.
        get_nodes(G).to_csv(path, index=True, mode="w")
        get_edges(G).to_csv(path, index=False, mode="a")


read_gdf = GDF.read_gdf
write_gdf = GDF.write_gdf
