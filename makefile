.PHONY: lint test

default:
	@cat makefile

env:
	python3 -m venv env; . env/bin/activate; pip install --upgrade pip

update:  env
	. env/bin/activate; pip install -r requirements.txt

lint:
	-pylint bin/clean_ids.py
	-pylint bin/extract_transcripts.py

test: lint
	python -m pytest -v tests

test_enrich:
	@. env/bin/activate && cat lib/mock_transcripts.jsonl | python -u bin/enrich_transcripts.py | python bin/validate_schema.py

test_oop:
	@. env/bin/activate && cat mock_transcripts.jsonl | python -u lab6_oop/enrich_transcripts_llm.py
