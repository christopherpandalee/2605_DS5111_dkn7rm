import sys
import io
import json
import pytest
from youtube_transcript_api import YouTubeTranscriptApi
 
# The executable entry point of your pipeline.
from lab4_transcript_testing.extract_transcripts import main
 
 
class MockTranscriptContainer:
    """Mimics the .to_raw_data() array output return schema of a fetched transcript."""
 
    def to_raw_data(self):
        return [
            {"start": 10.5, "text": "Automated container tracking loop text entry."}
        ]
 
 
# ---------------------------------------------------------------------------
# CASE 1: standard successful extraction sequence
# ---------------------------------------------------------------------------
def test_extract_transcripts_success_stream(monkeypatch, capsys):
    """
    Verifies that main() reads a valid video ID from stdin and emits exactly one
    structured JSON Lines object on stdout without hitting the internet.
    """
    # 1. Stub the third-party fetch so it returns our fake transcript.
    def stubbed_fetch_route(self, video_id):
        assert video_id == "fake_video_999"
        return MockTranscriptContainer()
 
    monkeypatch.setattr(YouTubeTranscriptApi, "fetch", stubbed_fetch_route)
 
    # 2. Feed one fake video ID through the input processor stream.
    monkeypatch.setattr(sys, "stdin", io.StringIO("fake_video_999\n"))
 
    # 3. Run the pipeline entry point directly.
    main()
 
    # 4. Capture stdout and isolate non-empty rows.
    captured = capsys.readouterr()
    stdout_lines = [line for line in captured.out.strip().split("\n") if line]
 
    # 5. Validate the emitted JSON Lines payload contract.
    assert len(stdout_lines) == 1, "Pipeline should emit exactly one row per valid ID."
 
    parsed = json.loads(stdout_lines[0])
    assert parsed["video_id"] == "fake_video_999"
    assert "Automated container tracking" in parsed["raw_text"]
