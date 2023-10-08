.PHONY: dev

ENGINE = venv/bin/python
PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
VENV_EXISTS := $(shell which venv/bin/python)

check_venv:
ifneq ($(ENGINE),$(VENV_EXISTS))
	$(error Virtualenv is not created)
endif

dev: check_venv
	$(ENGINE) $(PROJECT_DIR)/manage.py runserver