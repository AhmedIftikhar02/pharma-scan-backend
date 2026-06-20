import re
from typing import Optional

# Dosage pattern: 500mg, 10ml, 2.5mg, 1000iu, etc.
_RE_DOSAGE = re.compile(
    r'\b(\d+(?:\.\d+)?)\s*(mg|ml|mcg|g|iu|mg\/ml|mg\/5ml|tab|tabs|capsule|capsules|cap|caps|puff|puffs|tsp|tbsp)\b',
    re.IGNORECASE
)

# Numeric matrix: 1+1+1, 1-0-1, 1/0/1 (FIXED: removed Unicode character bug)
_RE_MATRIX = re.compile(
    r'\b([0-2])\s*[\+\-\/\.]\s*([0-2])\s*[\+\-\/\.]\s*([0-2])\b'
)

# Duration: "for 5 days", "x7", "1 week", "2 months"
_RE_DURATION = re.compile(
    r'\b(?:for\s+)?(\d+)\s*(day|days|week|weeks|month|months)\b|x\s*(\d+)',
    re.IGNORECASE
)

_FREQ_PATTERNS = {
    'ONCE_A_DAY': re.compile(
        r'\b(od|once\s+daily|once\s+a\s+day|in\s+the\s+morning|daily|once)\b',
        re.IGNORECASE
    ),
    'TWICE_A_DAY': re.compile(
        r'\b(bd|bid|twice\s+daily|twice\s+a\s+day|every\s+12\s+hours|2\s*times\s*daily|twice)\b',
        re.IGNORECASE
    ),
    'THREE_TIMES_A_DAY': re.compile(
        r'\b(tds|tid|three\s+times\s+daily|three\s+times\s+a\s+day|every\s+8\s+hours|3\s*times\s*daily)\b',
        re.IGNORECASE
    ),
    'FOUR_TIMES_A_DAY': re.compile(
        r'\b(qds|qid|four\s+times\s+daily|four\s+times\s+a\s+day|every\s+6\s+hours|4\s*times\s*daily)\b',
        re.IGNORECASE
    ),
    'BEFORE_SLEEP': re.compile(
        r'\b(hs|at\s+night|before\s+sleep|night|bedtime)\b',
        re.IGNORECASE
    ),
    'BEFORE_MEALS': re.compile(
        r'\b(ac|before\s+meals|empty\s+stomach|before\s+eating)\b',
        re.IGNORECASE
    ),
    'AFTER_MEALS': re.compile(
        r'\b(pc|after\s+meals|after\s+eating|with\s+food)\b',
        re.IGNORECASE
    ),
    'AS_NEEDED': re.compile(
        r'\b(sos|prn|as\s+needed|whenever\s+required|if\s+needed)\b',
        re.IGNORECASE
    ),
}


def extract_dosage(line: str) -> Optional[str]:
    match = _RE_DOSAGE.search(line)
    if match:
        return f"{match.group(1)}{match.group(2).lower().replace(' ', '')}"
    return None


def extract_frequency(line: str) -> dict:
    # 1. Check numeric matrix first (1+1+1, 1-0-1)
    matrix_match = _RE_MATRIX.search(line)
    if matrix_match:
        vals = [int(x) for x in matrix_match.groups()]
        total = sum(vals)
        orig_str = matrix_match.group(0).replace(' ', '')
        dose_map = {
            1: 'ONCE_A_DAY',
            2: 'TWICE_A_DAY',
            3: 'THREE_TIMES_A_DAY',
            4: 'FOUR_TIMES_A_DAY',
        }
        return {
            'standard_code': dose_map.get(total, f'CUSTOM_{total}_TIMES_A_DAY'),
            'original_code': orig_str
        }

    # 2. Check Latin/English patterns
    for code, pattern in _FREQ_PATTERNS.items():
        match = pattern.search(line)
        if match:
            return {
                'standard_code': code,
                'original_code': match.group(0).upper()
            }

    # 3. Fallback
    return {'standard_code': 'UNKNOWN', 'original_code': 'N/A'}


def extract_duration(line: str) -> Optional[str]:
    match = _RE_DURATION.search(line)
    if not match:
        return None
    if match.group(3):  # x7 pattern
        return f"{match.group(3)} days"
    count = match.group(1)
    unit = match.group(2).lower()
    return f"{count} {unit}"