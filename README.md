# networkx-gdf

Python package to read and write NetworkX graphs as GDF (Graph Data Format).

GDF is a compact file format originally implemented by [GUESS](http://graphexploration.cond.org). Although the software itself is not anymore maintained, the format is still supported by active open-source projects such as [Gephi](https://gephi.org/) (see details [here](https://gephi.org/users/supported-graph-formats/gdf-format/)).

## Requirements

* **Python>=3.7**
* networkx>=2.1
* pandas>=1.1.0

## Install

Package is available to install on [PyPI](https://pypi.org/project/networkx-gdf/):

```bash
pip install networkx-gdf
```

## Usage

Just two functions are implemented, for reading from and writing data to file.

```python
from networkx_gdf import read_gdf, write_gdf

# Builds NetworkX graph object from file.
G = read_gdf("input_file.gdf")

# Writes NetworkX graph object to file.
write_gdf(G, "output_file.gdf")
```

### Detailed usage

A few additional arguments are available both for reading and writing files:

#### Building NetworkX graph object from file

```python
G = read_gdf(
    "input_file.gdf",
    # Required; file path to read data from.

    directed=None,
    # Optional; consider edges as directed or undirected.
    # True: returns a <nx.DiGraph> or <nx.MultiDiGraph> object.
    # False: returns a <nx.Graph> or <nx.MultiGraph> object.
    # None (default): decides based on "directed" edge attribute in file.

    multigraph=None,
    # Optional; consider multiple or single edges among nodes.
    # True: always returns a <nx.MultiGraph> or <nx.MultiDiGraph> object.
    # False: sums edge weights and returns a <nx.Graph> or <nx.DiGraph> object.
    # None (default): decides based on number of edges among the same pair of nodes.

    node_attr=None,
    # Optional; node attributes to import data from.
    # Accepts either a list containing attribute names or a boolean (True, False).
    # Defaults to True, which considers all node attributes.

    edge_attr=None,
    # Optional; edge attributes to import data from.
    # Accepts either a list containing attribute names or a boolean (True, False).
    # Defaults to True, which considers all edge attributes.
)
```

#### Writing NetworkX graph object to file

```python
write_gdf(
    G,
    # Required; graph object from NetworkX.

    "output_file.gdf",
    # Required; file path to write data to.

    node_attr=None,
    # Optional; node attributes to export data from.
    # Accepts either a list containing attribute names or a boolean (True, False).
    # Defaults to True, which considers all node attributes.

    edge_attr=None,
    # Optional; edge attributes to export data from.
    # Accepts either a list containing attribute names or a boolean (True, False).
    # Defaults to True, which considers all edge attributes.
)
```

Note that any object types beyond integers/longs, floats/doubles, and booleans will be considered as strings.

### Importing as a class

Alternatively, the module can also be imported as a class and inherited:

```python
from networkx_gdf import GDF

class MyClass(GDF):
    ...

G = MyClass.read_gdf("input_file.gdf")
MyClass.write_gdf(G, "output_file.gdf")
```

Both functions are implemented as static methods, so initializing the class as an object is not required.

___

### References

* [NetworkX](https://networkx.github.io)
* [Pandas](https://pandas.pydata.org/)
