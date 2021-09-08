MODULE_NAME ?= hemlock
PORT_DOCS ?= 8020
PORT_TEST ?= 8080
REPORTS_DIR ?= reports
SPHINX_SOURCE_DIR ?= docs
SPHINX_BUILD_DIR ?= docs/_build
SRC_DIR ?= src

# Format the src directory with black
.PHONY: format
format:
	black ${SRC_DIR}

# Run unit tests, produce a coverage report, and serve it as a web page
.PHONY: test
test:
	mkdir -p ${REPORTS_DIR}
	tox -- --source=${MODULE_NAME} > ${REPORTS_DIR}/test.txt
	coverage html -d ${REPORTS_DIR}/coverage
	coverage report
.PHONY: testserve
testserve:
	python -m http.server ${PORT_TEST} -d ${REPORTS_DIR}/coverage

# Lint the source directory with pylint
.PHONY: lint
lint:
	mkdir -p ${REPORTS_DIR}
	pylint ${SRC_DIR} --reports=y > ${REPORTS_DIR}/lint.txt

# Run typehint checks with mypy
.PHONY: typehint
typehint:
	mkdir -p ${REPORTS_DIR}
	mypy ${SRC_DIR} > ${REPORTS_DIR}/typehint.txt

# Make sphinx docs, run doctests, and serve docs as a web page
.PHONY: docmake
docmake:
	python setup.py build_sphinx\
		--source ${SPHINX_SOURCE_DIR}\
		--build-dir ${SPHINX_BUILD_DIR}
.PHONY: doctest
doctest:
	sphinx-build ${SPHINX_SOURCE_DIR} ${REPORTS_DIR} -b doctest
.PHONY: docserve
docserve:
	python -m http.server ${PORT_DOCS} -d ${SPHINX_BUILD_DIR}/html
.PHONY: docs
docs: docmake doctest

# Run formatting, unit tests, linting, typehints, and doc creation
.PHONY: pipeline
pipeline: format test lint typehint docs
