"""
Local Security Scanner for Input Validation and Prompt Injection.
"""
import re
from typing import Tuple

class SecurityScanner:
    MAX_INPUT_LENGTH = 2000
    
    # Simple heuristics for prompt injection detection (since we must operate locally)
    INJECTION_PATTERNS = [
        r"(?i)ignore\s+(all\s+)?(previous\s+)?instructions",
        r"(?i)you\s+are\s+now",
        r"(?i)system\s+prompt",
        r"(?i)bypass",
        r"(?i)do\s+not\s+follow"
    ]

    @classmethod
    def scan_input(cls, user_prompt: str) -> Tuple[bool, str]:
        """
        Scans input for security violations.
        Returns (is_safe, error_message).
        """
        if not user_prompt or not user_prompt.strip():
            return False, "Input cannot be empty."

        if len(user_prompt) > cls.MAX_INPUT_LENGTH:
            return False, f"Input exceeds maximum allowed length of {cls.MAX_INPUT_LENGTH} characters."

        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, user_prompt):
                return False, "Security violation: Potential prompt injection detected."

        return True, ""
