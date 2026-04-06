from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(slots=True)
class Settings:
    openrouter_api_key: str | None = os.getenv("OPENROUTER_API_KEY")
    openrouter_model: str = os.getenv("OPENROUTER_MODEL", "minimax/minimax-m2.5:free")
    temperature: float = float(os.getenv("OPENROUTER_TEMPERATURE", "0.2"))
    max_tokens: int = int(os.getenv("OPENROUTER_MAX_TOKENS", "1800"))
    reasoning_effort: str = os.getenv("OPENROUTER_REASONING_EFFORT", "low")
    reasoning_summary: str = os.getenv("OPENROUTER_REASONING_SUMMARY", "concise")
    report_title: str = os.getenv(
        "REPORT_TITLE",
        "Laporan Detail Analisa & Rekomendasi Vibrasi Rotating Equipment (Terkoreksi)",
    )
    focus_label: str = os.getenv("FOCUS_LABEL", 'Equipment dengan Status "Running"')


def get_settings() -> Settings:
    return Settings()