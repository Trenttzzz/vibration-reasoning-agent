from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from .pipeline import analyze_records
from .schemas import FinalReport

app = FastAPI(
    title="Vibration Analysis Agent API",
    description="AI-powered vibration analysis for rotating equipment condition monitoring.",
    version="1.0.0",
)

ALLOWED_EXTENSIONS = {".xlsx", ".xlsm"}


@app.post(
    "/api/v1/analyze",
    response_model=FinalReport,
    summary="Analyze vibration data from an Excel file",
    description="Upload an Excel file (.xlsx or .xlsm) containing vibration measurement data. "
    "Returns a structured analysis report with fault detection, severity classification, "
    "and actionable recommendations.",
)
async def analyze(
    file: UploadFile = File(..., description="Excel file (.xlsx or .xlsm) with vibration data"),
    mode: str = Form(default="agent", description="Analysis mode: 'agent' (LLM-powered) or 'fallback' (deterministic only)"),
) -> FinalReport:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Format file tidak didukung. Gunakan file .xlsx atau .xlsm. Received: {suffix}",
        )

    if mode not in ("agent", "fallback"):
        raise HTTPException(
            status_code=400,
            detail=f"Mode tidak valid. Gunakan 'agent' atau 'fallback'. Received: {mode}",
        )

    tmp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = Path(tmp.name)

        report = analyze_records(tmp_path, mode=mode)
        return report

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan internal: {exc}") from exc

    finally:
        if tmp_path and tmp_path.exists():
            tmp_path.unlink()
