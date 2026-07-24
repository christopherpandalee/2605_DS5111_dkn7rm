import sys
import io
import platform
import pytest
from bin.clean_ids import main

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
 
def run_main(monkeypatch, input_text):
    """Feed input_text to main() via stdin and return captured stdout."""
    monkeypatch.setattr(sys, "stdin", io.StringIO(input_text))


@pytest.mark.parametrize("id_string, expected_out", [
    ("kcFsuxaJ1es", "kcFsuxaJ1es\n"), # good id
    ("abcde_fG-H1", "abcde_fG-H1\n"), # good id with dash and underscore
    ("ABCDEFGHIJ1", "ABCDEFGHIJ1\n"), # good id with all uppercase
    ("bad line!!!", ""), # bad line
    (" ", ""), # empty line
])
def test_good_bad_ids(monkeypatch, capsys, id_string, expected_out):
    """Tests good and bad ids and lines"""
    run_main(monkeypatch, id_string + "\n")
    main()
    captured = capsys.readouterr()
    assert captured.out == expected_out


@pytest.mark.parametrize("id_string, expected_out", [
    ("123456789",    ""),               # 9 chars  → rejected
    ("1234567890",   ""),               # 10 chars → rejected
    ("12345678901",  "12345678901\n"),  # 11 chars → accepted
    ("123456789012", ""),               # 12 chars → rejected
    ("1234567890123",""),               # 13 chars → rejected
])
def test_id_length_boundaries(monkeypatch, capsys, id_string, expected_out):
    """Only exactly 11-character IDs are accepted."""
    run_main(monkeypatch, id_string + "\n")
    main()
    captured = capsys.readouterr()
    assert captured.out == expected_out


