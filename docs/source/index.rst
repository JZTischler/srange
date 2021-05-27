srange - Specify complex integer ranges through strings
=======================================================

`srange` is a small package that allows you to specify and iterate over
ranges of integers via a string representing this range.


Package contents:
~~~~~~~~~~~~~~~~~

There are two separate modules available in `srange`:

======================== ===================================================
module                   description
======================== ===================================================
:mod:`srange.srange`     Express complex integer ranges in a string format and iterate over them
:mod:`srange.symrange`   Loop symmetrically outward from 0 alternating positive and negative values: 0, -1, 1, -2, 2, ...
======================== ===================================================


Installation
~~~~~~~~~~~~

The `srange` package is provided for easy installation with conda:

.. code-block:: bash

   conda install -c schlepuetz srange


Documentation contents:
~~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 1

   srange/index
   license


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
