from pydantic import BaseModel, Field
from typing import List, Optional


class PrescriptionRequest(BaseModel):
    raw_extracted_text: str = Field(
        ...,
        min_length=3,
        description='Raw OCR string extracted from prescription image'
    )


class DosageBlock(BaseModel):
    value: str
    is_predicted: bool


class FrequencyBlock(BaseModel):
    standard_code: str
    original_code: str
    suggested_trigger_times: List[str]


class MedicineEntry(BaseModel):
    medicine_name: str
    original_ocr_token: str
    confidence_score: float
    unverified_entity: bool
    dosage: DosageBlock
    frequency: FrequencyBlock
    duration: str  # new field


class MetaBlock(BaseModel):
    total_medicines_found: int
    processing_time_ms: float


class PrescriptionResponse(BaseModel):
    status: str
    meta: MetaBlock
    prescribed_medicines: List[MedicineEntry]


class ErrorResponse(BaseModel):
    status: str = 'error'
    message: str