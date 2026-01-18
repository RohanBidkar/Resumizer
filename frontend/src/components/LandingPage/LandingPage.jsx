import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './LandingPage.css';
import Header from '../Header/Header';
import ProgressIndicator from '../Progress/ProgressIndicator';
import Antigravity from '../antigravity/Antigravity';
import { analyzeResume, isValidResumeFile, isValidFileSize } from '../../services/api';

const LandingPage = () => {
    const navigate = useNavigate();

    const [resumeFile, setResumeFile] = useState(null);
    const [jdFile, setJDFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [progressStep, setProgressStep] = useState(0);

    useEffect(() => {
        if (loading) {
            const intervals = [
                setTimeout(() => setProgressStep(0), 0),
                setTimeout(() => setProgressStep(1), 2000),
                setTimeout(() => setProgressStep(2), 4000),
                setTimeout(() => setProgressStep(3), 6000),
            ];
            return () => intervals.forEach(clearTimeout);
        }
    }, [loading]);

    const handleResumeChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            if (!isValidResumeFile(file)) {
                setError('Please upload a PDF or DOCX file');
                return;
            }
            if (!isValidFileSize(file)) {
                setError('File size must be less than 5MB');
                return;
            }
            setResumeFile(file);
            setError(null);
        }
    };

    const handleJDChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            if (!isValidResumeFile(file)) {
                setError('Please upload a PDF or DOCX file');
                return;
            }
            if (!isValidFileSize(file)) {
                setError('File size must be less than 5MB');
                return;
            }
            setJDFile(file);
            setError(null);
        }
    };

    const handleAnalyze = async () => {
        if (!resumeFile) {
            setError('Please upload a resume first');
            return;
        }

        setLoading(true);
        setError(null);
        setProgressStep(0);

        try {
            const result = await analyzeResume(resumeFile, jdFile);

            navigate('/resume-checker-result', {
                state: {
                    analysisResult: result,
                    resumeFileName: resumeFile.name,
                    jdFileName: jdFile?.name
                }
            });

        } catch (err) {
            console.error('❌ Analysis failed:', err);
            setError(err.message || 'Failed to analyze resume. Please try again.');
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="landing-container">
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
                <Header isLanding={true} />
                <ProgressIndicator currentStep={progressStep} />
            </div>
        );
    }

    return (
        <div className="landing-container">
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

            <Header isLanding={true} />

            <main className="hero-section">
                <h1 className="hero-title">
                    Resumizer
                </h1>

                <p className="hero-subtitle">
                    Get instant feedback on your resume. Our AI analyzes format, content, and ATS compatibility to help you land more interviews.
                </p>

                {error && (
                    <div className="error-message">
                        {error}
                    </div>
                )}

                <div className="upload-container">
                    <div className="upload-box">
                        <input
                            type="file"
                            accept=".pdf,.docx"
                            onChange={handleResumeChange}
                            style={{ display: 'none' }}
                            id="resume-upload"
                        />
                        <label htmlFor="resume-upload" style={{ cursor: 'pointer', width: '100%' }}>
                            <div className="upload-text">
                                <h3>
                                    {resumeFile
                                        ? resumeFile.name
                                        : 'Choose your resume'}
                                </h3>
                                <p>PDF or DOCX, up to 5MB</p>
                            </div>
                            <button
                                className="upload-cta"
                                type="button"
                                onClick={(e) => {
                                    e.preventDefault();
                                    document.getElementById('resume-upload').click();
                                }}
                            >
                                {resumeFile ? 'Change file' : 'Select file'}
                            </button>
                        </label>
                    </div>
                </div>

                <div className="jd-analyze-row">
                    <div className="jd-upload-compact">
                        <input
                            type="file"
                            accept=".pdf,.docx"
                            onChange={handleJDChange}
                            style={{ display: 'none' }}
                            id="jd-upload"
                        />
                        <label htmlFor="jd-upload" className="jd-label">
                            <span className="jd-icon">📋</span>
                            <span className="jd-text">
                                {jdFile ? jdFile.name : 'Job description (optional)'}
                            </span>
                        </label>
                    </div>

                    <button
                        onClick={handleAnalyze}
                        disabled={!resumeFile}
                        className="analyze-button"
                    >
                        Analyze
                    </button>
                </div>

                <p className="help-text">
                    Add a job description for personalized ATS scoring
                </p>
            </main>
        </div>
    );
};

export default LandingPage;
