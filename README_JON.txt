==============
README_JON.txt
==============

Jon:

Your two Python source code files have been joined by more stuff.

.. This document was written in ReSTructured text format.
   Mostly, it looks like plain text.  This is a comment.
   
   Here are acouple helpful links:
   http://sphinx-doc.org/rest.html
   https://en.wikipedia.org/wiki/ReStructuredText

Regards,
   Pete

Directory Structure
-------------------

* ./docs	 - Sphinx documentation
* ./srange	 - Python srange project with your source code
* ./setup.py	 - Python packaging configuration file
* ./README.rst   - Text file (ReSTructured text format), describes this stuff
* ./MANIFEST.in  - used by packaging to include files normally missed
* ./VERSION	 - one way to easily share this number amongst the various parts
* ./srange/LICENSE.txt - standard ANL open source software license

Packaging
---------

Much can be written here.  Two basic commands::

  python ./setup.py sdist      # builds a source .tar.gz file for upload to PyPI
  python ./setup.py install    # installs this project into your python

Documentation
-------------

* ./docs/source/       - Documentation source code files (ReSTructured text format)
* ./docs/Makefile      - procedures to build the HTML, PDF, ...
* ./docs/make.bat      - Windows version of Makefile (keep it)
* ./docs/build         - contains built documentation

How to build the docs
~~~~~~~~~~~~~~~~~~~~~

Go into the projects ``docs`` directory and type::

    make html

The built documentation will appear in a new directory ``build/html``.
This directory is a complete web site.  Open the ``index.html``
to browse the documentation.

Documentation Source
~~~~~~~~~~~~~~~~~~~~

in the ``./docs/source``` directory:

* ./docs/source/conf.py     - Sphinx configuration used to build the documentation
* ./docs/source/index.rst   - documentation "home page"
* ./docs/source/_static     - used by Sphinx
* ./docs/source/_templates  - used by Sphinx

TODO
----

* Python source code: that's up to you, no comments reported by Sphinx
* add copyright to all source code modules
* revise .setup.py
* revise ./docs/source/conf.py
* revise ./docs/source/index.rst
* put project under public version control
* register with Python Package Index as a user
* upload project to PyPI
* register with readthedocs.org as a user
* configure documentation for publication at readthedocs.org

revisions to setup.py
~~~~~~~~~~~~~~~~~~~~~
* short and long descriptions
* url (for home page or documentation)
* download_url
* classifiers

revisions to docs/source/conf.py
~~~~~~~~~~~~~~~~~~~~~

====   =================================
line   variable declaration
====   =================================
47     copyright
97     html_theme
188    latex_documents
====   =================================
