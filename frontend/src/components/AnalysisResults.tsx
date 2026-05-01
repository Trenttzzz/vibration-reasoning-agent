import { useState } from 'react';
import type { FinalReport } from '../lib/types';
import ReportMeta from './ReportMeta';
import EquipmentTable from './EquipmentTable';
import PrioritySummary from './PrioritySummary';

interface AnalysisResultsProps {
  report: FinalReport;
  onBack: () => void;
}

export default function AnalysisResults({ report, onBack }: AnalysisResultsProps) {
  const [showThresholds, setShowThresholds] = useState(false);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold">Analysis Report</h1>
        <button
          onClick={onBack}
          className="px-4 py-2 text-sm font-medium border border-border rounded-md hover:bg-card transition-colors"
        >
          New Analysis
        </button>
      </div>

      <ReportMeta meta={report.meta} />

      <div>
        <h2 className="text-lg font-semibold mb-3">Equipment Analysis</h2>
        <EquipmentTable rows={report.rows} />
      </div>

      <PrioritySummary
        priority_1_text={report.priority_1_text}
        priority_2_text={report.priority_2_text}
        priority_3_text={report.priority_3_text}
      />

      <div className="bg-card border border-border rounded-lg">
        <button
          onClick={() => setShowThresholds(!showThresholds)}
          className="w-full flex items-center justify-between px-5 py-3 text-sm font-medium"
        >
          <span>ISO 10816-3 Threshold Reference</span>
          <svg
            className={`w-4 h-4 transition-transform ${showThresholds ? 'rotate-180' : ''}`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </button>
        {showThresholds && (
          <div className="px-5 pb-4 border-t border-border pt-3">
            <p className="text-sm text-text-secondary mb-3">{report.standard_reference_intro}</p>
            <ul className="list-disc list-inside space-y-1">
              {report.thresholds.map((t, i) => (
                <li key={i} className="text-sm text-text-secondary">{t}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      <p className="text-xs text-outline text-center pb-4">{report.closing_note}</p>
    </div>
  );
}
