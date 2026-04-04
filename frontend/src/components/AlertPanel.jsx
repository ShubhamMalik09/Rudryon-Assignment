import { useState } from "react";
import { AlertRow } from "./AlertRow";
import useWebSocket from "../hooks/useWebsocket";
import { WS_URL } from "../lib/config";

export function AlertsPanel() {
  const [alerts, setAlerts] = useState([]);

  useWebSocket(`${WS_URL}/ws/sensors/alerts`, (msg) => {
    setAlerts(msg);
  });

  return (
    <div className="bg-zinc-900 rounded-xl border border-zinc-800 p-5 flex flex-col">
      <div className="flex items-center gap-3 mb-4 w-full">
        <span className="text-sm font-semibold text-zinc-100">Alerts</span>
        <span
          className={`text-[10px] font-medium px-2.5 py-0.5 rounded-full border ${
            alerts.length > 0
              ? "bg-red-500/10 text-red-400 border-red-500/30"
              : "bg-zinc-800 text-zinc-500 border-zinc-700"
          }`}
        >
          {alerts.length} event{alerts.length !== 1 ? "s" : ""}
        </span>
      </div>

      {alerts.length === 0 ? (
        <p className="text-xs text-zinc-600 py-1">
          All sensors within normal range.
        </p>
      ) : (
        <div className="flex flex-col gap-2 w-full">
            <div className="grid grid-cols-5 w-full gap-4">
                <span className="ml-10 text-xs text-gray-300">Sensor Name</span>
                <span className="text-center text-xs text-gray-300">Rolling Average</span>
                <span className="text-center text-xs text-gray-300">Is Anamoly</span>
                <span className="text-center text-xs text-gray-300">Temperature</span>
                <span className="text-center text-xs text-gray-300">Updated At</span>
            </div>
          {alerts.map((a, i) => (
            <AlertRow key={a.id ?? i} alert={a} />
          ))}
        </div>
      )}
    </div>
  );
}