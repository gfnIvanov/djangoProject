.PHONY: dev install

ENGINE = venv/bin/python
ENGINE_SETUP = venv/bin/pip
PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
VENV_EXISTS := $(shell which venv/bin/python)

check_venv:
ifneq ($(ENGINE),$(VENV_EXISTS))
	$(error Virtualenv is not created)
endif

dev: check_venv
	$(ENGINE) $(PROJECT_DIR)/manage.py runserver

migrate: check_venv
	$(ENGINE) $(PROJECT_DIR)/manage.py migrate auth \
	&& $(ENGINE) $(PROJECT_DIR)/manage.py migrate

install:
	$(ENGINE_SETUP) install $(req)

req_in_file:
	$(ENGINE_SETUP) freeze > requirements.txt
