import React from 'react'
import { colorStyles } from "../utils/sensor";

const SparkLine = ({readings, color}) => {
  if (!readings || readings.length < 2) {
      return (
      <div className="w-full h-14 flex items-center justify-center text-xs text-zinc-600">
          no data
      </div>
      );
  }

  const temps = [...readings].reverse().map((r) => r.temperature);
  const min = Math.min(...temps);
  const max = Math.max(...temps);
  const range = max - min || 1;
 
  const W = 1000;
  const H = 56;
  const PX = 6;
  const PY = 6;
 
  const pts = temps.map((t, i) => {
    const x = PX + (i / (temps.length - 1)) * (W - PX * 2);
    const y = PY + (1 - (t - min) / range) * (H - PY * 2);
    return [x, y];
  });
 
  const polyline = pts.map(([x, y]) => `${x.toFixed(2)},${y.toFixed(2)}`).join(" ");
 
  const areaPoints = [
    `${pts[0][0].toFixed(2)},${H}`,
    ...pts.map(([x, y]) => `${x.toFixed(2)},${y.toFixed(2)}`),
    `${pts[pts.length - 1][0].toFixed(2)},${H}`,
  ].join(" ");
 
  const [lx, ly] = pts[pts.length - 1];
  const { stroke, fill } = colorStyles(color);
  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full h-14" preserveAspectRatio="none">
      <polygon points={areaPoints} fill={fill} />
      <polyline
        points={polyline}
        fill="none"
        stroke={stroke}
        strokeWidth="2"
        strokeLinejoin="round"
        strokeLinecap="round"
      />
      <circle cx={lx.toFixed(2)} cy={ly.toFixed(2)} r="4" fill={stroke} />
    </svg>
  )
}

export default SparkLine