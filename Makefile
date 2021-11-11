# env
VENV := .venv
VENV_ACTIVATE := $(VENV)/bin/activate
VENV_SENTINEL := $(VENV)/.sentinel
VENV_PIP := $(VENV)/bin/pip $(PIP_EXTRA_OPTS)
VENV_PRECOMMIT := $(VENV)/bin/pre-commit
VENV_PYTEST := $(VENV)/bin/pytest

STAGE ?= dev


.PHONY: ensure_no_venv
ensure_no_venv:
ifdef VIRTUAL_ENV
	$(error Please deactivate your current virtual env)
endif


.PHONY: $(VENV)
$(VENV):
	$(MAKE) $(VENV_SENTINEL)


$(VENV_SENTINEL): requirements.txt .pre-commit-config.yaml
	$(MAKE) ensure_no_venv
	rm -rf $(VENV)
	python3.8 -m venv $(VENV)
	$(VENV_PIP) install --upgrade pip wheel
	$(VENV_PIP) install -r requirements.txt
	$(VENV_PIP) install -r requirements-test.txt
	$(VENV_PRECOMMIT) install
	touch $(VENV_SENTINEL)


.PHONY: pre-commit
pre-commit: $(VENV_SENTINEL)
	$(VENV_PRECOMMIT) run -a


.PHONY: test
test:
	$(VENV_PYTEST) -vv tests/


clean:
	rm -rf $(VENV)
