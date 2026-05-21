'use client';

import React, { useEffect, useState } from 'react';

interface SqlPreviewProps {
  sql: string;
  tables: string[];
  editable?: boolean;
  isRunning?: boolean;
  error?: string;
  onRun?: (sql: string) => void;
  onSqlChange?: (sql: string) => void;
}

const SQL_KEYWORDS = [
  'SELECT', 'FROM', 'WHERE', 'JOIN', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN',
  'ON', 'AND', 'OR', 'ORDER BY', 'GROUP BY', 'HAVING', 'LIMIT', 'AS',
  'COUNT', 'SUM', 'AVG', 'MAX', 'MIN', 'DISTINCT', 'CASE', 'WHEN', 'THEN',
  'ELSE', 'END', 'IN', 'NOT', 'NULL', 'IS', 'LIKE', 'BETWEEN', 'EXISTS',
  'UNION', 'WITH', 'DESC', 'ASC', 'OFFSET', 'COALESCE', 'CAST',
];

const FORMAT_KEYWORDS = [
  'UNION ALL', 'FULL JOIN', 'CROSS JOIN', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN',
  'GROUP BY', 'ORDER BY', 'SELECT', 'FROM', 'WHERE', 'HAVING', 'LIMIT', 'OFFSET',
  'JOIN', 'ON', 'AND', 'OR', 'UNION', 'WITH', 'DESC', 'ASC', 'DISTINCT',
  'CASE', 'WHEN', 'THEN', 'ELSE', 'END', 'IN', 'NOT', 'NULL', 'IS', 'LIKE',
  'BETWEEN', 'EXISTS', 'COUNT', 'SUM', 'AVG', 'MAX', 'MIN', 'COALESCE', 'CAST',
].sort((a, b) => b.length - a.length);

const BREAK_KEYWORDS = [
  'WITH', 'SELECT', 'FROM', 'WHERE', 'GROUP BY', 'ORDER BY', 'HAVING',
  'LIMIT', 'OFFSET', 'UNION ALL', 'UNION', 'INTERSECT', 'EXCEPT',
  'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'FULL JOIN', 'CROSS JOIN', 'JOIN',
].sort((a, b) => b.length - a.length);

function formatSqlBasic(sql: string): string {
  if (!sql.trim()) return sql;

  const parts = sql.trim().split(/('(?:''|[^'])*')/);
  const formatted = parts.map((part, index) => {
    if (index % 2 === 1) return part;

    let segment = part.replace(/\s+/g, ' ');

    for (const keyword of FORMAT_KEYWORDS) {
      const pattern = keyword.replace(/\s+/g, '\\s+');
      segment = segment.replace(new RegExp(`\\b${pattern}\\b`, 'gi'), keyword);
    }

    for (const keyword of BREAK_KEYWORDS) {
      const pattern = keyword.replace(/\s+/g, '\\s+');
      segment = segment.replace(new RegExp(`\\s+(${pattern})\\b`, 'gi'), '\n$1');
    }

    return segment;
  }).join('');

  return formatted.replace(/\n{2,}/g, '\n').trim();
}

function highlightSQL(sql: string): React.ReactNode[] {
  const parts: React.ReactNode[] = [];
  let remaining = sql;
  let key = 0;

  while (remaining.length > 0) {
    // Check for string literals
    const strMatch = remaining.match(/^'[^']*'/);
    if (strMatch) {
      parts.push(<span key={key++} className="sql-string">{strMatch[0]}</span>);
      remaining = remaining.slice(strMatch[0].length);
      continue;
    }

    // Check for numbers
    const numMatch = remaining.match(/^\b\d+(\.\d+)?\b/);
    if (numMatch) {
      parts.push(<span key={key++} className="sql-number">{numMatch[0]}</span>);
      remaining = remaining.slice(numMatch[0].length);
      continue;
    }

    // Check for keywords (case-insensitive)
    let matched = false;
    for (const kw of SQL_KEYWORDS) {
      const regex = new RegExp(`^\\b${kw}\\b`, 'i');
      const kwMatch = remaining.match(regex);
      if (kwMatch) {
        parts.push(<span key={key++} className="sql-keyword">{kwMatch[0]}</span>);
        remaining = remaining.slice(kwMatch[0].length);
        matched = true;
        break;
      }
    }
    if (matched) continue;

    // Check for aggregate functions with parens
    const funcMatch = remaining.match(/^\b(COUNT|SUM|AVG|MAX|MIN|COALESCE|CAST)\s*\(/i);
    if (funcMatch) {
      const funcName = funcMatch[0].slice(0, -1);
      parts.push(<span key={key++} className="sql-function">{funcName}</span>);
      remaining = remaining.slice(funcName.length);
      continue;
    }

    // Default: take one character
    parts.push(<span key={key++}>{remaining[0]}</span>);
    remaining = remaining.slice(1);
  }

  return parts;
}

export default function SqlPreview({
  sql,
  tables,
  editable,
  isRunning,
  error,
  onRun,
  onSqlChange,
}: SqlPreviewProps) {
  const [copied, setCopied] = useState(false);
  const [mode, setMode] = useState<'preview' | 'edit'>('preview');
  const [draft, setDraft] = useState(sql);

  useEffect(() => {
    setDraft(sql);
  }, [sql]);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(draft);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  const handleRun = () => {
    if (onRun) {
      onRun(draft.trim());
    }
  };

  const handleFormat = () => {
    const formatted = formatSqlBasic(draft);
    setDraft(formatted);
    if (onSqlChange) {
      onSqlChange(formatted);
    }
    if (mode !== 'edit') {
      setMode('edit');
    }
  };

  const handleChange = (value: string) => {
    setDraft(value);
    if (onSqlChange) {
      onSqlChange(value);
    }
  };

  const isEditable = Boolean(editable && onRun);

  return (
    <div className="card fade-in-up stagger-1">
      <div className="card-title">
        SQL Query
      </div>
      <div className="sql-actions">
        <button className="copy-btn" onClick={handleCopy} type="button">
          {copied ? 'Copied' : 'Copy'}
        </button>
        {isEditable && (
          <>
            <button
              className="sql-toggle-btn"
              onClick={() => setMode(mode === 'preview' ? 'edit' : 'preview')}
              type="button"
            >
              {mode === 'preview' ? 'Edit' : 'Preview'}
            </button>
            <button
              className="sql-toggle-btn"
              onClick={handleFormat}
              type="button"
              disabled={!draft.trim()}
            >
              Format
            </button>
            <button
              className="sql-run-btn"
              onClick={handleRun}
              type="button"
              disabled={isRunning || !draft.trim()}
            >
              {isRunning ? 'Running...' : 'Run SQL'}
            </button>
          </>
        )}
      </div>
      {mode === 'edit' && isEditable ? (
        <textarea
          className="sql-editor"
          value={draft}
          onChange={(e) => handleChange(e.target.value)}
          spellCheck={false}
          rows={8}
        />
      ) : (
        <div className="sql-code">
          {highlightSQL(draft)}
        </div>
      )}
      {isEditable && (
        <div className="sql-note">Read-only: SELECT/CTE only</div>
      )}
      {error && <div className="sql-error">{error}</div>}
      {tables.length > 0 && (
        <div className="table-tags">
          {tables.map((t) => (
            <span key={t} className="table-tag">{t}</span>
          ))}
        </div>
      )}
    </div>
  );
}
