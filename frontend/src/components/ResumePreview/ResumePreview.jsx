import React from 'react';
import { Download, Share2, Maximize2 } from 'lucide-react';
import './ResumePreview.css';

const ResumePreview = () => {
    return (
        <div className="resume-preview-container">
            <div className="resume-header">
                <h3>Main Resume</h3>
                <div className="resume-actions">
                    <button className="action-icon" title="Zoom"><Maximize2 size={18} /></button>
                    <button className="action-icon" title="Download"><Download size={18} /></button>
                    <button className="action-icon" title="Share"><Share2 size={18} /></button>
                </div>
            </div>

            <div className="resume-scroll-area">
                {/* Mock Resume Document */}
                <div className="mock-resume">
                    <header className="mock-header">
                        <h1>Rohan Sharma</h1>
                        <p>Full Stack Developer</p>
                        <div className="contact-info">
                            <span>rohan@example.com</span> •
                            <span>+91 98765 43210</span> •
                            <span>github.com/rohan</span>
                        </div>
                    </header>

                    <section className="mock-section">
                        <h4>Experience</h4>
                        <div className="job">
                            <div className="job-header">
                                <span className="company">Tech Innovators Inc.</span>
                                <span className="date">2022 - Present</span>
                            </div>
                            <p className="role">Senior Frontend Engineer</p>
                            <ul>
                                <li>Led development of a React-based analytics dashboard used by 50k+ users.</li>
                                <li>Reduced initial load time by 40% using code splitting and lazy loading.</li>
                            </ul>
                        </div>

                        <div className="job">
                            <div className="job-header">
                                <span className="company">WebSolutions Ltd.</span>
                                <span className="date">2020 - 2022</span>
                            </div>
                            <p className="role">Junior Developer</p>
                            <ul>
                                <li>Collaborated with design team to implement responsive UI components.</li>
                                <li>Maintained legacy codebases and improved test coverage by 20%.</li>
                            </ul>
                        </div>
                    </section>

                    <section className="mock-section">
                        <h4>Education</h4>
                        <div className="school">
                            <div className="job-header">
                                <span className="company">State University</span>
                                <span className="date">2016 - 2020</span>
                            </div>
                            <p>B.Tech in Computer Science</p>
                        </div>
                    </section>

                    <section className="mock-section">
                        <h4>Skills</h4>
                        <div className="skills-list">
                            <span className="skill-tag">React</span>
                            <span className="skill-tag">Node.js</span>
                            <span className="skill-tag">CSS3</span>
                            <span className="skill-tag">Python</span>
                            <span className="skill-tag">Docker</span>
                            <span className="skill-tag">AWS</span>
                        </div>
                    </section>
                </div>
            </div>
        </div>
    );
};

export default ResumePreview;
