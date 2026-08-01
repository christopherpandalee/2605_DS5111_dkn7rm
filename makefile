.PHONY: lint test load

default:
	@cat makefile

ENV = env
PYTHON = $(ENV)/bin/python3
PIP = $(ENV)/bin/pip
ACTIVATE = $(ENV)/bin/activate

env:
	$(PYTHON) -m venv env; . $(ACTIVATE); pip install --upgrade pip

update:  env
	. $(ACTIVATE); pip install -r requirements.txt

lint:
	$(PYTHON) -m pylint bin/ lib/ tests/

test: lint
	$(PYTHON) -m pytest -v tests

test_enrich:
	@. $(ACTIVATE) && cat lib/mock_transcripts.jsonl | python -u bin/enrich_transcripts.py | python bin/validate_schema.py

test_oop:
	@. $(ACTIVATE) && cat lib/mock_transcripts.jsonl | python -u bin/enrich_transcripts_llm.py | python bin/validate_schema.py

load:
	@echo "Initiating Cloud Data Warehouse Synchronizer Node..."
	cat lib/mock_transcripts.jsonl | python bin/load_snowflake.py
