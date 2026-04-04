const LEGEND_ITEMS = [
  { color: "bg-green-500", label: "Nominal <70°C" },
  { color: "bg-yellow-400", label: "Warning 70–80°C" },
  { color: "bg-red-500", label: "Critical >80°C" },
];

export function Legend() {
  return (
    <div className="flex justify-evenly gap-5 text-sm text-zinc-600 pb-2 flex-wrap w-full">
      {LEGEND_ITEMS.map(({ color, label }) => (
        <span key={label} className="flex items-center gap-1.5">
          <span className={`w-2 h-2 rounded-full ${color}`} />
          {label}
        </span>
      ))}
      <span className="flex items-center gap-1.5 text-orange-500/70">
        ▲ Anomaly — hourly avg up 15%
      </span>
    </div>
  );
}