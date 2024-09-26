.. toctree::
   :hidden:
   :caption: Introduction

   Overview <self>

.. toctree::
   :hidden:
   :caption: Main documentation

   api

.. note::

   This documentation was generated on |today| for package release |release|.


############
networkx-gdf
############

.. image:: https://badge.fury.io/py/networkx-gdf.svg
   :target: https://pypi.org/project/networkx-gdf/
   :alt: PyPI version

.. image:: https://readthedocs.org/projects/networkx-gdf/badge/?version=latest
   :target: https://networkx-gdf.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://static.pepy.tech/badge/networkx-gdf
   :target: https://pepy.tech/project/networkx-gdf?versions=*
   :alt: Downloads

.. image:: https://static.pepy.tech/badge/networkx-gdf/month
   :target: https://pepy.tech/project/networkx-gdf?versions=*
   :alt: Downloads

.. image:: https://img.shields.io/pypi/l/networkx-gdf
   :target: https://github.com/nelsonaloysio/networkx-gdf/blob/main/LICENSE.md
   :alt: License


**NetworkX-GDF** extends the `NetworkX <https://networkx.org>`__ library to support GDF (Graph Data
Format) files.

It provides two functions to read and write GDF files, which are used to store graph data in a
tabular format. The package is designed to be lightweight on requirements and easy to use.

Install
=======

The package supports **Python 3.7++** and is readily available from `PyPI <https://pypi.org/project/networkx-gdf/>`_:

.. code-block:: bash

   $ pip install networkx-gdf


Quick start
===========

The following is a quick example of the package in action, covering its basic functionality.

.. code-block:: python

   >>> from networkx_gdf import read_gdf, write_gdf
   >>>
   >>> # Reads NetworkX graph object from file.
   >>> G = read_gdf("input_file.gdf")
   >>>
   >>> # Writes NetworkX graph object to file.
   >>> write_gdf(G, "output_file.gdf")

For details on the functions above and the package's usage, please refer to the
`API Reference <api.html>`__ page.

.. seealso::

   The package's `GitHub repository <https://github.com/nelsonaloysio/networkx-gdf>`__
   for the latest updates and issues. Contributions are welcome!


Cite
====

If this package is useful for your research, please kindly consider citing the
`NetworkX paper <https://conference.scipy.org/proceedings/scipy2008/paper_2/>`__:

   Hagberg, Aric A., Schult, Daniel A., Swart, Pieter J. (2008).
   ''Exploring Network Structure, Dynamics, and Function using NetworkX''.
   In: Proceedings of the 7th Python in Science Conference (SciPy2008).
   Pasadena (CA), USA, August 2008.

.. code-block:: tex

   @inproceedings{networkx2008,
      author    = {Aric A. Hagberg and Daniel A. Schult and Pieter J. Swart},
      title     = {Exploring Network Structure, Dynamics, and Function using NetworkX},
      booktitle = {Proceedings of the 7th Python in Science Conference},
      pages     = {11--15},
      address   = {Pasadena, CA USA},
      year      = {2008},
      editor    = {Ga\"el Varoquaux and Travis Vaught and Jarrod Millman},
      url       = {https://conference.scipy.org/proceedings/scipy2008/paper_2/},
   }
