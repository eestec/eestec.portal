#!/bin/bash

function handle_exit {
    if [ $? -ne 0 ]; then
        EXITCODE=1
    fi
}

EXITCODE=0

echo 'Running tests'
bin/test; handle_exit

echo '====== Running ZPTLint ======'
for pt in `find src/eestec/portal/ -name "*.pt"` ; do bin/zptlint $pt; done
for xml in `find src/eestec/portal/ -name "*.xml"` ; do bin/zptlint $xml; done
for zcml in `find src/eestec/portal/ -name "*.zcml"` ; do bin/zptlint $zcml; done

echo '====== Running PyFlakes ======'
bin/zopepy setup.py flakes; handle_exit

echo '====== Running pep8 =========='
bin/pep8 --ignore=E501 src/eestec/portal; handle_exit
bin/pep8 --ignore=E501 setup.py; handle_exit

if [ $EXITCODE -ne 0 ]; then
    exit 1
fi