import React from 'react';
import './ScoreGauge.css';
import { Award, Zap, BookOpen, Briefcase } from 'lucide-react';

const ScoreGauge = ({ score = 0, scoreBreakdown = null, hasJD = true }) => {
    // Use actual score from backend
    const displayScore = Math.round(score);

    // Calculate stroke dasharray for the gauge
    const radius = 80;
    const arcLength = Math.PI * radius; // Semi-circle arc length
    const strokeDashoffset = arcLength - (arcLength * displayScore) / 100;

    // Determine status and color based on score
    let status = "Needs Improvement";
    let statusColor = "#ef4444"; // red-500

    if (displayScore > 60) {
        status = "Good";
        statusColor = "#eab308"; // yellow-500
    }
    if (displayScore > 80) {
        status = "Excellent";
        statusColor = "#22c55e"; // green-500
    }

    return (
        <div className="score-wrapper">
            <div className="gauge-section">
                <div className="gauge-container">
                    <svg viewBox="0 0 200 110" className="gauge-svg">
                        <defs>
                            <linearGradient id="gaugeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                                <stop offset="0%" stopColor="#ef4444" />
                                <stop offset="50%" stopColor="#eab308" />
                                <stop offset="100%" stopColor="#22c55e" />
                            </linearGradient>
                            <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                                <feGaussianBlur stdDeviation="3" result="coloredBlur" />
                                <feMerge>
                                    <feMergeNode in="coloredBlur" />
                                    <feMergeNode in="SourceGraphic" />
                                </feMerge>
                            </filter>
                        </defs>

                        {/* Background Track */}
                        <path
                            d="M 20 100 A 80 80 0 0 1 180 100"
                            fill="none"
                            stroke="#e5e7eb"
                            strokeWidth="12"
                            strokeLinecap="round"
                        />

                        {/* Progress Arc */}
                        <path
                            d="M 20 100 A 80 80 0 0 1 180 100"
                            fill="none"
                            stroke="url(#gaugeGradient)"
                            strokeWidth="12"
                            strokeLinecap="round"
                            strokeDasharray={arcLength}
                            strokeDashoffset={strokeDashoffset}
                            filter="url(#glow)"
                            className="gauge-progress"
                        />
                    </svg>

                    <div className="score-content">
                        <h2 className="score-text">
                            {displayScore}
                            <span className="percent">%</span>
                        </h2>
                        <div className="status-badge" style={{ color: statusColor, borderColor: statusColor }}>
                            {status}
                        </div>
                    </div>
                </div>
            </div>

            {/* Visual Breakdown */}
            {scoreBreakdown && (
                <div className="breakdown-section">
                    <h3 className="breakdown-title">Score Breakdown</h3>

                    <div className="breakdown-grid">
                        <div className="breakdown-item">
                            <div className="breakdown-header">
                                <span className="icon-wrapper"><Zap size={16} /> Skills</span>
                                <span className="score-value">{scoreBreakdown.skills_score}/40</span>
                            </div>
                            <div className="progress-bar-bg">
                                <div
                                    className="progress-bar-fill"
                                    style={{ width: `${(scoreBreakdown.skills_score / 40) * 100}%` }}
                                ></div>
                            </div>
                        </div>

                        <div className="breakdown-item">
                            <div className="breakdown-header">
                                <span className="icon-wrapper"><Briefcase size={16} /> Experience</span>
                                <span className="score-value">{scoreBreakdown.experience_score}/30</span>
                            </div>
                            <div className="progress-bar-bg">
                                <div
                                    className="progress-bar-fill"
                                    style={{ width: `${(scoreBreakdown.experience_score / 30) * 100}%` }}
                                ></div>
                            </div>
                        </div>

                        <div className="breakdown-item">
                            <div className="breakdown-header">
                                <span className="icon-wrapper"><BookOpen size={16} /> Education</span>
                                <span className="score-value">{scoreBreakdown.education_score}/15</span>
                            </div>
                            <div className="progress-bar-bg">
                                <div
                                    className="progress-bar-fill"
                                    style={{ width: `${(scoreBreakdown.education_score / 15) * 100}%` }}
                                ></div>
                            </div>
                        </div>

                        <div className="breakdown-item">
                            <div className="breakdown-header">
                                <span className="icon-wrapper"><Award size={16} /> Quality</span>
                                <span className="score-value">{scoreBreakdown.quality_score}/15</span>
                            </div>
                            <div className="progress-bar-bg">
                                <div
                                    className="progress-bar-fill"
                                    style={{ width: `${(scoreBreakdown.quality_score / 15) * 100}%` }}
                                ></div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ScoreGauge;
