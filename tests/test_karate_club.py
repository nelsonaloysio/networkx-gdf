#!/usr/bin/env python

import logging as log
from argparse import ArgumentParser
from io import BytesIO, StringIO
from os import remove

import networkx as nx
from networkx_gdf import GDF, read_gdf, write_gdf

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def test_karate_club_graph(*args, **kwargs) -> None:
    assert GDF.read_gdf == read_gdf
    assert GDF.write_gdf == write_gdf

    G = nx.karate_club_graph()
    log.debug(G)

    # G -> file -> G
    log.info("G -> graph.gdf -> G")
    write_gdf(G, "graph.gdf")
    G_ = read_gdf("graph.gdf")
    log.debug(G_)
    assert G.order() == G_.order()
    assert G.size() == G_.size()

    # G -> file -> G
    log.info("G -> open(graph.gdf) -> G")
    with open("graph.gdf", "wb") as f:
        write_gdf(G, f)
    with open("graph.gdf", "rb") as f:
        G_ = read_gdf(f)
    assert G.order() == G_.order()
    log.debug(G_)
    assert G.size() == G_.size()
    remove("graph.gdf")

    # G -> BytesIO -> G
    log.info("G -> BytesIO -> G")
    bio = BytesIO()
    write_gdf(G, bio)
    G_ = read_gdf(bio)
    log.debug(G_)
    assert G.order() == G_.order()
    assert G.size() == G_.size()

    # G -> StringIO -> G
    log.info("G -> StringIO -> G")
    sio = StringIO()
    write_gdf(G, sio)
    G_ = read_gdf(sio)
    log.debug(G_)
    assert G.order() == G_.order()
    assert G.size() == G_.size()


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("--log-level",
                        choices=["debug", "info", "warning", "error", "critical", "notset"],
                        help="Set the logging level.")

    args = parser.parse_args()
    log_level = args.__dict__.pop("log_level")

    if log_level is not None:
        log.basicConfig(format=LOG_FORMAT, level=getattr(log, log_level.upper()))

    test_karate_club_graph(**vars(args))
    print("All tests passed!")
