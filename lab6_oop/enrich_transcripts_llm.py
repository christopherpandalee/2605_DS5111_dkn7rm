"""LLM-based transcript enrich using OOP foundations"""
from abc import ABC, abstractmethod

class LLMStrategy(ABC): # pylint: disable=too-few-public-methods
    """Contract for any LLM to enrich Youtube transcripts"""
    @abstractmethod
    def enrich(self, video_id: str, raw_text: str) -> dict:
        """Accept one transcript record; return enriched, structured data as a dict."""
