"""
Utilities Package for ThinkFlow Studio.

Contains common helper tools (text parsing, date formatting, regex cleaners)
that do not belong to specific domain directories.

TODOs:
    - [ ] Add markdown tables parsing utilities for agent report formatting.
    - [ ] Create token counter utility functions utilizing tiktoken or gemini estimates.
"""

from typing import Any, List


class TextCleaner:
    """
    Utility helper for scrubbing and preparing raw user texts.
    """
    @staticmethod
    def remove_markdown_fences(text: str) -> str:
        """
        Removes ```json and similar code block fences from LLM responses.
        """
        lines = text.splitlines()
        cleaned_lines = [
            line for line in lines
            if not (line.strip().startswith("```") or line.strip() == "```")
        ]
        return "\n".join(cleaned_lines).strip()


class TokenHelper:
    """
    Placeholder utility for estimating token counts.
    """
    @staticmethod
    def estimate_tokens(text: str) -> int:
        """
        Provides a simple word-based rough estimation of token length.
        """
        # Roughly 1 word ~ 1.3 tokens
        return int(len(text.split()) * 1.3)
