export function StatCards({ avgTemp, critCount, warnCount }) {
  const stats = [
    {
      label: "critical units",
      value: Object.values(critCount).filter(v => v === true).length,
      color: Object.values(critCount).filter(v => v === true).length > 0 ? "text-red-400" : "text-zinc-100",
    },
    {
      label: "warning units",
      value: Object.values(warnCount).filter(v => v === true).length,
      color: Object.values(warnCount).filter(v => v === true).length > 0 ? "text-yellow-400" : "text-zinc-100",
    },
  ];

  return (
    <div className="grid grid-cols-3 gap-4">
      {stats.map(({ label, value, color }) => (
        <div key={label} className="bg-zinc-900 rounded-xl border border-zinc-800 px-5 py-4">
          <div className="text-xs text-zinc-500 mb-1">{label}</div>
          <div className={`text-2xl font-semibold tabular-nums ${color}`}>{value}</div>
        </div>
      ))}
    </div>
  );
}