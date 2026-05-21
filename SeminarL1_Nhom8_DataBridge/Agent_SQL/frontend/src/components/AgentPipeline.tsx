'use client';

import React, { useState } from 'react';
import { AgentStep } from '@/types';

interface AgentPipelineProps {
  steps: AgentStep[];
}

export default function AgentPipeline({ steps }: AgentPipelineProps) {
  const [expanded, setExpanded] = useState(false);

  if (!steps || steps.length === 0) return null;

  return (
    <div className="pipeline-section fade-in-up stagger-3">
      <button
        className="pipeline-toggle"
        onClick={() => setExpanded(!expanded)}
        type="button"
      >
        <svg
          width="14" height="14" viewBox="0 0 24 24" fill="none"
          stroke="currentColor" strokeWidth="2"
          style={{ transform: expanded ? 'rotate(90deg)' : 'rotate(0deg)', transition: 'transform 0.2s' }}
        >
          <polyline points="9 18 15 12 9 6" />
        </svg>
        <span>Agent Pipeline</span>
        <span style={{ marginLeft: 'auto', fontSize: '11px' }}>
          {steps.length} steps
        </span>
      </button>

      {expanded && (
        <div className="pipeline-steps">
          {steps.map((step, i) => (
            <React.Fragment key={i}>
              {i > 0 && (
                <div className="pipeline-connector">→</div>
              )}
              <div className="pipeline-step">
                <div className="pipeline-step-header">
                  <div className="pipeline-step-num">{i + 1}</div>
                  <div className="pipeline-step-name">{step.agent}</div>
                </div>
                <div className="pipeline-step-detail">
                  <strong style={{ color: 'var(--text-secondary)' }}>Input:</strong>{' '}
                  {step.input_summary}
                </div>
                <div className="pipeline-step-detail" style={{ marginTop: '6px' }}>
                  <strong style={{ color: 'var(--text-secondary)' }}>Output:</strong>{' '}
                  {step.output_summary}
                </div>
              </div>
            </React.Fragment>
          ))}
        </div>
      )}
    </div>
  );
}
