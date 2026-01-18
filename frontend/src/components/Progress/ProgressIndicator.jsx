import React from 'react';
import { Check, Loader2 } from 'lucide-react';
import './ProgressIndicator.css';

const ProgressIndicator = ({ currentStep = 0 }) => {
    const steps = [
        { id: 1, text: 'Parsing your resume', icon: '📄' },
        { id: 2, text: 'Analyzing your experience', icon: '💼' },
        { id: 3, text: 'Extracting your skills', icon: '🎯' },
        { id: 4, text: 'Generating recommendations', icon: '✨' }
    ];

    return (
        <div className="progress-container">
            <div className="progress-header">
                <h2>Analyzing Your Resume</h2>
                <p>Please wait while we process your information...</p>
            </div>

            <div className="progress-steps">
                {steps.map((step, index) => {
                    const isComplete = index < currentStep;
                    const isCurrent = index === currentStep;
                    const isPending = index > currentStep;

                    return (
                        <div
                            key={step.id}
                            className={`progress-step ${isComplete ? 'complete' : ''} ${isCurrent ? 'active' : ''} ${isPending ? 'pending' : ''}`}
                        >
                            <div className="step-icon">
                                {isComplete ? (
                                    <Check size={20} className="check-icon" />
                                ) : isCurrent ? (
                                    <Loader2 size={20} className="spinner-icon" />
                                ) : (
                                    <span className="step-emoji">{step.icon}</span>
                                )}
                            </div>
                            <div className="step-text">
                                {step.text}
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default ProgressIndicator;
