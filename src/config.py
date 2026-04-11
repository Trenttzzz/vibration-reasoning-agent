from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()

@dataclass(slots=True)
class Settings:
    llm_provider: str = os.getenv("LLM_PROVIDER", "openrouter")

    openrouter_api_key: str | None = os.getenv("OPENROUTER_API_KEY")
    openrouter_model: str = os.getenv("OPENROUTER_MODEL", "minimax/minimax-m2.5:free")
    openrouter_temperature: float = float(os.getenv("OPENROUTER_TEMPERATURE", "0.2"))
    openrouter_max_tokens: int = int(os.getenv("OPENROUTER_MAX_TOKENS", "1800"))
    openrouter_reasoning_effort: str = os.getenv("OPENROUTER_REASONING_EFFORT", "low")
    openrouter_reasoning_summary: str = os.getenv("OPENROUTER_REASONING_SUMMARY", "concise")

    sumopod_api_key: str | None = os.getenv("SUMOPOD_API_KEY")
    sumopod_model: str = os.getenv("SUMOPOD_MODEL", "glm-5.1")
    sumopod_base_url: str = os.getenv("SUMOPOD_BASE_URL", "https://ai.sumopod.com/v1")
    sumopod_temperature: float = float(os.getenv("SUMOPOD_TEMPERATURE", "0.2"))
    sumopod_max_tokens: int = int(os.getenv("SUMOPOD_MAX_TOKENS", "1800"))

    report_title: str = os.getenv(
        "REPORT_TITLE",
        "Laporan Detail Analisa & Rekomendasi Vibrasi Rotating Equipment (Terkoreksi)",
    )
    focus_label: str = os.getenv("FOCUS_LABEL", 'Equipment dengan Status "Running"')


def get_settings() -> Settings:
    return Settings()