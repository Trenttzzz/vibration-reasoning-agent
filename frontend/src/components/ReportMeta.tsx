import type { ReportMeta as ReportMetaType } from '../lib/types';

export default function ReportMeta({ meta }: { meta: ReportMetaType }) {
  return (
    <div className="bg-card border border-border rounded-lg p-5">
      <h2 className="text-lg font-semibold mb-3">{meta.title}</h2>
      <dl className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-sm">
        <div>
          <dt className="text-text-secondary">Tanggal Pengukuran</dt>
          <dd className="font-medium mt-0.5">{meta.tanggal_pengukuran}</dd>
        </div>
        <div>
          <dt className="text-text-secondary">Area</dt>
          <dd className="font-medium mt-0.5">{meta.area}</dd>
        </div>
        <div>
          <dt className="text-text-secondary">Fokus Laporan</dt>
          <dd className="font-medium mt-0.5">{meta.fokus_laporan}</dd>
        </div>
      </dl>
    </div>
  );
}
