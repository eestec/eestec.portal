=============
Tips & Tricks
=============

Tunneling to ETHZ server
========================

Sometimes you need direct access to services running on ETHZ server. All servers
are running on local address ``127.0.0.2``, and the ports for them are as
follows::

    zope1       = 8091
    zope2       = 8092
    zope3       = 8093
    zope4       = 8094
    zope4_debug = 8099 (needs to be manually started with ``bin/zope_debug fg``)
    zeo         = 8090
    haproxy     = 8080
    supervisor  = 9000


So, to access (for example) ``zope_debug`` use:

    $ ssh eestecwm@galen.ee.ethz.ch -L 8099:127.0.0.2:8099

Then open ``http://localhost:8099`` in your browser and you will directly access
the service on this port.

Setting up Git
==============

Git is a very useful tool, especially when you configure it to your needs. Here
are a couple of tips.

Enhanced git prompt
-------------------

Do one (or more) of the following:
 * http://clalance.blogspot.com/2011/10/git-bash-prompts-and-tab-completion.html
 * http://en.newinstance.it/2010/05/23/git-autocompletion-and-enhanced-bash-prompt/
 * http://gitready.com/advanced/2009/02/05/bash-auto-completion.html


Example of ``~/.gitconfig``
---------------------------

.. sourcecode:: ini

    [user]
        name = John Smith
        email = john.smith@gmail.com
    [diff "cfg"]
        funcname = ^\\(\\[.*\\].*\\)$
    [color]
        diff = auto
        status = auto
        branch = auto
    [alias]
        st = status
        ci = commit
        br = branch
        co = checkout
    [core]
        excludesfile = /home/jsmith/.gitignore
        editor = nano
    [github]
        user = jsmith
        token = <token_here>

Example of ``~/.gitignore``
---------------------------

.. sourcecode:: ini

    # Compiled source #
    ###################
    *.com
    *.class
    *.dll
    *.exe
    *.o
    *.so
    *.lo
    *.la
    *.rej
    *.pyc
    *.pyo

    # Packages #
    ############
    # it's better to unpack these files and commit the raw source
    # git has its own built in compression methods
    *.7z
    *.dmg
    *.gz
    *.iso
    *.jar
    *.rar
    *.tar
    *.zip

    # Logs and databases #
    ######################
    *.log
    *.sql
    *.sqlite

    # OS generated files #
    ######################
    .DS_Store
    .DS_Store?
    ehthumbs.db
    Icon?
    Thumbs.db

    # Python projects related #
    ###########################
    *.egg-info
    Makefile
    .egg-info.installed.cfg
    *.pt.py
    *.cpt.py
    *.zpt.py
    *.html.py
    *.egg

