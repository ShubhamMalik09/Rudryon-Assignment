import React, { useEffect, useState } from "react";
import { getAllSensors } from "../apis/sensors";
import SensorCard from "../components/SensorCard";
import { AlertsPanel } from "../components/AlertPanel";
import Header from "../components/Header";
import { Legend } from "../components/Legend";
import { StatCards } from "../components/StatCards";

const MainPage = () => {
  const [sensors, setSensors] = useState([]);
  const [ error, setError ] = useState(null);
  const [warnCount, setWarnCount ] = useState({});
  const [criticalCount, setCriticalCount] = useState({});

  useEffect(()=>{
    handleGetSensors();
  },[]);

  const handleGetSensors = async() =>{
    try{
        const result = await getAllSensors();
        setSensors(result);
        console.log(result);
    } catch(error){
        console.log(error.message || error);
        setSensors([]);
    }
  }

  return (
    <div className="min-h-screen bg-zinc-950 p-6 text-zinc-100">
      <div className="max-w-5xl mx-auto flex flex-col gap-5">
        <Header sensors={sensors} />
        <div className="flex w-full">
          <Legend />
        </div>
        {error && (
          <div className="text-xs text-amber-400 bg-amber-400/10 border border-amber-400/20 rounded-lg px-4 py-2">
            {error}
          </div>
        )}

        {/* <StatCards
          critCount={criticalCount}
          warnCount={warnCount}
        /> */}

        <div className="flex flex-col gap-3">
          {sensors.map((s) => (
            <SensorCard
              key={s.id}
              sensor={s}
              setCriticalCount={setCriticalCount}
              setWarnCount={setWarnCount}
            />
          ))}
        </div>

        <AlertsPanel />
      </div>
    </div>
  );
};

export default MainPage;
