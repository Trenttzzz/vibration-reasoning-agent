from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> Any:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def extract_records(payload: Any) -> list[dict]:
    if isinstance(payload, list):
        return payload

    if isinstance(payload, dict):
        if "records" in payload and isinstance(payload["records"], list):
            return payload["records"]

        if "items" in payload and isinstance(payload["items"], list):
            return payload["items"]

        schema_markers = {"_meta", "_threshold", "tanggal", "equipment", "driver", "driven"}
        if len(schema_markers.intersection(set(payload.keys()))) >= 4 and "_type" in str(payload):
            raise ValueError(
                "Input JSON terlihat seperti schema template, bukan hasil parser aktual. "
                "Gunakan file JSON hasil parsing nyata atau file Excel raw."
            )

    raise ValueError(
        "Format input tidak dikenali. Gunakan list of records, object dengan key 'records' atau 'items', "
        "atau file Excel raw."
    )