#!/bin/bash

echo 'Running tests'
bin/test -s eestec.portal

echo '====== Running ZPTLint ======'
for pt in `find src/eestec/portal/ -name "*.pt"` ; do bin/zptlint $pt; done

echo '====== Running PyFlakes ======'
bin/pyflakes src/eestec/portal
bin/pyflakes setup.py

echo '====== Running pep8 =========='
bin/pep8 --ignore=E501 src/eestec/portal
bin/pep8 --ignore=E501 setup.py

