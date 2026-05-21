'use client';

import React from 'react';

interface ExplanationProps {
  text: string;
}

export default function Explanation({ text }: ExplanationProps) {
  return (
    <div className="card explanation-card fade-in-up stagger-2">
      <div className="card-title">
        Explanation
      </div>
      <p className="explanation-text">{text}</p>
    </div>
  );
}
