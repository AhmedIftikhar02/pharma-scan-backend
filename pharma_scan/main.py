import nest_asyncio
nest_asyncio.apply()
import time
from fastapi import FastAPI, HTTPException
from pharma_scan.core.preprocessor import clean_text
from pharma_scan.core.regex_parser import extract_dosage, extract_frequency, extract_duration
from pharma_scan.core.fuzzy_ner import match_drug, extract_drug_token
from pharma_scan.core.krr_engine import apply_krr_rules
from pharma_scan.schemas.models import PrescriptionRequest, PrescriptionResponse

app = FastAPI(
    title="Pharma-Scan & AI Prescription Reader",
    description="Core AI & Backend Engine for Parsing Medical Prescriptions",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {
        "status": "healthy",
        "service": "Pharma-Scan Core AI Engine",
        "documentation": "/docs"
    }


@app.post("/api/v1/analyze", response_model=PrescriptionResponse)
async def analyze_prescription(payload: PrescriptionRequest):
    start_time = time.time()

    raw_text = payload.raw_extracted_text
    if not raw_text or not raw_text.strip():
        raise HTTPException(status_code=400, detail="Raw extracted text cannot be empty.")

    cleaned_lines = clean_text(raw_text)
    prescribed_medicines = []

    for line in cleaned_lines:
        drug_token = extract_drug_token(line)
        extracted_dosage = extract_dosage(line)
        extracted_freq_dict = extract_frequency(line)
        extracted_dur = extract_duration(line)  # new

        ner_result = match_drug(drug_token)
        if not ner_result or ner_result.get('is_unknown'):
            continue

        final_entity = apply_krr_rules(
            resolved_drug=ner_result["resolved_drug"],
            original_token=ner_result["original_token"],
            confidence_score=ner_result["confidence_score"],
            unverified_entity=ner_result["unverified_entity"],
            extracted_dosage=extracted_dosage,
            extracted_freq_dict=extracted_freq_dict,
            extracted_duration=extracted_dur,  # new
        )
        prescribed_medicines.append(final_entity)

    elapsed_ms = round((time.time() - start_time) * 1000, 2)

    return {
        "status": "success",
        "meta": {
            "total_medicines_found": len(prescribed_medicines),
            "processing_time_ms": elapsed_ms,
        },
        "prescribed_medicines": prescribed_medicines
    }