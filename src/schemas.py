from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator


SeverityLabel = Literal["BAIK", "CUKUP", "WASPADA", "BAHAYA"]
FaultName = Literal[
    "bearing_damage",
    "misalignment",
    "unbalance",
    "overheat_or_lubrication",
]


class BearingMeasurement(BaseModel):
    ax: float | None = None
    v: float | None = None
    h: float | None = None
    he: float | None = None
    temp: float | None = None


class EquipmentInfo(BaseModel):
    tag_name: str = Field(..., description="Kode tag unik equipment")
    deskripsi: str = Field(..., description="Nama atau deskripsi equipment")
    pondasi: str | None = None
    posisi: str | None = None
    kw: float | None = None
    ampere: float | None = None
    rpm: float | None = None


class OperationStatus(BaseModel):
    run: bool = False
    standby: bool = False
    repair: bool = False

    @model_validator(mode="after")
    def ensure_only_one_status(self) -> "OperationStatus":
        true_count = sum([self.run, self.standby, self.repair])
        if true_count > 1:
            raise ValueError("Hanya satu status operasi yang boleh bernilai true.")
        return self


class DriverData(BaseModel):
    NDE: BearingMeasurement
    DE: BearingMeasurement
    grounding: str | None = None
    temp_terminal_box: float | None = None


class DrivenData(BaseModel):
    DE: BearingMeasurement
    NDE: BearingMeasurement


class ParsedEquipmentRecord(BaseModel):
    tanggal: str
    no: int
    area: str
    equipment: EquipmentInfo
    status: OperationStatus
    driver: DriverData
    driven: DrivenData


class MetricFinding(BaseModel):
    point_label: str
    metric: Literal["ax", "v", "h", "he", "temp"]
    value: float
    severity: SeverityLabel
    notes: str | None = None


class FaultHypothesis(BaseModel):
    fault_name: FaultName
    confidence: float = Field(..., ge=0.0, le=1.0)
    evidence: list[str] = Field(default_factory=list)


class PreAnalysisFacts(BaseModel):
    no: int
    tanggal: str
    area: str
    tag_name: str
    deskripsi: str
    running: bool
    top_vibration_point: str
    top_vibration_value: float
    top_vibration_metric: Literal["ax", "v", "h", "he"]
    overall_level: SeverityLabel
    abnormal_findings: list[MetricFinding] = Field(default_factory=list)
    fault_hypotheses: list[FaultHypothesis] = Field(default_factory=list)


class EquipmentNarrative(BaseModel):
    no: int
    tag_name: str
    deskripsi: str
    titik_nilai_vibrasi_tertinggi: str
    overall_level: SeverityLabel
    analysis: str
    recommendations: list[str]
    priority_bucket: Literal["PRIORITAS_1", "PRIORITAS_2", "PRIORITAS_3"]


class ReportMeta(BaseModel):
    title: str
    tanggal_pengukuran: str
    area: str
    fokus_laporan: str


class ReportRow(BaseModel):
    no: int
    tag_name: str
    deskripsi: str
    titik_nilai_vibrasi_tertinggi: str
    analysis: str
    recommendations: list[str]
    overall_level: SeverityLabel
    priority_bucket: Literal["PRIORITAS_1", "PRIORITAS_2", "PRIORITAS_3"]


class FinalReport(BaseModel):
    meta: ReportMeta
    standard_reference_intro: str
    thresholds: list[str]
    rows: list[ReportRow]
    priority_1_text: str
    priority_2_text: str
    priority_3_text: str
    closing_note: str