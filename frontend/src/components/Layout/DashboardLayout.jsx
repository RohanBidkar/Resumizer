import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './DashboardLayout.css';
import Header from '../Header/Header';
import ScoreGauge from '../ScoreGauge/ScoreGauge';
import AnalysisResult from '../AnalysisResult/AnalysisResult';
import Antigravity from '../antigravity/Antigravity';

const DashboardLayout = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { analysisResult, resumeFileName, jdFileName } = location.state || {};

  if (!analysisResult) {
    return (
      <div className="dashboard-container">
        {/* Animated background */}
        <div className="antigravity-background">
          <Antigravity
            count={300}
            magnetRadius={6}
            ringRadius={7}
            waveSpeed={0.4}
            waveAmplitude={1}
            particleSize={1.5}
            lerpSpeed={0.05}
            color={'#312e81'}
            autoAnimate={true}
            particleVariance={1}
          />
        </div>
        <Header />
        <main className="no-data-container">
          <div className="no-data-card">
            <h2>⚠️ No Analysis Data Found</h2>
            <p>Please upload a resume from the landing page to see results.</p>
            <button
              onClick={() => navigate('/resume-checker')}
              className="back-button"
            >
              Go to Upload Page
            </button>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      {/* Animated background */}
      <div className="antigravity-background">
        <Antigravity
          count={300}
          magnetRadius={6}
          ringRadius={7}
          waveSpeed={0.4}
          waveAmplitude={1}
          particleSize={1.5}
          lerpSpeed={0.05}
          color={'#312e81'}
          autoAnimate={true}
          particleVariance={1}
        />
      </div>
      <Header />
      <main className="results-main">
        <div className="results-grid">
          {/* Left Column: Score Card - Sticky on Desktop */}
          <div className="results-sidebar">
            <div className="sticky-wrapper">
              <ScoreGauge
                score={analysisResult.ats_score || analysisResult.quality_score}
                scoreBreakdown={analysisResult.score_breakdown}
                hasJD={!!analysisResult.ats_score}
              />

              <div className="action-buttons-sidebar">
                <button
                  onClick={() => window.print()}
                  className="primary-button full-width"
                >
                  Download Report
                </button>
                <button
                  onClick={() => navigate('/resume-checker')}
                  className="secondary-button full-width"
                >
                  Analyze Another
                </button>
              </div>
            </div>
          </div>

          {/* Right Column: Detailed Analysis */}
          <div className="results-content">
            <AnalysisResult
              result={analysisResult}
              resumeFileName={resumeFileName}
              jdFileName={jdFileName}
            />
          </div>
        </div>
      </main>
    </div>
  );
};

export default DashboardLayout;
