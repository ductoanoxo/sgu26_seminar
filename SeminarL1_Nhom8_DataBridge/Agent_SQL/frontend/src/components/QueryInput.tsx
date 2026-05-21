'use client';

import React, { useState, FormEvent } from 'react';

interface QueryInputProps {
  onSubmit: (query: string) => void;
  isLoading: boolean;
}

const EXAMPLES = [
  'Show all users from the USA',
  'Total revenue per month',
  'Top 5 best-selling products',
  'Average order value by country',
  'Users who placed more than 2 orders',
  'Order count by status',
];

export default function QueryInput({ onSubmit, isLoading }: QueryInputProps) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (query.trim() && !isLoading) {
      onSubmit(query.trim());
    }
  };

  const handleExample = (example: string) => {
    setQuery(example);
    if (!isLoading) {
      onSubmit(example);
    }
  };

  return (
    <div className={`card query-section fade-in-up ${isLoading ? 'loading' : ''}`}>
      <div className="card-title">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="11" cy="11" r="8" />
          <path d="m21 21-4.3-4.3" />
        </svg>
        Ask a Question
      </div>
      <form className="query-form" onSubmit={handleSubmit}>
        <input
          id="query-input"
          type="text"
          className="query-input"
          placeholder="Ask anything about your data..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          disabled={isLoading}
          autoFocus
        />
        <button
          id="query-submit"
          type="submit"
          className="query-submit"
          disabled={isLoading || !query.trim()}
        >
          {isLoading ? (
            <>
              <span className="spinner" />
              Processing
            </>
          ) : (
            <>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                <path d="M5 12h14M12 5l7 7-7 7" />
              </svg>
              Ask
            </>
          )}
        </button>
      </form>
      <div className="examples">
        {EXAMPLES.map((ex) => (
          <button
            key={ex}
            className="example-pill"
            onClick={() => handleExample(ex)}
            disabled={isLoading}
            type="button"
          >
            {ex}
          </button>
        ))}
      </div>
    </div>
  );
}
