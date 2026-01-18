import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import DashboardLayout from './components/Layout/DashboardLayout';
import LandingPage from './components/LandingPage/LandingPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/resume-checker" replace />} />
        <Route path="/resume-checker" element={<LandingPage />} />
        <Route path="/resume-checker-result" element={<DashboardLayout />} />
      </Routes>
    </Router>
  );
}

export default App;
