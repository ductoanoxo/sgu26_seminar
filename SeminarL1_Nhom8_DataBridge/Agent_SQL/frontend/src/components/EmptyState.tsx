'use client';

import React from 'react';

interface EmptyStateProps {
  onSuggestionClick: (query: string) => void;
}

const SUGGESTIONS = [
  { text: 'Show all users and their order counts', icon: '👥' },
  { text: 'Total revenue per month in 2024', icon: '📈' },
  { text: 'Top 5 best-selling products by quantity', icon: '🏆' },
  { text: 'Average order value by country', icon: '🌍' },
];

export default function EmptyState({ onSuggestionClick }: EmptyStateProps) {
  return (
    <div className="empty-state fade-in-up">
      <div className="empty-icon">✨</div>
      <h2 className="empty-title">Ask anything about your data</h2>
      <p className="empty-subtitle">
        Type a question in natural language and get instant SQL results with visualizations
      </p>
      <div className="empty-suggestions">
        {SUGGESTIONS.map((s) => (
          <button
            key={s.text}
            className="suggestion-card"
            onClick={() => onSuggestionClick(s.text)}
            type="button"
          >
            <span style={{ marginRight: '8px' }}>{s.icon}</span>
            {s.text}
          </button>
        ))}
      </div>
    </div>
  );
}
