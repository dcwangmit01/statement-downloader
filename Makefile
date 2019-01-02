PYTHON ?= python

venv:
	if [ ! -d .venv ] ; then \
	  virtualenv -p python3 .venv; \
	fi

install:
	pip install --editable .

pep8:
	yapf --style='{based_on_style: pep8, column_limit: 119}' -i $$(find * -type f -name '*.py')
	flake8 --max-line-length=119 ./app ./tests

test: pep8
	pip -q install -r test-requirements.txt
	pytest

dist: clean
	(cd $(BASE) && $(PYTHON) setup.py sdist)

clean:
	find * -type f -name *.pyc | xargs rm -f
	find * -type f -name *~ |xargs rm -f
	find * -type d -name __pycache__ |xargs rm -rf
	rm -rf *.egg-info
	rm -rf dist/
	rm -f *.csv
