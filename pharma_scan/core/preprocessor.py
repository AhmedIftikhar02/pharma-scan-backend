import re
from typing import List

BLOCK_LIST_TOKENS: List[str] = [
    # Original tokens
    "dr.", "clinic", "hospital", "tel:", "tel :", "phone:", "phone :",
    "email:", "email :", "web:", "web :", "address", "date:",
    "m.b.b.s", "mbbs", "rgn no", "rx", "patient:", "patient :",
    "age:", "name:", "gender:", "signature", "stamp",
    # Extended tokens
    "fcps", "mrcp", "md.", "ms.", "prof.", "consultant",
    "prescription", "ref.", "ref:", "follow up", "follow-up",
    "advised", "advised to", "investigations", "lab:", "report",
    "next visit", "review after", "blood pressure", "weight:",
    "bp:", "sugar:", "registration", "opd", "ipd", "ward",
    "uhid", "mr no", "mr:", "cr no", "cr:", "bill no",
    "whatsapp", "facebook", "www.", "http",
]

_RE_PURE_NUMERIC = re.compile(r"^\s*[\d\s\-\/\:\.\,]+\s*$")
_RE_PHONE_LIKE = re.compile(r"^\s*[\+\d\s\-\(\)]{7,}\s*$")


def _is_blocked_line(line: str) -> bool:
    lower = line.lower().strip()

    if not lower:
        return True

    if _RE_PURE_NUMERIC.match(lower):
        return True

    if _RE_PHONE_LIKE.match(lower):
        return True

    for token in BLOCK_LIST_TOKENS:
        if token in lower:
            return True

    return False


def clean_text(raw_text: str) -> List[str]:
    lines = raw_text.splitlines()
    clean_lines = [
        line.strip()
        for line in lines
        if not _is_blocked_line(line)
    ]
    return clean_lines