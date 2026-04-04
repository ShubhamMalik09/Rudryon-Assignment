import { relTime } from "../utils/sensor";

export function AlertRow({ alert }) {
    console.log(alert)
  return (
    <div className="grid grid-cols-5 items-center gap-4 px-4 py-3 rounded-lg bg-red-500/5 border border-red-500/20 text-sm w-full">
        <div className="flex w-full gap-4 items-center">
            <span className="w-2 h-2 rounded-full bg-red-400 shrink-0" />
            <span className="font-semibold text-zinc-200 shrink-0 w-full">
                {alert?.sensor_name ?? `Sensor ${alert.sensor_id}`}
            </span>
        </div>
        {alert?.rolling_avg && (
            <div className="flex w-full items-center justify-center">
                <span className="text-zinc-500 text-xs">
                    {alert?.rolling_avg?.toFixed(2)}
                </span>
            </div>
        )}
        <div className="flex w-full items-center justify-center">
            {
                alert.is_anomaly && (
                    <span className="text-[10px] px-2 py-0.5 rounded-full border bg-orange-400/10 text-orange-400 border-orange-400/30 font-medium">
                    ▲ Anomaly
                    </span>
                )
            }
        </div>
      <div className="flex w-full items-center justify-center">
        <span className="font-semibold text-red-400 w-16 text-right tabular-nums">
            {alert.temperature?.toFixed(1)}°C
        </span>
      </div>
      <div className="flex w-full items-center justify-center">
        <span className="text-xs text-zinc-600 w-16 text-right">
            {alert.timestamp ? relTime(alert.timestamp) : "--"}
        </span>
      </div>
    </div>
  );
}