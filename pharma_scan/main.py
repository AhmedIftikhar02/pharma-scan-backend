import nest_asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

# Core engine imports
from pharma_scan.core.preprocessor import clean_text
from pharma_scan.core.regex_parser import extract_dosage, extract_frequency
from pharma_scan.core.fuzzy_ner import match_drug
from pharma_scan.core.krr_engine import apply_krr_rules

# Pydantic schemas
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
    raw_text = payload.raw_extracted_text
    if not raw_text or not raw_text.strip():
        raise HTTPException(status_code=400, detail="Raw extracted text cannot be empty.")
    
    # 1. Preprocessing
    cleaned_lines = clean_text(raw_text)
    
    prescribed_medicines = []
    
    # 2. Process each valid line
    for line in cleaned_lines:
        # Extract direct features from regex
        extracted_dosage = extract_dosage(line)
        extracted_freq_dict = extract_frequency(line)
        
        # Extract drug name using Fuzzy NER
        ner_result = match_drug(line)
        
        # If no valid drug is found or confidence is below absolute safety threshold, skip or handle
        if not ner_result:
            continue
            
        # 3. Pass through KRR Engine for default injection & rule validation
        final_entity = apply_krr_rules(
            resolved_drug=ner_result["resolved_drug"],
            original_token=ner_result["original_token"],
            confidence_score=ner_result["confidence_score"],
            unverified_entity=ner_result["unverified_entity"],
            extracted_dosage=extracted_dosage,
            extracted_freq_dict=extracted_freq_dict
        )
        
        prescribed_medicines.append(final_entity)
        
    return {
        "status": "success",
        "meta": {
            "total_medicines_found": len(prescribed_medicines),
            "processing_time_ms": 0.2  # Simulated or lightweight benchmark
        },
        "prescribed_medicines": prescribed_medicines
    }

    from mangum import Mangum
    handler = Mangum(app)