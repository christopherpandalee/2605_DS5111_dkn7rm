"""LLM-based transcript enrich using OOP foundations"""
from abc import ABC, abstractmethod

import os
import sys
import logging
import json
from google import genai
from google.genai import types

class LLMStrategy(ABC): # pylint: disable=too-few-public-methods
    """Contract for any LLM to enrich Youtube transcripts"""
    @abstractmethod
    def enrich(self, video_id: str, raw_text: str) -> dict:
        """Accept one transcript record; return enriched, structured data as a dict."""

class GeminiStrategy(LLMStrategy):  # pylint: disable=too-few-public-methods
    """Concrete strategy that enriches transcripts via the Google Gemini API."""

    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            logging.critical("GEMINI_API_KEY not found in environment. Terminating.")
            sys.exit(1)
        self.client = genai.Client(api_key=api_key)

    def enrich(self, video_id: str, raw_text: str) -> dict:
        """AI cleanup of transcript"""
        response_schema = {
            "type": "OBJECT",
            "properties": {
                "video_id": {"type": "STRING"},
                "cleaned_text": {"type": "STRING"},
                "tech_terms": {"type": "ARRAY", "items": {"type": "STRING"}},
                "book_names": {"type": "ARRAY", "items": {"type": "STRING"}},
            },
            "required": ["video_id", "cleaned_text"],
        }

        prompt = f"""
        You are an elite data engineer. Clean this transcript text for video_id '{video_id}'.
        1. Strip all timestamps and duration codes.
        2. Extract technical architecture terms and books.
        """

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, raw_text],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=response_schema,
            ),
        )

        return json.loads(response.text)

class TranscriptEnricher: # pylint: disable=too-few-public-methods
    """Vendor-neutral engine: streams jsonl records through an injected LLM strategy."""

    def __init__(self, strategy: LLMStrategy):
        self.strategy = strategy

    def run_stream(self):
        """Parses json file to jsonl file if able. writes out to stdout if able"""
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            try:
                payload = json.loads(line)
                video_id = payload["video_id"]
                raw_text = payload["raw_text"]
            except Exception as e: # pylint: disable=broad-exception-caught
                logging.error("Failed to parse incoming JSON payload row: %s", str(e))
                continue

            try:
                result = self.strategy.enrich(video_id, raw_text)
                sys.stdout.write(json.dumps(result) + "\n")
                sys.stdout.flush()
            except Exception as e: # pylint: disable=broad-exception-caught
                logging.error("Failed processing video %s: %s", video_id, str(e))
