from __future__ import annotations

import json
from pathlib import Path

from .agent import analyze_equipment
from .config import get_settings
from .docx_writer import write_report_docx
from .normalizer import extract_records, load_json
from .parser_excel import parse_excel_file
from .report_builder import build_final_report
from .rules import build_pre_analysis
from .schemas import FinalReport, ParsedEquipmentRecord


def _load_input_records(input_path: str | Path) -> list[dict]:
    input_path = Path(input_path)
    suffix = input_path.suffix.lower()

    if suffix in {".xlsx", ".xlsm"}:
        return parse_excel_file(input_path)

    if suffix == ".json":
        payload = load_json(input_path)
        return extract_records(payload)

    raise ValueError("Format input tidak didukung. Gunakan file .xlsx, .xlsm, atau .json")


def run_pipeline(
    input_path: str | Path,
    output_docx: str | Path,
    output_json: str | Path | None = None,
    mode: str = "agent",
) -> FinalReport:
    settings = get_settings()
    raw_records = _load_input_records(input_path)

    invalid_rows: list[dict] = []
    validated_records: list[ParsedEquipmentRecord] = []

    for item in raw_records:
        try:
            validated_records.append(ParsedEquipmentRecord.model_validate(item))
        except Exception as exc:
            invalid_rows.append({
                "row": item,
                "error": str(exc),
        })

    records = validated_records

    if not records:
        raise ValueError("Tidak ada record valid setelah proses validasi.")

    if invalid_rows:
        print(f"[WARNING] Skipped {len(invalid_rows)} invalid rows during validation.")
        for idx, bad in enumerate(invalid_rows[:5], start=1):
            print(f"  {idx}. Error: {bad['error']}")
            print(f"     Row preview: {bad['row']}")
    running_records = [record for record in records if record.status.run]
    target_records = running_records or records

    narratives = []
    for record in target_records:
        facts = build_pre_analysis(record)
        narratives.append(analyze_equipment(facts, settings=settings, mode=mode))

    final_report = build_final_report(
        records=target_records,
        narratives=narratives,
        settings=settings,
    )

    write_report_docx(final_report, output_docx)

    if output_json is not None:
        output_json = Path(output_json)
        output_json.parent.mkdir(parents=True, exist_ok=True)
        with open(output_json, "w", encoding="utf-8") as file:
            json.dump(final_report.model_dump(mode="json"), file, ensure_ascii=False, indent=2)

    return final_report