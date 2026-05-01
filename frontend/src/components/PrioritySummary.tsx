interface PriorityCardProps {
  level: 1 | 2 | 3;
  text: string;
}

const accentColors: Record<number, string> = {
  1: 'border-l-bahaya',
  2: 'border-l-waspada',
  3: 'border-l-baik',
};

const labels: Record<number, string> = {
  1: 'PRIORITAS 1 — Immediate Action',
  2: 'PRIORITAS 2 — Schedule Investigation',
  3: 'PRIORITAS 3 — Tighten Monitoring',
};

function PriorityCard({ level, text }: PriorityCardProps) {
  return (
    <div className={`bg-card border border-border rounded-lg p-4 border-l-4 ${accentColors[level]}`}>
      <h3 className="text-sm font-semibold mb-2">{labels[level]}</h3>
      <p className="text-sm text-text-secondary whitespace-pre-line">{text}</p>
    </div>
  );
}

interface PrioritySummaryProps {
  priority_1_text: string;
  priority_2_text: string;
  priority_3_text: string;
}

export default function PrioritySummary({
  priority_1_text,
  priority_2_text,
  priority_3_text,
}: PrioritySummaryProps) {
  return (
    <div className="space-y-3">
      <h2 className="text-lg font-semibold">Priority Summary</h2>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <PriorityCard level={1} text={priority_1_text} />
        <PriorityCard level={2} text={priority_2_text} />
        <PriorityCard level={3} text={priority_3_text} />
      </div>
    </div>
  );
}
