from pharma_scan.data.knowledge_base import DEFAULT_DOSAGE_KB, TIME_TRIGGER_MAP


def _resolve_dosage(medicine_name: str, extracted_dosage: str | None) -> dict:
    if extracted_dosage:
        return {'value': extracted_dosage, 'is_predicted': False}

    kb_key = medicine_name.lower()
    default = DEFAULT_DOSAGE_KB.get(kb_key)
    if default:
        return {'value': default, 'is_predicted': True}

    return {'value': 'N/A', 'is_predicted': False}


def apply_krr_rules(
    resolved_drug: str,
    original_token: str,
    confidence_score: float,
    unverified_entity: bool,
    extracted_dosage: str | None,
    extracted_freq_dict: dict,
    extracted_duration: str | None = None,
) -> dict:
    resolved_dosage = _resolve_dosage(resolved_drug, extracted_dosage)

    std_code = extracted_freq_dict.get('standard_code', 'UNKNOWN')
    orig_code = extracted_freq_dict.get('original_code', 'N/A')
    trigger_times = TIME_TRIGGER_MAP.get(std_code, [])

    return {
        'medicine_name': resolved_drug,
        'original_ocr_token': original_token,
        'confidence_score': confidence_score,
        'unverified_entity': unverified_entity,
        'dosage': resolved_dosage,
        'frequency': {
            'standard_code': std_code,
            'original_code': orig_code,
            'suggested_trigger_times': trigger_times,
        },
        'duration': extracted_duration or 'N/A',
    }