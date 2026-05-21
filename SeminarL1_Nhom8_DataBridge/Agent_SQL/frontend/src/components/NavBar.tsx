import React from 'react';

interface NavBarProps {
  onConnectClick?: () => void;
}

export default function NavBar({ onConnectClick }: NavBarProps) {
  return (
    <nav className="hero-nav">
      <div className="hero-nav-container">
        {/* Logo */}
        <div className="hero-logo">
          Logoipsum
        </div>

        {/* Menu Items */}
        <ul className="hero-menu">
          <li><a href="#platform">Platform</a></li>
          <li>
            <a href="#features" className="hero-menu-item-with-icon">
              Features
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="hero-chevron">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </a>
          </li>
          <li><a href="#projects">Projects</a></li>
          <li><a href="#community">Community</a></li>
          <li><a href="#contact">Contact</a></li>
        </ul>

        {/* Right side buttons */}
        <div className="hero-auth-buttons">
          <button className="hero-btn-signup">Sign Up</button>
          <button className="hero-btn-login">Log In</button>
        </div>
      </div>
    </nav>
  );
}
