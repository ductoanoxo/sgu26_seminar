'use client';

import React from 'react';

interface DataTableProps {
  columns: string[];
  rows: Record<string, unknown>[];
  rowCount: number;
  truncated?: boolean;
}

export default function DataTable({ columns, rows, rowCount, truncated = false }: DataTableProps) {
  if (!columns.length || !rows.length) return null;

  const displayRows = rows.slice(0, 100);

  return (
    <div className="card fade-in-up stagger-4">
      <div className="card-title">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <rect x="3" y="3" width="18" height="18" rx="2" />
          <path d="M3 9h18M3 15h18M9 3v18M15 3v18" />
        </svg>
        Results
      </div>
      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              <th>#</th>
              {columns.map((col) => (
                <th key={col}>{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {displayRows.map((row, i) => (
              <tr key={i}>
                <td style={{ color: 'var(--text-muted)' }}>{i + 1}</td>
                {columns.map((col) => (
                  <td key={col}>{formatCell(row[col])}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="table-footer">
        Showing {displayRows.length} of {rowCount} rows{truncated ? ' (limited)' : ''}
      </div>
    </div>
  );
}

function formatCell(value: unknown): string {
  if (value === null || value === undefined) return '—';
  if (typeof value === 'number') {
    // Format numbers with appropriate precision
    if (Number.isInteger(value)) return value.toLocaleString();
    return value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }
  return String(value);
}
