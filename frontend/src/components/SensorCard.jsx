import React, { useEffect, useState } from 'react'
import { calcStats, colorStyles, relTime, tempColor, tempLabel } from '../utils/sensor';
import SparkLine from './SparkLine';
import { WS_URL } from '../lib/config';
import useWebSocket from '../hooks/useWebsocket';

const SensorCard = ({sensor, setCriticalCount, setWarnCount}) => {
    const [ color, setColor ] = useState("green");
    const [ readingsData, setReadingsData ] = useState({ min: 0, max: 0, avg: 0});
    const [ readingStyles, setReadingStyles ] = useState(colorStyles(color));
    const [ readings, setReadings ] = useState([])
    const [ currentTemp, setCurrentTemp ] = useState(null);
    const [ isAnomaly, setIsAnomaly ] = useState(false)

    useWebSocket(`${WS_URL}/ws/sensors/${sensor.id}/readings`, (msg) => {
      setReadings(msg);
    });

    useEffect(()=>{
        if(readings.length > 0){
            const newcolor = tempColor(readings?.[0]?.temperature);
            const newcolorstyles = colorStyles(newcolor);
            const newReadingsData = calcStats(readings);
            if (readings.some((x) => x.is_anomaly)){
              setIsAnomaly(true)
            }
            else{
              setIsAnomaly(false);
            }
            if (readings.some((x) => (x.temperature>=70 && x.temperature<80))){
              setWarnCount((prev) =>({...prev, [sensor.id]: true}))
            }else{
              setWarnCount((prev) =>({...prev, [sensor.id]: false}))
            }

            if (readings.some((x) =>  x.temperature>80)){
              setCriticalCount((prev) =>({...prev, [sensor.id]: true}))
            }else{
              setCriticalCount((prev) =>({...prev, [sensor.id]: false}))
            }
            
            setReadingsData(newReadingsData);
            setReadingStyles(newcolorstyles);
            setCurrentTemp(readings?.[0]?.temperature);
            setColor(newcolor);
        }
    },[readings]);

  return (
    <div
      className={`bg-zinc-900 rounded-xl border border-zinc-800 border-l-4 ${readingStyles.border} flex flex-col overflow-hidden`}
    >
      {/* info row */}
      <div className="flex items-center gap-6 px-5 pt-4 pb-3">
        {/* name + location */}
        <div className="w-36 shrink-0">
          <div className="text-sm font-semibold text-zinc-100">{sensor.name}</div>
          {/* <div className="text-xs text-zinc-500 mt-0.5">{sensor?.loc}</div> */}
        </div>
 
        {/* current temp */}
        <div className="w-28 shrink-0">
          <span className={`text-4xl font-semibold tabular-nums ${readingStyles.text}`}>
            {currentTemp != null ? currentTemp.toFixed(1) : "--"}°
          </span>
          <span className="text-zinc-600 text-sm ml-1">C</span>
        </div>
 
        {/* status + anomaly badges */}
        <div className="flex gap-2 items-center">
          <span className={`text-[10px] font-medium px-2.5 py-0.5 rounded-full border ${readingStyles.pill}`}>
            {tempLabel(currentTemp)}
          </span>
          {isAnomaly && (
            <span className="text-[10px] font-medium px-2.5 py-0.5 rounded-full border bg-orange-400/10 text-orange-400 border-orange-400/30">
              ▲ Anomaly
            </span>
          )}
        </div>
 
        {/* stats + updated */}
        <div className="ml-auto flex gap-6 text-right">
          {[
            ["min", readingsData.min],
            ["avg", readingsData.avg],
            ["max", readingsData.max],
          ].map(([label, val]) => (
            <div key={label}>
              <div className="text-[10px] text-zinc-600 uppercase tracking-wider">{label}</div>
              <div className="text-sm font-semibold text-zinc-300 tabular-nums">{val}°</div>
            </div>
          ))}
          {/* <div>
            <div className="text-[10px] text-zinc-600 uppercase tracking-wider">updated</div>
            <div className="text-sm font-semibold text-zinc-300">
              {readings?.[0]?.timestamp ? relTime(readings?.[0]?.timestamp) : "--"}
            </div>
          </div> */}
        </div>
      </div>
 
      {/* full-width sparkline */}
      <SparkLine readings={readings} color={color} />
    </div>
  );
}

export default SensorCard