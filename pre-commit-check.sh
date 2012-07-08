#!/bin/bash

echo 'Running tests'
bin/test -s eestec.portal

echo '====== Running ZPTLint ======'
for pt in `find src/eestec/portal/ -name "*.pt"` ; do bin/zptlint $pt; done
for xml in `find src/eestec/portal/ -name "*.xml"` ; do bin/zptlint $xml; done
for zcml in `find src/eestec/portal/ -name "*.zcml"` ; do bin/zptlint $zcml; done

echo '====== Running PyFlakes ======'
bin/zopepy setup.py flakes

echo '====== Running pep8 =========='
bin/pep8 --ignore=E501 src/eestec/portal
bin/pep8 --ignore=E501 setup.py

