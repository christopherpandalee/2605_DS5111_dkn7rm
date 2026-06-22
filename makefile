.PHONY: lint test

default:
	@cat makefile

env:
	python3 -m venv env; . env/bin/activate; pip install --upgrade pip

update:  env
	. env/bin/activate; pip install -r requirements.txt

lint:
	-pylint lab2_cleaning_ids/clean_ids.py
	-pylint lab4_transcript_testing/extract_transcripts.py

test: lint
	python -m pytest -v tests

test_enrich:
	@. env/bin/activate && cat mock_transcripts.jsonl | python -u lab5_enrich_transcript/enrich_transcripts.py | python lab5_enrich_transcript/validate_schema.py
