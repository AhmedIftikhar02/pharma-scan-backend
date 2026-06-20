import re
from typing import List

# --- Block-list: administrative/non-medical tokens to strip ---
BLOCK_LIST_TOKENS: List[str] = [
    "dr.", "clinic", "hospital", "tel:", "tel :", "phone:", "phone :",
    "email:", "email :", "web:", "web :", "address", "date:",
    "m.b.b.s", "mbbs", "rgn no", "rx", "patient:", "patient :",
    "age:", "name:", "gender:", "signature", "stamp",
]

# --- Regex: strip lines that are purely numeric or date-like ---
_RE_PURE_NUMERIC = re.compile(r"^\s*[\d\s\-\/\:\.\,]+\s*$")


def _is_blocked_line(line: str) -> bool:
    """Return True if this line should be removed from the payload."""
    lower = line.lower().strip()

    # Empty or whitespace-only
    if not lower:
        return True

    # Purely numeric / date line
    if _RE_PURE_NUMERIC.match(lower):
        return True

    # Contains any block-list token
    for token in BLOCK_LIST_TOKENS:
        if token in lower:
            return True

    return False


def clean_text(raw_text: str) -> List[str]:
    """
    Split raw OCR payload into lines, strip letterhead/admin noise.
    Returns a list of clean candidate drug-entry lines.
    """
    lines = raw_text.splitlines()
    clean_lines = [
        line.strip()
        for line in lines
        if not _is_blocked_line(line)
    ]
    return clean_lines