#!/bin/sh

# A cronjob script that re-creates demo.eestec.net every night

git clone git://github.com/eestec/eestec.portal.git
cd eestec.portal
virtualenv-2.6 --no-site-packages .
bin/python2.6 bootstrap.py
bin/buildout -c demo.cfg
bin/instance start

