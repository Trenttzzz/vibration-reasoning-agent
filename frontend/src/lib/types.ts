export type SeverityLabel = 'BAIK' | 'CUKUP' | 'WASPADA' | 'BAHAYA';

export type FaultName =
  | 'bearing_damage'
  | 'misalignment'
  | 'unbalance'
  | 'overheat_or_lubrication';

export type PriorityBucket = 'PRIORITAS_1' | 'PRIORITAS_2' | 'PRIORITAS_3';

export interface BearingMeasurement {
  ax: number | null;
  v: number | null;
  h: number | null;
  he: number | null;
  temp: number | null;
}

export interface EquipmentInfo {
  tag_name: string;
  deskripsi: string;
  pondasi: string | null;
  posisi: string | null;
  kw: number | null;
  ampere: number | null;
  rpm: number | null;
}

export interface OperationStatus {
  run: boolean;
  standby: boolean;
  repair: boolean;
}

export interface MetricFinding {
  point_label: string;
  metric: string;
  value: number;
  severity: SeverityLabel;
  notes: string | null;
}

export interface FaultHypothesis {
  fault_name: FaultName;
  confidence: number;
  evidence: string[];
}

export interface ReportMeta {
  title: string;
  tanggal_pengukuran: string;
  area: string;
  fokus_laporan: string;
}

export interface ReportRow {
  no: number;
  tag_name: string;
  deskripsi: string;
  titik_nilai_vibrasi_tertinggi: string;
  analysis: string;
  recommendations: string[];
  overall_level: SeverityLabel;
  priority_bucket: PriorityBucket;
}

export interface FinalReport {
  meta: ReportMeta;
  standard_reference_intro: string;
  thresholds: string[];
  rows: ReportRow[];
  priority_1_text: string;
  priority_2_text: string;
  priority_3_text: string;
  closing_note: string;
}
