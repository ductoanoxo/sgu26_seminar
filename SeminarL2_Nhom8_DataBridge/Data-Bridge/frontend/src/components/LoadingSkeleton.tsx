'use client';

import React from 'react';

export default function LoadingSkeleton() {
  return (
    <div className="results-section">
      <div className="two-col">
        <div className="card">
          <div className="card-title">
            <div className="skeleton skeleton-text" style={{ width: '100px' }} />
          </div>
          <div className="skeleton skeleton-block" />
        </div>
        <div className="card">
          <div className="card-title">
            <div className="skeleton skeleton-text" style={{ width: '120px' }} />
          </div>
          <div className="skeleton skeleton-text w-full" />
          <div className="skeleton skeleton-text w-75" />
          <div className="skeleton skeleton-text w-50" />
        </div>
      </div>
      <div className="card">
        <div className="card-title">
          <div className="skeleton skeleton-text" style={{ width: '80px' }} />
        </div>
        <div className="skeleton skeleton-block" />
      </div>
      <div className="card">
        <div className="card-title">
          <div className="skeleton skeleton-text" style={{ width: '110px' }} />
        </div>
        <div className="skeleton skeleton-chart" />
      </div>
    </div>
  );
}
