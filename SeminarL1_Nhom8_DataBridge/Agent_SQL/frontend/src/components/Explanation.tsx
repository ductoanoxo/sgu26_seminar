'use client';

import React from 'react';

interface ExplanationProps {
  text: string;
}

export default function Explanation({ text }: ExplanationProps) {
  return (
    <div className="card explanation-card fade-in-up stagger-2">
      <div className="card-title">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="12" cy="12" r="10" />
          <path d="M12 16v-4M12 8h.01" />
        </svg>
        Explanation
      </div>
      <p className="explanation-text">{text}</p>
    </div>
  );
}
