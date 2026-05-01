import { useState } from 'react';
import type { ReportRow } from '../lib/types';
import SeverityBadge from './SeverityBadge';

export default function EquipmentTable({ rows }: { rows: ReportRow[] }) {
  const [expanded, setExpanded] = useState<Set<number>>(new Set());

  const toggle = (no: number) => {
    setExpanded((prev) => {
      const next = new Set(prev);
      if (next.has(no)) next.delete(no);
      else next.add(no);
      return next;
    });
  };

  return (
    <div className="bg-card border border-border rounded-lg overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border">
              <th className="text-left px-4 py-3 text-xs font-semibold uppercase tracking-wider text-text-secondary">No</th>
              <th className="text-left px-4 py-3 text-xs font-semibold uppercase tracking-wider text-text-secondary">Tag Name</th>
              <th className="text-left px-4 py-3 text-xs font-semibold uppercase tracking-wider text-text-secondary">Deskripsi</th>
              <th className="text-left px-4 py-3 text-xs font-semibold uppercase tracking-wider text-text-secondary">Titik & Nilai Vibrasi Tertinggi</th>
              <th className="text-left px-4 py-3 text-xs font-semibold uppercase tracking-wider text-text-secondary">Analisa</th>
              <th className="text-left px-4 py-3 text-xs font-semibold uppercase tracking-wider text-text-secondary">Rekomendasi</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => {
              const isExpanded = expanded.has(row.no);
              return (
                <tr
                  key={row.no}
                  className="border-b border-border/50 hover:bg-surface transition-colors"
                >
                  <td className="px-4 py-3 text-text-secondary">{row.no}</td>
                  <td className="px-4 py-3 font-medium">{row.tag_name}</td>
                  <td className="px-4 py-3 text-text-secondary">{row.deskripsi}</td>
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2">
                      <SeverityBadge level={row.overall_level} />
                      <span className="font-mono text-xs">{row.titik_nilai_vibrasi_tertinggi}</span>
                    </div>
                  </td>
                  <td className="px-4 py-3 max-w-xs">
                    <p className={isExpanded ? '' : 'line-clamp-3'}>{row.analysis}</p>
                    {row.analysis.length > 200 && (
                      <button
                        onClick={() => toggle(row.no)}
                        className="text-primary text-xs font-medium mt-1 hover:underline"
                      >
                        {isExpanded ? 'Show less' : 'Show more'}
                      </button>
                    )}
                  </td>
                  <td className="px-4 py-3 max-w-xs">
                    <ul className="list-disc list-inside space-y-1">
                      {row.recommendations.map((rec, i) => (
                        <li key={i} className="text-text-secondary text-xs">{rec}</li>
                      ))}
                    </ul>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
