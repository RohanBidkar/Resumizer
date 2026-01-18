import React from 'react';
import {
    FileText, CheckCircle2, XCircle, Sparkles,
    TrendingUp, AlertCircle, Info, Briefcase,
    Link, Trophy
} from 'lucide-react';
import './AnalysisResult.css';

const AnalysisResult = ({ result, resumeFileName, jdFileName }) => {
    const hasJD = !!result.ats_score;

    return (
        <div className="analysis-container">
            {/* Header / Title - Only on mobile/tablet where sidebar isn't dominant */}
            <div className="mobile-header">
                <h1 className="main-title">Analysis Report</h1>
                <p className="subtitle">Detailed breakdown of your resume's performance</p>
            </div>

            {/* Files Info Card */}
            <div className="result-card info-card">
                <div className="card-header">
                    <div className="icon-box blue">
                        <FileText size={20} />
                    </div>
                    <div>
                        <h3>Analyzed Documents</h3>
                        <p className="card-subtitle">Source files used for this analysis</p>
                    </div>
                </div>
                <div className="card-content row-content">
                    <div className="file-chip">
                        <span className="file-icon">📄</span>
                        <span className="file-name">{resumeFileName || 'Resume'}</span>
                    </div>
                    {jdFileName && (
                        <div className="file-chip">
                            <span className="file-icon">📋</span>
                            <span className="file-name">{jdFileName}</span>
                        </div>
                    )}
                </div>
            </div>

            {/* Overall Feedback Card */}
            {(result.overall_feedback || result.feedback) && (
                <div className="result-card feedback-card">
                    <div className="card-header">
                        <div className="icon-box purple">
                            <Info size={20} />
                        </div>
                        <h3>Executive Summary</h3>
                    </div>
                    <div className="card-content">
                        <p className="feedback-text">
                            {result.overall_feedback || result.feedback}
                        </p>
                    </div>
                </div>
            )}

            {/* Skills Section - Side by Side Grid */}
            {hasJD && (
                <div className="skills-grid-layout">
                    {/* Matched Skills */}
                    <div className="result-card matched-card">
                        <div className="card-header">
                            <div className="icon-box green">
                                <CheckCircle2 size={20} />
                            </div>
                            <h3>Matched Skills</h3>
                            <span className="count-badge green">{result.matched_skills?.length || 0}</span>
                        </div>
                        <div className="skills-cloud">
                            {result.matched_skills && result.matched_skills.map((skill, idx) => (
                                <span key={idx} className="skill-pill matched">
                                    {skill}
                                </span>
                            ))}
                            {(!result.matched_skills || result.matched_skills.length === 0) && (
                                <p className="empty-state">No matching skills found.</p>
                            )}
                        </div>
                    </div>

                    {/* Missing Skills */}
                    <div className="result-card missing-card">
                        <div className="card-header">
                            <div className="icon-box red">
                                <XCircle size={20} />
                            </div>
                            <h3>Missing Keywords</h3>
                            <span className="count-badge red">{result.missing_skills?.length || 0}</span>
                        </div>
                        <div className="skills-cloud">
                            {result.missing_skills && result.missing_skills.map((skill, idx) => (
                                <span key={idx} className="skill-pill missing">
                                    {skill}
                                </span>
                            ))}
                            {(!result.missing_skills || result.missing_skills.length === 0) && (
                                <p className="empty-state">No missing skills detected! 🎉</p>
                            )}
                        </div>
                    </div>
                </div>
            )}

            {/* Strengths Card */}
            {result.strengths && result.strengths.length > 0 && (
                <div className="result-card strengths-card">
                    <div className="card-header">
                        <div className="icon-box teal">
                            <TrendingUp size={20} />
                        </div>
                        <h3>Key Strengths</h3>
                    </div>
                    <ul className="modern-list">
                        {result.strengths.map((strength, idx) => (
                            <li key={idx}>
                                <span className="bullet teal">•</span>
                                {strength}
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Suggestions Card */}
            {result.suggestions && result.suggestions.length > 0 && (
                <div className="result-card suggestions-card">
                    <div className="card-header">
                        <div className="icon-box orange">
                            <Sparkles size={20} />
                        </div>
                        <h3>Actionable Improvements</h3>
                    </div>
                    <ul className="modern-list">
                        {result.suggestions.map((suggestion, idx) => (
                            <li key={idx}>
                                <span className="bullet orange">→</span>
                                {suggestion}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default AnalysisResult;
