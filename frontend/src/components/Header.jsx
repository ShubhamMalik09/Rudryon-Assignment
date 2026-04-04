import React from 'react'

const Header = ({sensors}) => {
   return (
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-3">
        {/* <span className="w-2 h-2 rounded-full bg-green-400" /> */}
        <h1 className="text-2xl font-semibold text-zinc-100">Sensor Dashboard</h1>
        <span className="text-base text-zinc-500 border border-zinc-800 rounded px-2 py-0.5">
          {sensors.length} units · Live
        </span>
      </div>
    </div>
  );
}

export default Header