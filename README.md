# networkx-gdf

Python package to read and write NetworkX graphs as GDF (Graph Data Format).

## Requirements

* **Python>=3.7**
* networkx>=2.1
* pandas>=1.1.0

## Usage

Just two functions are implemented, for reading from and writing data to file.

```
from networkx_gdf import read_gdf, write_gdf

# Builds NetworkX graph object from file.
G = read_gdf("input_file.gdf")

# Writes NetworkX graph object to file.
write_gdf(G, "output_file.gdf)
```

### Detailed usage

A few additional arguments are available both for reading and writing files:

#### Building NetworkX graph object from file

```
G = read_gdf(
    "input_file.gdf",
    # Required; file path to read data from.

    directed=None,
    # Optional; consider graph edges as directed or undirected.
    # True: returns a <nx.DiGraph> or <nx.MultiDiGraph> object.
    # False: returns a <nx.Graph> or <nx.MultiGraph> object.
    # None (default): decides based on "directed" field in file.

    multigraph=None,
    # Optional; consider multiple or single edges among nodes.
    # True: always returns a <nx.MultiGraph> or <nx.MultiDiGraph> object.
    # False: sums edge weights and returns a <nx.Graph> or <nx.DiGraph> object.
    # None (default): only returns a multiplex graph if multiple edges are found.

    node_attr=True,
    # Optional; node attributes to import data from.
    # Accepts either a [list] containing attribute names or a bool (True, False).
    # Defaults to True, which considers all node attributes.

    edge_attr=True,
    # Optional; edge attributes to import data from.
    # Accepts either a [list] containing attribute names or a bool (True, False).
    # Defaults to True, which considers all edge attributes.
)
```

#### Writing NetworkX graph object to file

```
write_gdf(
    G,
    # Required; graph object from NetworkX.

    "output_file.gdf",
    # Required; file path to write data to.

    node_attr=True,
    # Optional; node attributes to export data from.
    # Accepts either a [list] containing attribute names or a bool (True, False).
    # Defaults to True, which considers all node attributes.

    edge_attr=True,
    # Optional; edge attributes to export data from.
    # Accepts either a [list] containing attribute names or a bool (True, False).
    # Defaults to True, which considers all edge attributes.
)
```

### Importing as a class

Alternatively, the module can also be imported as a class, e.g., for inheriting it:

```
from networkx_gdf import GDF

class MyClass(GDF):
    ...
```

___

References
---

* [NetworkX](https://networkx.github.io)
* [Pandas](https://pandas.pydata.org/)
