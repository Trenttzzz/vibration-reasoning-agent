import type { SeverityLabel } from '../lib/types';

const colorMap: Record<SeverityLabel, string> = {
  BAIK: 'bg-baik text-white',
  CUKUP: 'bg-cukup text-white',
  WASPADA: 'bg-waspada text-white',
  BAHAYA: 'bg-bahaya text-white',
};

export default function SeverityBadge({ level }: { level: SeverityLabel }) {
  return (
    <span
      className={`inline-block px-2.5 py-0.5 rounded-full text-xs font-semibold tracking-wide ${colorMap[level]}`}
    >
      {level}
    </span>
  );
}
