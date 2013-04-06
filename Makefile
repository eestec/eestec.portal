# convenience makefile to boostrap & run buildout
# use `make options=-v` to run buildout with extra options

version = 2.7
python = bin/python
options =

all: docs tests

coverage: htmlcov/index.html

htmlcov/index.html: src/eestec/portal/*.py src/eestecportal/browser/*.py \
		src/eestec/portal/content/*.py src/eestec/portal/tests/ *.py bin/coverage
	@bin/coverage run --source=./src/eestec/portal/ --branch bin/test
	@bin/coverage html -i
	@touch $@
	@echo "Coverage report was generated at '$@'."

docs: docs/html/index.html

docs/html/index.html: docs/*.rst src/eestec/portal/*.py src/eestec/portal/browser/*.py \
		src/eestec/portal/tests/*.py bin/sphinx-build
	bin/sphinx-build docs docs/html
	@touch $@
	@echo "Documentation was generated at '$@'."

bin/sphinx-build: .installed.cfg
	@touch $@

.installed.cfg: bin/buildout buildout.cfg buildout.d/*.cfg setup.py
	bin/buildout $(options)

bin/buildout: $(python) buildout.cfg bootstrap.py
	$(python) bootstrap.py -d
	@touch $@

$(python):
	virtualenv -p python$(version) --no-site-packages .
	@touch $@

tests: .installed.cfg
	@bin/test
	@bin/flake8 setup.py
	@bin/flake8 src/eestec/portal
	@for pt in `find src/eestec/portal -name "*.pt"` ; do bin/zptlint $$pt; done
	@for xml in `find src/eestec/portal -name "*.xml"` ; do bin/zptlint $$xml; done
	@for zcml in `find src/eestec/portal -name "*.zcml"` ; do bin/zptlint $$zcml; done

clean:
	@rm -rf .coverage .installed.cfg .mr.developer.cfg bin docs/html htmlcov \
	    parts develop-eggs src/eestec.portal.egg-info lib include .Python

.PHONY: all docs tests clean