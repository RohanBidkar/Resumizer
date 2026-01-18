import React from 'react';
import { UserCircle, Hexagon } from 'lucide-react';
import './Header.css';

const Header = ({ isLanding = false }) => {
    return (
        <header className={`app-header ${isLanding ? 'landing-header' : ''}`}>
            <div className="logo-section">
                {/* If landing, use text based logo mainly */}
                {!isLanding && (
                    <div className="logo-icon">
                        <Hexagon size={28} fill="var(--primary-orange)" stroke="none" />
                        <span className="logo-letter">R</span>
                    </div>
                )}
                <h1 className="app-name">
                    <span className="logo-gradient">Resumizer</span>
                </h1>
            </div>

            {isLanding ? (
                <nav className="landing-nav">
                    <a href="#">Resume Templates</a>
                    <a href="#">Resume Examples</a>
                    <a href="#">Free Resources</a>
                    <a href="#">Builders</a>
                    <a href="#">Pricing</a>
                    <button className="login-btn outline">Login</button>
                </nav>
            ) : (
                <button className="login-btn">
                    <span>Login via Clerk</span>
                    <UserCircle size={20} />
                </button>
            )}
        </header>
    );
};

export default Header;
