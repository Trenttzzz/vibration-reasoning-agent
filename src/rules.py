from __future__ import annotations

from collections import Counter
from typing import Iterable

from .schemas import (
    FaultHypothesis,
    MetricFinding,
    ParsedEquipmentRecord,
    PreAnalysisFacts,
    SeverityLabel,
)


VIBRATION_THRESHOLDS = {
    "BAIK": (None, 2.8),
    "CUKUP": (2.8, 4.5),
    "WASPADA": (4.5, 7.1),
    "BAHAYA": (7.1, None),
}

TEMP_THRESHOLDS = {
    "BAIK": (None, 60.0),
    "CUKUP": (60.0, 80.0),
    "BAHAYA": (80.0, None),
}


def classify_vibration(value: float | None) -> SeverityLabel:
    if value is None:
        return "BAIK"
    if value < 2.8:
        return "BAIK"
    if value < 4.5:
        return "CUKUP"
    if value <= 7.1:
        return "WASPADA"
    return "BAHAYA"


def classify_temperature(value: float | None) -> SeverityLabel:
    if value is None:
        return "BAIK"
    if value < 60:
        return "BAIK"
    if value < 80:
        return "CUKUP"
    return "BAHAYA"


def severity_rank(label: SeverityLabel) -> int:
    return {"BAIK": 0, "CUKUP": 1, "WASPADA": 2, "BAHAYA": 3}[label]


def iter_vibration_points(record: ParsedEquipmentRecord) -> Iterable[tuple[str, str, float]]:
    point_map = [
        ("Motor NDE", record.driver.NDE),
        ("Motor DE", record.driver.DE),
        ("Driven DE", record.driven.DE),
        ("Driven NDE", record.driven.NDE),
    ]
    for point_name, bearing in point_map:
        for metric in ("ax", "v", "h", "he"):
            value = getattr(bearing, metric)
            if value is not None:
                yield point_name, metric, float(value)


def iter_temperature_points(record: ParsedEquipmentRecord) -> Iterable[tuple[str, str, float]]:
    temp_points = [
        ("Motor NDE", "temp", record.driver.NDE.temp),
        ("Motor DE", "temp", record.driver.DE.temp),
        ("Driven DE", "temp", record.driven.DE.temp),
        ("Driven NDE", "temp", record.driven.NDE.temp),
    ]
    if record.driver.temp_terminal_box is not None:
        temp_points.append(("Terminal Box", "temp", float(record.driver.temp_terminal_box)))

    for point_name, metric, value in temp_points:
        if value is not None:
            yield point_name, metric, float(value)


def build_abnormal_findings(record: ParsedEquipmentRecord) -> list[MetricFinding]:
    findings: list[MetricFinding] = []

    for point_name, metric, value in iter_vibration_points(record):
        severity = classify_vibration(value)
        if severity != "BAIK":
            findings.append(
                MetricFinding(
                    point_label=point_name,
                    metric=metric,
                    value=value,
                    severity=severity,
                )
            )

    for point_name, metric, value in iter_temperature_points(record):
        severity = classify_temperature(value)
        if severity != "BAIK":
            findings.append(
                MetricFinding(
                    point_label=point_name,
                    metric=metric,
                    value=value,
                    severity=severity,
                )
            )

    findings.sort(key=lambda item: (-severity_rank(item.severity), -item.value, item.point_label))
    return findings


def top_vibration(record: ParsedEquipmentRecord) -> tuple[str, str, float]:
    points = list(iter_vibration_points(record))
    if not points:
        return "Tidak ada data", "h", 0.0
    point_name, metric, value = max(points, key=lambda item: item[2])
    return point_name, metric, value


def detect_faults(
    record: ParsedEquipmentRecord,
    abnormal_findings: list[MetricFinding],
) -> list[FaultHypothesis]:
    hypotheses: list[FaultHypothesis] = []

    high_he = [f for f in abnormal_findings if f.metric == "he" and f.value >= 4.5]
    high_ax = [f for f in abnormal_findings if f.metric == "ax" and f.value >= 4.5]
    high_horizontal = [f for f in abnormal_findings if f.metric == "h" and f.value >= 4.5]
    high_temp = [f for f in abnormal_findings if f.metric == "temp" and f.value >= 60.0]

    if high_he:
        evidence = [f"{item.point_label} HE={item.value:.1f} ({item.severity})" for item in high_he[:4]]
        confidence = 0.90 if any(item.value > 7.1 for item in high_he) else 0.75
        hypotheses.append(
            FaultHypothesis(
                fault_name="bearing_damage",
                confidence=confidence,
                evidence=evidence,
            )
        )

    if len(high_ax) >= 2:
        evidence = [f"{item.point_label} AX={item.value:.1f} ({item.severity})" for item in high_ax[:4]]
        confidence = 0.88 if len(high_ax) >= 3 else 0.75
        hypotheses.append(
            FaultHypothesis(
                fault_name="misalignment",
                confidence=confidence,
                evidence=evidence,
            )
        )

    if len(high_horizontal) >= 2:
        evidence = [f"{item.point_label} H={item.value:.1f} ({item.severity})" for item in high_horizontal[:4]]
        hypotheses.append(
            FaultHypothesis(
                fault_name="unbalance",
                confidence=0.70,
                evidence=evidence,
            )
        )

    if high_temp:
        evidence = [f"{item.point_label} TEMP={item.value:.1f} ({item.severity})" for item in high_temp[:4]]
        hypotheses.append(
            FaultHypothesis(
                fault_name="overheat_or_lubrication",
                confidence=0.65,
                evidence=evidence,
            )
        )

    hypotheses.sort(key=lambda item: item.confidence, reverse=True)
    return hypotheses


