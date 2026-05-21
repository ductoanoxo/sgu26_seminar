'use client';

import React, { useState, FormEvent } from 'react';

interface HeroSearchInputProps {
  onSubmit: (query: string) => void;
  isLoading?: boolean;
  onConnectClick?: () => void;
}

export default function HeroSearchInput({ onSubmit, isLoading = false, onConnectClick }: HeroSearchInputProps) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (query.trim() && !isLoading) {
      onSubmit(query.trim());
    }
  };

  return (
    <div className="hero-search-box">
      {/* Top row: Credit info & powered by */}
      <div className="hero-search-top">
        <div className="hero-credits">
          <span>60/450 credits</span>
          <button className="hero-btn-upgrade">Upgrade</button>
        </div>
        <div className="hero-powered-by">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"></path>
          </svg>
          <span>Powered by GPT-4o</span>
        </div>
      </div>

      {/* Main input area */}
      <form onSubmit={handleSubmit} className="hero-search-main">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Type question..."
          className="hero-input-field"
          disabled={isLoading}
          maxLength={3000}
        />
        <button type="submit" className="hero-btn-submit" disabled={isLoading || !query.trim()}>
          {isLoading ? (
            <div className="hero-spinner"></div>
          ) : (
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <line x1="12" y1="19" x2="12" y2="5"></line>
              <polyline points="5 12 12 5 19 12"></polyline>
            </svg>
          )}
        </button>
      </form>

      {/* Bottom row: actions & counter */}
      <div className="hero-search-bottom">
        <div className="hero-search-actions">
          <button type="button" className="hero-action-btn" onClick={onConnectClick}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <rect x="2" y="2" width="20" height="8" rx="2" ry="2"></rect>
              <rect x="2" y="14" width="20" height="8" rx="2" ry="2"></rect>
              <line x1="6" y1="6" x2="6.01" y2="6"></line>
              <line x1="6" y1="18" x2="6.01" y2="18"></line>
            </svg>
            Connect Data
          </button>
          <button type="button" className="hero-action-btn">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"></path>
            </svg>
            Attach
          </button>
          <button type="button" className="hero-action-btn">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
              <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
              <line x1="12" y1="19" x2="12" y2="23"></line>
              <line x1="8" y1="23" x2="16" y2="23"></line>
            </svg>
            Voice
          </button>
          <button type="button" className="hero-action-btn">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            Prompts
          </button>
        </div>
        <div className="hero-char-counter">
          {query.length}/3,000
        </div>
      </div>
    </div>
  );
}
