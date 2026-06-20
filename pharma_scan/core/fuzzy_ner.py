from rapidfuzz import process, fuzz
from pharma_scan.data.drug_lexicon import DRUG_LEXICON

THRESHOLD_AUTO = 85.0
THRESHOLD_WARN = 65.0

# Build lowercase → original_case mapping once at module load
_LEXICON_LOWER_MAP = {name.lower(): name for name in DRUG_LEXICON}
_LEXICON_LOWER_LIST = list(_LEXICON_LOWER_MAP.keys())


def match_drug(token: str) -> dict:
    token_clean = token.strip().lower()  # normalize input to lowercase

    result = process.extractOne(
        token_clean,
        _LEXICON_LOWER_LIST,
        scorer=fuzz.token_sort_ratio,
        score_cutoff=0,
    )

    if result is None:
        return {
            'resolved_drug': 'UNKNOWN',
            'original_token': token.strip(),
            'confidence_score': 0.0,
            'unverified_entity': False,
            'is_unknown': True,
        }

    matched_lower, score, _ = result
    score = round(float(score), 2)
    matched_name = _LEXICON_LOWER_MAP[matched_lower]  # restore original casing

    if score >= THRESHOLD_AUTO:
        return {
            'resolved_drug': matched_name,
            'original_token': token.strip(),
            'confidence_score': score,
            'unverified_entity': False,
            'is_unknown': False,
        }
    elif score >= THRESHOLD_WARN:
        return {
            'resolved_drug': matched_name,
            'original_token': token.strip(),
            'confidence_score': score,
            'unverified_entity': True,
            'is_unknown': False,
        }
    else:
        return {
            'resolved_drug': 'UNKNOWN',
            'original_token': token.strip(),
            'confidence_score': score,
            'unverified_entity': False,
            'is_unknown': True,
        }


def extract_drug_token(line: str) -> str:
    FORM_SUFFIXES = {
        'tabs', 'tab', 'syrup', 'cap', 'caps',
        'inj', 'injection', 'susp', 'drops', 'cream', 'gel', 'solution'
    }
    words = line.split()
    candidate_words = []
    for word in words:
        clean = word.strip('.,;:').lower()
        if not clean:  # guard against empty string crash
            continue
        if candidate_words and (clean[0].isdigit() or clean in FORM_SUFFIXES):
            break
        candidate_words.append(word)
    return ' '.join(candidate_words)