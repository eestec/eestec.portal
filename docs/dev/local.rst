=============================
Local development environment
=============================

This section is meant for developers on the eestec.net project. It's purpose is
to guide them through the steps needed to start contributing.

.. note ::: This HowTo is written for Linux and OS X users. If you're are
   running Windows I suggest using VMWare or a similar Virtualization product to
   install Ubuntu Linux on a virtual machine or installing Ubuntu Linux as a
   secondary OS on your machine. Alternatively, you can browse Plone's
   documentation on how to get Plone development environment up and running on
   Windows. Plone does run on Windows but it's not completely trivial to set it
   up.

Prerequisites
=============

System libraries
----------------

First let's look at 'system' libraries and applications that are normally
installed with your OS packet manager, such as apt, aptitude, yum, etc.:

* ``libxml2`` - an xml parser written in C
* ``libxslt`` - XSLT library written in C
* ``pcre`` - Perl regex libraly
* ``git`` - version control system.
* ``gcc`` - the GNU Compiler Collection.
* ``g++`` - the C++ extensions for gcc.
* ``GNU make`` - the fundamental build-control tool.
* ``GNU tar`` - the (un)archiving tool for extracting downloaded archives.
* ``bzip2`` and ``gzip`` decompression packages - ``gzip`` is nearly standard,
  however some platforms will require that ``bzip2`` be installed.
* ``Python 2.6`` - Plone 4.2 does NOT work with other Python version so you need
  this exact version.


Python tools
------------

Then you'll also need to install some Python specific tools:

* easy_install - the Python packaging system (download
  http://peak.telecommunity.com/dist/ez_setup.py and run
  ``sudo python ez_setup.py``.
* virtualenv - a tool that assists in creating isolated Python working
  environments.


Further information
-------------------

If you experience problems read through the following links as almost all of the
above steps are required for a default Plone development environment:

* http://plone.org/documentation/tutorial/buildout
* http://pypi.python.org/pypi/zc.buildout/
* http://pypi.python.org/pypi/setuptools
* http://plone.org/documentation/tutorial/installing-plone-3-with-the-unified-installer

If you are an OS X user, you first need a working Python implementation (the one
that comes with the operating system is broken). Use
https://github.com/collective/buildout.python and be happy. Also applicable to
other OSes, if getting a working Python proves a challenge.


Creating the development environment
====================================

Go to your home folder or a folder you use for development and `clone` latest
``eestec.portal`` code:

.. sourcecode:: bash

    [you@local ~]$ cd <your_work_folder>
    [you@local work]$ git clone https://github.com/eestec/eestec.portal.git

Now `cd` into the newly created directory and create an isolated python
environment:

.. sourcecode:: bash

    [you@local work]$ cd eestec.portal
    [you@local eestec.portal]$ virtualenv -p python2.6 --no-site-packages ./

    # OS X users using collective.buildout.python would run the following
    [you@local eestec.portal]$ <path>/<to>/<collective.buildout.python>/bin/virtualenv-2.6 --no-site-packages ./

Confirm you are indeed using Python 2.6:

.. sourcecode:: bash

    [you@local eestec.portal]$ bin/python -V
    Python 2.6.7

Bootstrap tools and scripts in ``bin/``:

.. sourcecode:: bash

    [you@local eestec.portal]$ bin/python bootstrap.py

Buildout builds Zope and any other servers we might need, fetches all
dependencies and installs them, generates config files and scripts, prepares
deployment tools and much more. Read more about buildout at
http://plone.org/documentation/tutorial/buildout:

.. sourcecode:: bash

    [you@local eestec.portal]$ bin/buildout

Make tea. Buildout needs a couple of minutes to finish preparing your
development environment.


Starting the portal
===================

Let's start Zope - the application server. There are several ways to start Zope.
For development purposes we'll use the 'foreground' mode which starts Zope in
console's foreground so you can immediately see all debug messages and use the
Python Debugger to interactively debug your code:

.. sourcecode:: bash

    [you@local eestec.portal]$ bin/zope fg


Once Zope has started you need to add a Plone site. Open up a browser and
point it to ``http://localhost:8080/@@plone-addsite?site_id=Plone``. Username
is ``admin``, password is also ``admin``. Check the ``eestec.portal`` checkbox
in the `Add-ons` list and click ``Create Plone Site``.

There you go, a local installation of the EESTEC portal on your laptop. Go
nuts with it!

