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
* ``Python 2.7`` - Plone 4.2 does NOT work with other Python version so you need
  this exact version.
* development headers for libxml2, libxslt and python

Python tools
------------

Then you'll also need to install some Python specific tools:

* easy_install - the Python packaging system (download
  http://peak.telecommunity.com/dist/ez_setup.py and run
  ``sudo python ez_setup.py``.
* virtualenv - a tool that assists in creating isolated Python working
  environments.


Code style guide
----------------

We use the ``plone.api`` style guide so please read it and use it:
http://ploneapi.readthedocs.org/en/latest/contribute/conventions.html


Further information
-------------------

If you experience problems read through the following links as almost all of the
above steps are required for a default Plone development environment:

* http://plone.org/documentation/tutorial/buildout
* http://pypi.python.org/pypi/zc.buildout/
* http://pypi.python.org/pypi/setuptools
* http://plone.org/documentation/manual/installing-plone

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
environment and build the development environment.

.. sourcecode:: bash

    [you@local work]$ cd eestec.portal
    [you@local eestec.portal]$ make

Internally, this uses `zc.buildout` to build Zope and any other servers we
might need, fetches all dependencies and installs them, generates config files
and scripts, prepares deployment tools and much more. Read more about buildout
at http://plone.org/documentation/tutorial/buildout:

While buildout is running go make some tea. When you run it for the first time
it needs a couple of minutes to finish preparing your development environment.
More if you have a slower Internet connection.

After ``make`` is finished your development environment is ready! You have
more make command on your disposal:

.. sourcecode:: bash

    [you@local eestec.portal]$ make tests  # run all unit tests
    [you@local eestec.portal]$ make docs  # generate documentation
    [you@local eestec.portal]$ make clean && make  # start from scratch


.. _starting-the-portal:

Starting the portal
===================

Let's start Zope - the application server. There are several ways to start Zope.
For development purposes we'll use the 'foreground' mode which starts Zope in
console's foreground so you can immediately see all debug messages and use the
Python Debugger to interactively debug your code:

.. sourcecode:: bash

    [you@local eestec.portal]$ bin/instance fg


Once Zope has started you need to add a Plone site. Open up a browser and
point it to ``http://localhost:8080/@@plone-addsite?site_id=Plone``. Username
is ``admin``, password is also ``admin``. Check the ``eestec.portal`` checkbox
in the `Add-ons` list and click ``Create Plone Site``.

There you go, a local installation of the EESTEC portal on your laptop. Go
nuts with it!

You can also run our :ref:`unit-tests` or perform :ref:`syntax-validation`.


.. _adding-initial-content:

Adding initial content
======================

If you don't have a ZODB to work with, as in, you are starting with a fresh
install of Plone, follow this steps to add some content to your site so you
can see what your code does:

#. Follow the :ref:`starting-the-portal` instructions above.
#. Use the ``Add new ...`` drop down menu to add a new ``LC``.
#. Once inside the new LC, use the ``Add new ...`` drop down menu again, this
   time to add a new ``Event``.
#. Once inside the new Event, use the ``Add new ...`` drop down menu for the
   last time, now to add a new ``Event Application``.
#. Use the ``State:`` drop-down menu to play around with different items'
   workflow states.


.. _working-on-an-issue:

Working on an issue
===================

Out GitHub account contains a `list of open issues
<https://github.com/eestec/eestec.portal/issues>`_. Click on one that is labeled
with a green ``entry-level`` tag. If the issue description says ``No one is
assigned`` it means no-one is already working on it and you can claim it as your
own. Click on the button next to the text and make yourself the one assigned
for this issue.

Based on our :ref:`git_workflow` all new features must be developed in separate
git branches. So if you are not doing a simple bugfix, but rather adding new
features/enhancements, you should create a *feature branch*. This way your work
is kept in an isolated place where you can receive feedback on it, improve it,
etc. Once we are happy with your implementation, your branch gets merged into
*master* at which point everyone else starts using your code.

.. sourcecode:: bash

    [you@local eestec.portal]$ git checkout master  # go to master branch
    [you@local eestec.portal]$ git checkout -b issue_17  # create a feature branch
    # replace 17 with the issue number you are working on

    # change code here

    [you@local eestec.portal]$ git add -p && git commit  # commit my changes
    [you@local eestec.portal]$ git push origin issue_17  # push my branch to GitHub
    # at this point other can see your changes but they don't get effected by
    them; in other words, others can comment on your code without your code
    changing their development environments

Read more about Git branching at http://learn.github.com/p/branching.html. Also,
to make your git nicer, we have a :ref:`unit-tests` chapter in *Tips &
Tricks.*

Also please add your name to the
`Changelog <https://github.com/eestec/eestec.portal/blob/master/docs/HISTORY.rst>`_

Once you are done with your work and you would like us to merge your changes
into master, go to GitHub to do a *pull request*. Open a browser and point it to
https://github.com/eestec/eestec.portal/tree/issue_<ISSUE_NUMBER>. There you
should see a ``Pull Request`` button. Click on it, wrote some text what you
did and anything else you would like to tell the on who will merge your branch,
and finally click ``Send pull request``. Now wait that someone comes by and
merges your branch (don't do it yourself, even if you have permissions to do
so).

An example pull request text::

    Please merge my branch that resolves issue #13.

