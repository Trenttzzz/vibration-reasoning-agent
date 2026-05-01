import { useState } from 'react';
import type { FinalReport } from './lib/types';
import { analyze, ApiError } from './api/client';
import UploadZone from './components/UploadZone';
import AnalysisResults from './components/AnalysisResults';
import LoadingSpinner from './components/LoadingSpinner';

type Mode = 'agent' | 'fallback';

export default function App() {
  const [file, setFile] = useState<File | null>(null);
  const [mode, setMode] = useState<Mode>('agent');
  const [report, setReport] = useState<FinalReport | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    try {
      const result = await analyze(file, mode);
      setReport(result);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.detail);
      } else {
        setError('An unexpected error occurred. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    setReport(null);
    setFile(null);
    setError(null);
  };

  if (report) {
    return (
      <div className="min-h-screen bg-surface">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <AnalysisResults report={report} onBack={handleBack} />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-surface flex items-center justify-center px-4">
      <div className="w-full max-w-lg">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-semibold">Vibration Analysis Agent</h1>
          <p className="text-sm text-text-secondary mt-1">
            Upload vibration measurement data for AI-powered analysis
          </p>
        </div>

        <div className="bg-card border border-border rounded-lg p-6 space-y-5">
          <UploadZone onFileSelect={setFile} disabled={loading} />

          <div className="space-y-2">
            <label className="text-sm font-medium">Analysis Mode</label>
            <div className="flex gap-3">
              <label className="flex items-center gap-2 text-sm cursor-pointer">
                <input
                  type="radio"
                  name="mode"
                  value="agent"
                  checked={mode === 'agent'}
                  onChange={() => setMode('agent')}
                  disabled={loading}
                  className="accent-primary"
                />
                Agent (LLM-powered)
              </label>
              <label className="flex items-center gap-2 text-sm cursor-pointer">
                <input
                  type="radio"
                  name="mode"
                  value="fallback"
                  checked={mode === 'fallback'}
                  onChange={() => setMode('fallback')}
                  disabled={loading}
                  className="accent-primary"
                />
                Fallback (Deterministic)
              </label>
            </div>
          </div>

          {error && (
            <div className="bg-bahaya/10 border border-bahaya/20 text-bahaya text-sm rounded-md px-4 py-3">
              {error}
            </div>
          )}

          <button
            onClick={handleAnalyze}
            disabled={!file || loading}
            className="w-full py-2.5 bg-primary text-white text-sm font-medium rounded-md hover:bg-primary-hover disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Analyzing...' : 'Analyze'}
          </button>
        </div>

        {loading && <LoadingSpinner message="Analyzing vibration data..." />}
      </div>
    </div>
  );
}