def determine_overall_level(abnormal_findings: list[MetricFinding]) -> SeverityLabel:
    if not abnormal_findings:
        return "BAIK"
    return max(abnormal_findings, key=lambda item: severity_rank(item.severity)).severity


def build_pre_analysis(record: ParsedEquipmentRecord) -> PreAnalysisFacts:
    abnormal_findings = build_abnormal_findings(record)
    top_point, top_metric, top_value = top_vibration(record)
    fault_hypotheses = detect_faults(record, abnormal_findings)
    overall_level = determine_overall_level(abnormal_findings)

    return PreAnalysisFacts(
        no=record.no,
        tanggal=record.tanggal,
        area=record.area,
        tag_name=record.equipment.tag_name,
        deskripsi=record.equipment.deskripsi,
        running=record.status.run,
        top_vibration_point=top_point,
        top_vibration_value=round(top_value, 2),
        top_vibration_metric=top_metric,
        overall_level=overall_level,
        abnormal_findings=abnormal_findings,
        fault_hypotheses=fault_hypotheses,
    )


def default_recommendations(fault_names: list[str], overall_level: SeverityLabel) -> list[str]:
    recommendations: list[str] = []

    if "bearing_damage" in fault_names:
        recommendations.append("Ganti bearing yang terindikasi rusak dan inspeksi dudukan bearing serta poros.")
    if "misalignment" in fault_names:
        recommendations.append("Lakukan alignment ulang pada pasangan driver dan driven.")
    if "unbalance" in fault_names:
        recommendations.append("Lakukan balancing dan inspeksi rotor atau impeller.")
    if "overheat_or_lubrication" in fault_names:
        recommendations.append("Periksa pelumasan, temperatur operasi, dan kondisi pendinginan atau sealing.")

    if overall_level == "BAHAYA":
        recommendations.append("Jadwalkan shutdown terkontrol dan perbaikan segera.")
    elif overall_level == "WASPADA":
        recommendations.append("Lakukan investigasi mendalam dan percepat jadwal corrective maintenance.")
    elif overall_level == "CUKUP":
        recommendations.append("Perketat monitoring tren vibrasi pada inspeksi berikutnya.")

    deduped: list[str] = []
    for item in recommendations:
        if item not in deduped:
            deduped.append(item)
    return deduped


def default_priority_bucket(overall_level: SeverityLabel) -> str:
    if overall_level == "BAHAYA":
        return "PRIORITAS_1"
    if overall_level == "WASPADA":
        return "PRIORITAS_2"
    return "PRIORITAS_3"


def deterministic_analysis_text(facts: PreAnalysisFacts) -> str:
    level_intro = {
        "BAHAYA": "BAHAYA! Kondisi vibrasi berada pada level kritis dan berisiko menimbulkan kerusakan lanjutan.",
        "WASPADA": "WASPADA! Kondisi vibrasi tidak ideal dan perlu investigasi lebih lanjut.",
        "CUKUP": "CUKUP. Unit masih dapat beroperasi, namun perlu monitoring tren dengan ketat.",
        "BAIK": "BAIK. Tidak ada indikasi anomali yang signifikan dari data yang tersedia.",
    }[facts.overall_level]

    top_sentence = (
        f"Titik vibrasi tertinggi berada pada {facts.top_vibration_point} "
        f"({facts.top_vibration_metric.upper()}) sebesar {facts.top_vibration_value:.1f} mm/s."
    )

    if facts.fault_hypotheses:
        fault_sentence = (
            "Indikasi dominan mengarah ke "
            + ", ".join(hypothesis.fault_name.replace("_", " ") for hypothesis in facts.fault_hypotheses[:3])
            + "."
        )
    else:
        fault_sentence = "Belum ada pola fault dominan yang cukup kuat dari rules awal."

    evidence_parts = []
    for finding in facts.abnormal_findings[:4]:
        metric_name = finding.metric.upper()
        evidence_parts.append(f"{finding.point_label} {metric_name}={finding.value:.1f} ({finding.severity})")

    evidence_sentence = (
        "Temuan utama: " + "; ".join(evidence_parts) + "."
        if evidence_parts
        else "Tidak ada titik abnormal yang menonjol."
    )

    return " ".join([level_intro, top_sentence, fault_sentence, evidence_sentence])


def summarize_priority_tags(rows: list[dict], bucket: str, default_text: str) -> str:
    tags = [row["tag_name"] for row in rows if row["priority_bucket"] == bucket]
    if not tags:
        return default_text

    tag_list = ", ".join(tags)
    explanations = {
        "PRIORITAS_1": "Semua unit ini berada pada level bahaya dan memerlukan tindakan segera.",
        "PRIORITAS_2": "Unit perlu investigasi dan corrective maintenance terjadwal dalam waktu dekat.",
        "PRIORITAS_3": "Unit cukup aman untuk operasi, namun monitoring harus tetap dijaga.",
    }
    return f"{tag_list}. ({explanations[bucket]})"


def dominant_area(records: list[ParsedEquipmentRecord]) -> str:
    if not records:
        return "-"
    counter = Counter(item.area for item in records)
    return counter.most_common(1)[0][0]