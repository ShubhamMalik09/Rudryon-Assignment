export function tempColor(t) {
  if (t >= 80) return "red";
  if (t >= 70) return "yellow";
  return "green";
}

export function tempLabel(t) {
  if (t >= 80) return "Critical";
  if (t >= 70) return "Warning";
  return "Nominal";
}

export function relTime(ts) {
  const s = Math.floor((Date.now() - new Date(ts)) / 1000);
  if (s < 60) return `${s}s ago`;
  return `${Math.floor(s / 60)}m ago`;
}

export function colorStyles(color) {
  return {
    border:
      color === "red"
        ? "border-l-red-500"
        : color === "yellow"
        ? "border-l-yellow-400"
        : "border-l-green-500",
    text:
      color === "red"
        ? "text-red-400"
        : color === "yellow"
        ? "text-yellow-400"
        : "text-green-400",
    pill:
      color === "red"
        ? "bg-red-500/10 text-red-400 border-red-500/30"
        : color === "yellow"
        ? "bg-yellow-400/10 text-yellow-400 border-yellow-400/30"
        : "bg-green-500/10 text-green-400 border-green-500/30",
    stroke:
      color === "red" ? "#f87171" : color === "yellow" ? "#fbbf24" : "#4ade80",
    fill:
      color === "red"
        ? "rgba(248,113,113,0.08)"
        : color === "yellow"
        ? "rgba(251,191,36,0.08)"
        : "rgba(74,222,128,0.08)",
  };
}

export function calcStats(readings) {
  const temps = readings?.map((r) => r.temperature) ?? [];
  if (!temps.length) return { min: "--", max: "--", avg: "--" };
  return {
    min: Math.min(...temps).toFixed(1),
    max: Math.max(...temps).toFixed(1),
    avg: (temps.reduce((a, b) => a + b, 0) / temps.length).toFixed(1),
  };
}