import re

# --- Regex Patterns for Dosage Extraction ---
# Matches patterns like 500mg, 500 mg, 10ml, 2.5ml, 1 tab, 2 capsules
_RE_DOSAGE = re.compile(
    r'(\d+(?:\.\d+)?)\s*(mg|ml|g|tab|tabs|capsule|capsules|cap|caps|puff|puffs|tsp|tbsp)\b',
    re.IGNORECASE
)

# --- Regex Patterns for Frequency Codes ---
_FREQ_PATTERNS = {
    'ONCE_A_DAY': re.compile(r'\b(od|once\s+daily|once\s+a\s+day|in\s+the\s+morning|at\s+bedtime)\b', re.IGNORECASE),
    'TWICE_A_DAY': re.compile(r'\b(bd|bid|twice\s+daily|twice\s+a\s+day|every\s+12\s+hours)\b', re.IGNORECASE),
    'THREE_TIMES_A_DAY': re.compile(r'\b(tds|tid|three\s+times\s+daily|three\s+times\s+a\s+day|every\s+8\s+hours)\b', re.IGNORECASE),
    'FOUR_TIMES_A_DAY': re.compile(r'\b(qds|qid|four\s+times\s+daily|four\s+times\s+a\s+day|every\s+6\s+hours)\b', re.IGNORECASE),
    'BEFORE_SLEEP': re.compile(r'\b(hs|at\s+night|before\s+sleep|night)\b', re.IGNORECASE),
    'BEFORE_MEALS': re.compile(r'\b(ac|before\s+meals|empty\s+stomach)\b', re.IGNORECASE),
    'AFTER_MEALS': re.compile(r'\b(pc|after\s+meals)\b', re.IGNORECASE),
    'AS_NEEDED': re.compile(r'\b(sos|prn|as\s+needed|whenever\s+required)\b', re.IGNORECASE),
}

# --- Numeric Matrix Pattern (e.g., 1+1+1, 1-0-1, 0-0-1) ---
_RE_MATRIX = re.compile(r'\b([0-2])\s*[\+\-\:引导]\s*([0-2])\s*[\+\-\:引导]\s*([0-2])\b')


def extract_dosage(line: str) -> str | None:
    """
    Scans a line and extracts structural dosage details (e.g., '500mg').
    Returns None if no dosage token matches.
    """
    match = _RE_DOSAGE.search(line)
    if match:
        # Reconstruct cleanly (e.g., '500 mg' -> '500mg')
        return f"{match.group(1)}{match.group(2).lower()}"
    return None


def extract_frequency(line: str) -> dict:
    """
    Scans a line for explicit Latin codes, English phrases, or numeric matrices (1+1+1).
    Maps it to a standardized KRR trigger code.
    """
    # 1. Test Numeric Matrix First (e.g., 1+1+1, 1-0-1)
    matrix_match = _RE_MATRIX.search(line)
    if matrix_match:
        vals = [int(x) for x in matrix_match.groups()]
        total_doses = sum(vals)
        orig_str = matrix_match.group(0)
        
        if total_doses == 3:
            return {'standard_code': 'THREE_TIMES_A_DAY', 'original_code': orig_str}
        elif total_doses == 2:
            return {'standard_code': 'TWICE_A_DAY', 'original_code': orig_str}
        elif total_doses == 1:
            return {'standard_code': 'ONCE_A_DAY', 'original_code': orig_str}
        elif total_doses == 4:
            return {'standard_code': 'FOUR_TIMES_A_DAY', 'original_code': orig_str}

    # 2. Test Direct Patterns (Regex Map)
    for code, pattern in _FREQ_PATTERNS.items():
        match = pattern.search(line)
        if match:
            return {
                'standard_code': code,
                'original_code': match.group(0).upper()
            }

    # 3. Fallback if completely unknown
    return {
        'standard_code': 'UNKNOWN',
        'original_code': 'N/A'
    }