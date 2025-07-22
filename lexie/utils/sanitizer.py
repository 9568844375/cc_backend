# === FILE: utils/sanitizer.py ===
import re
import logging

BLOCKED_PATTERNS = [
    r"(?i)openai", r"(?i)os\.", r"(?i)sys\.", r"(?i)import", r"(?i)subprocess",
    r"(?i)token", r"(?i)exec", r"(?i)evaluate", r"(?i)globals\(\)", r"(?i)__.*__"
]


def sanitize_input(text):
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, text):
            logging.warning(f"Blocked input: {text}")
            return "[Input blocked for safety]"
    return text
