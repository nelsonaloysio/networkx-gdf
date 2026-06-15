#!/usr/bin/env python

from io import StringIO, BytesIO
from os import remove

from networkx_gdf import GDF, read_gdf, write_gdf

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

GRAPH = """
nodedef>name VARCHAR,label VARCHAR
A,Node A
B,Node B
edgedef>node1 VARCHAR,node2 VARCHAR,directed BOOLEAN
A,B,True
A,B,True
"""


def test_networkx_gdf():
    gdf = GDF()
    assert GDF.read_gdf == read_gdf
    assert gdf.read_gdf == read_gdf
    assert GDF.write_gdf == write_gdf
    assert gdf.write_gdf == write_gdf

    path = "test.gdf"
    with open(path, "w") as f:
        f.write(GRAPH)

    for file in (path, StringIO(GRAPH), BytesIO(GRAPH.encode())):
        G = read_gdf(file)
        assert G.order() == 2
        assert G.size() == 2
        assert G.is_directed() == True
        assert G.is_multigraph() == True
        assert G.nodes["A"]["label"] == "Node A"
        assert G.nodes["B"]["label"] == "Node B"

    sio, bio = StringIO(), BytesIO()
    with open(path, "w") as f:
        for file in (path, f, sio, bio):
            write_gdf(G, file)
    with open(path, "r") as f:
        assert GRAPH.lstrip() == f.read() == sio.read() == bio.read().decode()

    G = read_gdf(path, directed=False)
    assert G.is_directed() == False

    G = read_gdf(path, multigraph=False)
    assert G.is_multigraph() == False
    assert G.edges["A", "B"]["weight"] == 2

    try:
        read_gdf(StringIO(GRAPH.replace("True", "False", 1)))
    except NotImplementedError:
        pass

    remove("test.gdf")


if __name__ == "__main__":
    test_networkx_gdf()
    print("All tests passed!")
