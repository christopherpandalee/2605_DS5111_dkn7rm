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
    
def test_extract_transcripts_handles_unfetchable_id(monkeypatch, capsys):
    """
    Verifies that the pipeline catches a failed fetch gracefully:
      - it does NOT crash / propagate the exception,
      - the empty line and the un-fetchable ID produce no valid row,
      - a subsequent valid ID is still processed (the loop survives).
    """
    # fetch succeeds only for "good_video"; everything else raises, simulating an
    # un-fetchable video (disabled/missing transcript, bad ID, etc.).
    def selective_fetch(self, video_id):
        if video_id == "good_video":
            return MockTranscriptContainer()
        raise Exception(f"Could not retrieve transcript for {video_id!r}")
 
    monkeypatch.setattr(YouTubeTranscriptApi, "fetch", selective_fetch)
 
    # Input stream: an empty line, an un-fetchable ID, then a valid ID.
    monkeypatch.setattr(sys, "stdin", io.StringIO("\nbad_video_id\ngood_video\n"))
 
    # main() must NOT raise — if it does, this line fails the test, which is the
    # whole point: an error in the stream should be handled, not propagated.
    main()
 
    captured = capsys.readouterr()
    stdout_lines = [line for line in captured.out.strip().split("\n") if line]
 
    # Only the valid ID should yield an output row; the empty and un-fetchable
    # IDs are skipped gracefully.
    assert len(stdout_lines) == 1, "Only the valid ID should produce a row."
 
    parsed = json.loads(stdout_lines[0])
    assert parsed["video_id"] == "good_video"
    assert "raw_text" in parsed
