import sys
import io
import platform
import pytest
from lab2_cleaning_ids.clean_ids import main

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
 
def run_main(monkeypatch, input_text):
    """Feed input_text to main() via stdin and return captured stdout."""
    monkeypatch.setattr(sys, "stdin", io.StringIO(input_text))


def test_running_on_ubuntu():
    """The pipeline is expected to run on Ubuntu."""
    os_info = platform.freedesktop_os_release() if hasattr(platform, "freedesktop_os_release") else {}
    os_id = os_info.get("ID", "").lower()
    assert os_id == "ubuntu", (
        f"Expected Ubuntu, got '{os_id}'. "
        "This test suite is designed for Ubuntu environments."
    )
 
 
def test_python_version():
    """Require Python 3.10 or later."""
    assert sys.version_info >= (3, 10), (
        f"Python 3.10+ required; running {sys.version}"
    )


@pytest.mark.xfail(reason="Unicode letters are not yet supported")
def test_unicode_id_accepted(monkeypatch, capsys):
    """
    Future feature: IDs with valid-length unicode chars should pass.
    Currently fails because the allowed-chars set is ASCII-only.
    """
    run_main(monkeypatch, "ñbcdefghij1\n")   # contains 'ñ'
    main()
    captured = capsys.readouterr()
    assert captured.out == "ñbcdefghij1\n"


@pytest.mark.skip(reason="test designed to skip")
def test_file_input_mode(tmp_path):
    """
    This test is designed to be skipped
    """
    pass

@pytest.mark.parametrize("id_string, should_pass", [
    # (input,            expected in stdout?)
    ("kcFsuxaJ1es",  True),   # canonical valid ID
    ("DQw4w9WgXcQ",  True),   # another valid ID
    ("asd123",        False),  # too short (6 chars)
    ("123456789012",  False),  # too long  (12 chars)
    ("hello world!",  False),  # spaces and punctuation
    ("AAAAAAAAAAA",   True),   # 11 uppercase letters
    ("00000000000",   True),   # 11 zeros
    ("____-------",   True),   # 11 valid special chars (underscores/dashes)
    ("abc defghij",   False),  # space in the middle
    ("",               False),  # empty string
])
def test_parametrized_id_validation(monkeypatch, capsys, id_string, should_pass):
    """Parametrized sweep across valid and invalid ID shapes."""
    run_main(monkeypatch, id_string + "\n")
    main()
    captured = capsys.readouterr()
    if should_pass:
        assert captured.out == id_string + "\n", (
            f"Expected '{id_string}' to be accepted, but it was rejected."
        )
    else:
        assert captured.out == "", (
            f"Expected '{id_string}' to be rejected, but it was accepted."
        )
