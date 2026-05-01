import type { FinalReport } from '../lib/types';

const API_BASE = '/api/v1';

export class ApiError extends Error {
  status: number;
  detail: string;

  constructor(status: number, detail: string) {
    super(detail);
    this.name = 'ApiError';
    this.status = status;
    this.detail = detail;
  }
}

export async function analyze(file: File, mode: string): Promise<FinalReport> {
  const form = new FormData();
  form.append('file', file);
  form.append('mode', mode);

  const res = await fetch(`${API_BASE}/analyze`, {
    method: 'POST',
    body: form,
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: 'Unknown error' }));
    throw new ApiError(res.status, body.detail || 'Analysis failed');
  }

  return res.json();
}
