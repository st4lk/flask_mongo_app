SERVER_HOST ?= 0.0.0.0
FLASK_APP ?= music_app
FLASK_ENV ?= development
ENV ?= venv

shell:
	bash

install: .install
.install: requirements/main.txt
	$(ENV)/bin/pip install -r requirements/main.txt
	touch $@

install-test: .install-test
.install-test: requirements/tests.txt
	$(ENV)/bin/pip install -r requirements/tests.txt
	touch $@

devserver: install
	FLASK_APP=$(FLASK_APP) FLASK_ENV=$(FLASK_ENV) $(ENV)/bin/flask run --host=$(SERVER_HOST)

command: install
	FLASK_APP=$(FLASK_APP) FLASK_ENV=$(FLASK_ENV) $(ENV)/bin/flask $(COMMAND)

test: install install-test
	$(ENV)/bin/python -m pytest $(TEST_ARGS)
