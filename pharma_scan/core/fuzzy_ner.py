from rapidfuzz import process, fuzz
from pharma_scan.data.drug_lexicon import DRUG_LEXICON

# Confidence thresholds
THRESHOLD_AUTO    = 85.0
THRESHOLD_WARN    = 65.0

def match_drug(token: str) -> dict:
    """
    Match a raw OCR token against the drug lexicon using RapidFuzz.
    Returns a result dict with match metadata.

    Confidence tiers:
      >= 85 : auto-corrected, clean match
      65-84 : matched but flagged as unverified
      < 65  : rejected as unknown
    """
    token_clean = token.strip()

    result = process.extractOne(
        token_clean,
        DRUG_LEXICON,
        scorer=fuzz.token_sort_ratio,
        score_cutoff=0,
    )

    if result is None:
        return {
            'resolved_drug':     'UNKNOWN',
            'original_token':    token_clean,
            'confidence_score':  0.0,
            'unverified_entity': False,
            'is_unknown':        True,
        }

    matched_name, score, _ = result
    score = round(float(score), 2)

    if score >= THRESHOLD_AUTO:
        return {
            'resolved_drug':      matched_name,
            'original_token':     token_clean,
            'confidence_score':   score,
            'unverified_entity':  False,
            'is_unknown':         False,
        }
    elif score >= THRESHOLD_WARN:
        return {
            'resolved_drug':      matched_name,
            'original_token':     token_clean,
            'confidence_score':   score,
            'unverified_entity':  True,
            'is_unknown':         False,
        }
    else:
        return {
            'resolved_drug':      'UNKNOWN',
            'original_token':     token_clean,
            'confidence_score':   score,
            'unverified_entity':  False,
            'is_unknown':         True,
        }


def extract_drug_token(line: str) -> str:
    """
    Heuristic: first word(s) of a prescription line are the drug name.
    Strips known non-drug suffixes like 'tabs', 'syrup', 'cap', 'inj'.
    """
    FORM_SUFFIXES = {'tabs', 'tab', 'syrup', 'cap', 'caps',
                     'inj', 'injection', 'susp', 'drops', 'cream', 'gel'}
    words = line.split()
    candidate_words = []
    for word in words:
        clean = word.strip('.,;:').lower()
        # Stop at dosage digit or known form suffix after first word collected
        if candidate_words and (clean[0].isdigit() or clean in FORM_SUFFIXES):
            break
        candidate_words.append(word)
    return ' '.join(candidate_words)