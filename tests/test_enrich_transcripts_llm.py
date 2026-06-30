import sys
import io
import json
from lab6_oop.enrich_transcripts_llm import LLMStrategy, TranscriptEnricher


class MockLLMStrategy(LLMStrategy):  # pylint: disable=too-few-public-methods
    """Test double: honors the LLMStrategy contract, returns canned data, no network."""

    def enrich(self, video_id: str, raw_text: str) -> dict:
        return {
            "video_id": video_id,
            "cleaned_text": "Welcome to class. Today we are testing mock frameworks.",
            "tech_terms": ["mock frameworks"],
            "book_names": [],
        }
    
def test_orchestrator_processes_stream(monkeypatch, capsys):
    """Engine reads a jsonl line, calls the injected strategy, writes valid JSON out."""
    # Fake one line of stdin
    mock_row = {"video_id": "ds5111_v001", "raw_text": "00:01 Welcome to class."}
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(mock_row) + "\n"))

    # Inject the dummy strategy — no network, no monkeypatching the SDK
    engine = TranscriptEnricher(MockLLMStrategy())
    engine.run_stream()

    # Capture and verify what hit stdout
    captured = capsys.readouterr()
    lines = captured.out.strip().split("\n")
    assert len(lines) == 1

    parsed = json.loads(lines[0])
    assert parsed["video_id"] == "ds5111_v001"
    assert "mock frameworks" in parsed["tech_terms"]
