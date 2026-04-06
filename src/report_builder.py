from __future__ import annotations

from .config import Settings
from .rules import summarize_priority_tags
from .schemas import EquipmentNarrative, FinalReport, ParsedEquipmentRecord, ReportMeta, ReportRow


def build_final_report(
    records: list[ParsedEquipmentRecord],
    narratives: list[EquipmentNarrative],
    settings: Settings,
) -> FinalReport:
    running_records = [record for record in records if record.status.run]
    area = running_records[0].area if running_records else (records[0].area if records else "-")
    tanggal = running_records[0].tanggal if running_records else (records[0].tanggal if records else "-")

    rows = [
        ReportRow(
            no=item.no,
            tag_name=item.tag_name,
            deskripsi=item.deskripsi,
            titik_nilai_vibrasi_tertinggi=item.titik_nilai_vibrasi_tertinggi,
            analysis=item.analysis,
            recommendations=item.recommendations,
            overall_level=item.overall_level,
            priority_bucket=item.priority_bucket,
        )
        for item in sorted(narratives, key=lambda x: x.no)
    ]

    rows_dict = [row.model_dump(mode="json") for row in rows]

    return FinalReport(
        meta=ReportMeta(
            title=settings.report_title,
            tanggal_pengukuran=tanggal,
            area=area,
            fokus_laporan=settings.focus_label,
        ),
        standard_reference_intro=(
            "Analisa tingkat keparahan vibrasi mengacu pada standar ISO 10816-3 "
            "untuk motor dan rotating equipment sejenis."
        ),
        thresholds=[
            "< 2.8 mm/s (Baik): Kondisi operasional sangat baik.",
            "2.8 - 4.5 mm/s (Cukup): Dapat diterima, namun memerlukan monitoring tren.",
            "4.5 - 7.1 mm/s (Waspada): Kondisi tidak memuaskan dan perlu investigasi.",
            "> 7.1 mm/s (Bahaya): Level vibrasi berisiko merusak dan memerlukan tindakan segera.",
        ],
        rows=rows,
        priority_1_text=summarize_priority_tags(
            rows_dict,
            "PRIORITAS_1",
            "Tidak ada unit kategori bahaya pada laporan ini.",
        ),
        priority_2_text=summarize_priority_tags(
            rows_dict,
            "PRIORITAS_2",
            "Tidak ada unit kategori waspada pada laporan ini.",
        ),
        priority_3_text=summarize_priority_tags(
            rows_dict,
            "PRIORITAS_3",
            "Tidak ada unit kategori cukup untuk monitoring diperketat.",
        ),
        closing_note="Dokumen ini disusun otomatis dari hasil parser, rules engine, dan agent analisa.",
    )