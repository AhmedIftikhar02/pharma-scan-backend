# Cell 16: Write pharma_scan/main.py

lines = [
    "from fastapi import FastAPI, HTTPException\n",
    "from fastapi.responses import JSONResponse\n",
    "from pharma_scan.schemas.models import AnalyzeRequest, AnalyzeResponse, ErrorResponse\n",
    "from pharma_scan.core.krr_engine import run_pipeline\n",
    "\n",
    "app = FastAPI(\n",
    "    title='Pharma-Scan AI Engine',\n",
    "    description='Intelligent prescription parser microservice',\n",
    "    version='1.0.0',\n",
    ")\n",
    "\n",
    "\n",
    "@app.get('/')\n",
    "def health_check():\n",
    "    return {'status': 'online', 'service': 'Pharma-Scan AI Engine v1.0.0'}\n",
    "\n",
    "\n",
    "@app.post(\n",
    "    '/api/v1/analyze',\n",
    "    response_model=AnalyzeResponse,\n",
    "    responses={422: {'model': ErrorResponse}, 500: {'model': ErrorResponse}},\n",
    ")\n",
    "def analyze_prescription(payload: AnalyzeRequest):\n",
    "    \"\"\"\n",
    "    Accept raw OCR prescription text.\n",
    "    Returns structured medicine entities with dosage and trigger times.\n",
    "    \"\"\"\n",
    "    try:\n",
    "        result = run_pipeline(payload.raw_extracted_text)\n",
    "        return JSONResponse(content=result, status_code=200)\n",
    "    except Exception as e:\n",
    "        raise HTTPException(\n",
    "            status_code=500,\n",
    "            detail=str(e)\n",
    "        )\n",
]

with open("pharma_scan/main.py", "w") as f:
    f.writelines(lines)

print("✅ main.py written.")