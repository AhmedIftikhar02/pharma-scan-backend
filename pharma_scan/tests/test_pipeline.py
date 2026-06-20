import pytest
from fastapi.testclient import TestClient
from pharma_scan.main import app

client = TestClient(app)

class TestOCRTypoCorrection:
    """PRD Challenge 4 -- RapidFuzz guardrail tiers."""

    def test_panaddl_corrects_to_panadol(self):
        response = client.post("/api/v1/analyze", json={"raw_extracted_text": "Panaddl 500mg 1+1+1"})
        assert response.status_code == 200
        med = response.json()['prescribed_medicines'][0]
        assert med['medicine_name'] == 'Panadol'
        assert med['confidence_score'] >= 85.0
        assert med['unverified_entity'] is False

    def test_brufn_corrects_to_brufen(self):
        response = client.post("/api/v1/analyze", json={"raw_extracted_text": "Brufn Syrup"})
        assert response.status_code == 200
        med = response.json()['prescribed_medicines'][0]
        assert med['medicine_name'] == 'Brufen'
        assert med['confidence_score'] >= 85.0

    def test_azithromycn_corrects_to_azithromycin(self):
        response = client.post("/api/v1/analyze", json={"raw_extracted_text": "Azithromycn 250mg OD"})
        assert response.status_code == 200
        med = response.json()['prescribed_medicines'][0]
        assert med['medicine_name'] == 'Azithromycin'
        assert med['confidence_score'] >= 85.0


class TestKRRDosageFallback:
    """PRD Challenge 2 -- KB-driven dosage fallback engine."""

    def test_missing_dosage_triggers_kb_default(self):
        response = client.post("/api/v1/analyze", json={"raw_extracted_text": "Brufn Syrup"})
        assert response.status_code == 200
        med = response.json()['prescribed_medicines'][0]
        assert med['dosage']['is_predicted'] is True
        assert med['dosage']['value'] == '400mg'

    def test_explicit_dosage_skips_fallback(self):
        response = client.post("/api/v1/analyze", json={"raw_extracted_text": "Panaddl 500mg 1+1+1"})
        assert response.status_code == 200
        med = response.json()['prescribed_medicines'][0]
        assert med['dosage']['is_predicted'] is False
        assert med['dosage']['value'] == '500mg'

    def test_amoxicillin_no_explicit_dosage_uses_kb(self):
        response = client.post("/api/v1/analyze", json={"raw_extracted_text": "Amoxicillin tabs twice daily"})
        assert response.status_code == 200
        med = response.json()['prescribed_medicines'][0]
        assert med['dosage']['value'] == '250mg'
        assert med['dosage']['is_predicted'] is True


@pytest.fixture
def prd_sample_payload():
    return (
        'Dr. Sabeeh Ahmed Clinic\n'
        'Tel: 123456 | Date: 2026-06 | Email: doctor@clinic.com\n'
        'M.B.B.S Rgn No 4521 | Rx\n'
        'Panaddl 500mg 1+1+1\n'
        'Amoxicillin tabs twice daily\n'
        'Brufn Syrup'
    )