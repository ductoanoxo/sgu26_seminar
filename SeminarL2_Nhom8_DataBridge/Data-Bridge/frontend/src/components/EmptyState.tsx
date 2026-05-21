'use client';

import React from 'react';

interface EmptyStateProps {
  onSuggestionClick: (query: string) => void;
}

const SUGGESTIONS = [
  { text: 'Show all users and their order counts' },
  { text: 'Total revenue per month in 2024' },
  { text: 'Top 5 best-selling products by quantity' },
  { text: 'Average order value by country' },
];

export default function EmptyState({ onSuggestionClick }: EmptyStateProps) {
  return (
    <div className="empty-state fade-in-up">
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
            {s.text}
          </button>
        ))}
      </div>
    </div>
  );
}
