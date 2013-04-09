# convenience makefile to boostrap & run buildout
# use `make options=-v` to run buildout with extra options
#
# % make bootstrap
# % make
# % make check
# % make docs
#


LOCALISED_SCRIPTS = ipython ipdb flake8 pylint
PROJECT = $(shell basename $(shell pwd))

NIX_PROFILE := $(shell pwd)/nixprofile

OUTER_ENV := PATH=$(PATH) \
	LD_LIBRARY_PATH=$(LD_LIBRARY_PATH) \
	PKG_CONFIG_PATH=$(PKG_CONFIG_PATH) \
	NIX_LDFLAGS=$(NIX_LDFLAGS) \
	NIX_CFLAGS_COMPILE=$(NIX_CFLAGS_COMPILE)

PATH = $(NIX_PROFILE)/bin
LD_LIBRARY_PATH = $(NIX_PROFILE)/lib
PKG_CONFIG_PATH = $(NIX_PFOFILE)/lib/pkgconfig
NIX_LDFLAGS = -L $(NIX_PROFILE)/lib
NIX_CFLAGS_COMPILE = -I $(NIX_PROFILE)/include -I $(NIX_PROFILE)/include/sasl


version = 2.7
python = ./bin/python
options =

### default target

all: buildout


### targets you might want to run

bootstrap: dev.nix requirements.txt setup.py
	${OUTER_ENV} nix-env -p ${NIX_PROFILE} -i dev-env -f dev.nix
	${NIX_PROFILE}/bin/virtualenv --distribute --clear .
	echo ../../../nixprofile/lib/python2.7/site-packages > lib/python2.7/site-packages/nixprofile.pth
	./bin/pip install -r requirements.txt --no-index -f ""
	for script in ${LOCALISED_SCRIPTS}; do ./bin/easy_install -H "" $$script; done
	$(python) bootstrap.py -d

print-syspath:
	$(python) -c 'import sys,pprint;pprint.pprint(sys.path)'

# leaving dependencies in case somebody wants to tune further
# currently, buildout is phony and run anyway if called
buildout: buildout.cfg buildout.d/*.cfg setup.py
	./bin/buildout $(options)

check: tests

coverage: htmlcov/index.html

docs: docs/html/index.html

clean:
	rm -rf .coverage .installed.cfg .mr.developer.cfg bin docs/html htmlcov \
		parts develop-eggs src/eestec.portal.egg-info lib include .Python


### targets needed by the ones you might want to run (see above)

htmlcov/index.html: src/eestec/portal/*.py src/eestecportal/browser/*.py \
		src/eestec/portal/content/*.py src/eestec/portal/tests/ *.py bin/coverage
	./bin/coverage run --source=./src/eestec/portal/ --branch ./bin/test
	./bin/coverage html -i
	@touch $@
	@echo "Coverage report was generated at '$@'."

docs/html/index.html: docs/*.rst src/eestec/portal/*.py src/eestec/portal/browser/*.py \
		src/eestec/portal/tests/*.py bin/sphinx-build
	./bin/sphinx-build docs docs/html
	@touch $@
	@echo "Documentation was generated at '$@'."

tests:
	./bin/test
	./bin/flake8 setup.py
	./bin/flake8 src/eestec/portal
	for pt in `find src/eestec/portal -name "*.pt"` ; do ./bin/zptlint $$pt; done
	for xml in `find src/eestec/portal -name "*.xml"` ; do ./bin/zptlint $$xml; done
	for zcml in `find src/eestec/portal -name "*.zcml"` ; do ./bin/zptlint $$zcml; done

.PHONY: all bootstrap buildout check clean coverage docs print-syspath tests
