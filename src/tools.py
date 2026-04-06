from __future__ import annotations

import json
from typing import Any

from langchain.tools import tool

from .schemas import FaultName


FAULT_LIBRARY: dict[FaultName, dict[str, Any]] = {
    "bearing_damage": {
        "definition": "Kerusakan bearing yang umumnya ditandai oleh nilai HE tinggi dan dapat diikuti peningkatan radial vibration.",
        "default_actions": [
            "Ganti bearing yang rusak",
            "Inspeksi poros, housing, dan dudukan bearing",
            "Periksa kualitas pelumasan",
        ],
    },
    "misalignment": {
        "definition": "Ketidaksejajaran driver dan driven yang biasanya memicu axial vibration tinggi pada beberapa titik.",
        "default_actions": [
            "Lakukan alignment ulang",
            "Periksa soft foot dan kondisi kopling",
            "Verifikasi kondisi baseplate dan pondasi",
        ],
    },
    "unbalance": {
        "definition": "Ketidakseimbangan rotor atau impeller yang sering terlihat dari radial atau horizontal vibration dominan.",
        "default_actions": [
            "Lakukan balancing",
            "Periksa impeller atau rotor",
            "Verifikasi adanya deposit, aus, atau deformasi",
        ],
    },
    "overheat_or_lubrication": {
        "definition": "Temperatur tinggi atau gejala pelumasan buruk yang dapat mempercepat wear bearing.",
        "default_actions": [
            "Periksa grease atau oil",
            "Pastikan jalur pelumasan bekerja baik",
            "Periksa suhu operasi dan pendinginan",
        ],
    },
}


@tool
def get_threshold_reference() -> str:
    """Mengembalikan acuan threshold severity vibrasi dan temperatur."""
    return (
        "ISO 10816-3 digunakan sebagai acuan velocity vibration. "
        "Kategori velocity: <2.8 BAIK, 2.8 sampai 4.5 CUKUP, 4.5 sampai 7.1 WASPADA, >7.1 BAHAYA. "
        "Kategori temperatur: <60 BAIK, 60 sampai 80 CUKUP, >80 BAHAYA."
    )


@tool
def get_fault_library(fault_name: str) -> str:
    """Mengembalikan definisi fault dan aksi default dalam format JSON string."""
    payload = FAULT_LIBRARY.get(
        fault_name,  # type: ignore[arg-type]
        {
            "definition": "Fault tidak ditemukan dalam library lokal.",
            "default_actions": ["Lakukan inspeksi manual lanjutan."],
        },
    )
    return json.dumps(payload, ensure_ascii=False)


@tool
def get_report_style_guide() -> str:
    """Mengembalikan gaya bahasa laporan teknis operasional."""
    return (
        "Gunakan gaya laporan operasional yang lugas, teknis, dan langsung ke inti. "
        "Jangan mengarang angka baru. "
        "Mulai analisa dari severity, lanjutkan bukti teknis, lalu simpulkan fault dominan dan rekomendasi tindakan."
    )