import { useState } from 'react'
import { Route, Routes } from 'react-router-dom'
import MainPage from './pages/MainPage'
import AlertsPage from './pages/AlertsPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<MainPage />} />
      <Route path="/alerts" element={<AlertsPage />} />
    </Routes>
  )
}

export default App
