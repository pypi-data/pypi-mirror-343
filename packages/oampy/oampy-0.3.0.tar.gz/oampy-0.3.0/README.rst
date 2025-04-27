=====
oampy
=====

``oampy`` is a Python package and command line tool that allows to access data
from the Open Access Monitor (OAM), which is run by Forschungszentrum Jülich.

Installation
============

... via PyPI
~~~~~~~~~~~~

.. code-block:: bash

   pip install oampy

Prerequisite
============

Create an environment variable ``OAM_EMAIL`` with your email address. If the
variable isn’t created before using this package, your ``username@hostname``
will be used to populate the user agent field in the request headers instead.
Since `version 2.1 <https://open-access-monitor.de/notes>`_ you need a token to
use the API. Therefore, you must create an environment variable ``OAM_TOKEN``
with your token.
See also `Usage Terms`_ below.

Usage Examples
==============

Command Line
~~~~~~~~~~~~

.. code-block:: shell

    # set environment variable OAM_EMAIL
    export OAM_EMAIL="researcher@institution.org"
    # set environment variable OAM_TOKEN
    export OAM_TOKEN="YOUR_SECRET_OAM_API_TOKEN"
    # fetch metadata of journal given by ISSN
    oampy journal "0360-4012"
    # fetch metadata of publication given by DOI
    oampy publication "10.1007/s11263-011-0505-4"

Interpreter
~~~~~~~~~~~

.. code-block:: python

    # import package os
    import os
    # set environment variable OAM_EMAIL
    os.environ["OAM_EMAIL"] = "researcher@institution.org"
    # set environment variable OAM_TOKEN
    os.environ["OAM_TOKEN"] = "YOUR_SECRET_OAM_API_TOKEN"
    # import package oampy
    import oampy
    # fetch metadata of journal
    journal = oampy.get_journal("0360-4012")
    # fetch metadata of publication
    publication = oampy.get_publication("10.1007/s11263-011-0505-4")

Usage Terms
===========

Open Access Monitor
~~~~~~~~~~~~~~~~~~~

    The database of the Open Access Monitor Germany is published under the Open Database License 1.0.

    The data can be reused under the following conditions:

    - Reuse of larger amounts of data and use of the API: please contact us.
    - Reuse of the data by download via the OAM application: CC BY 4.0

    https://open-access-monitor.de
