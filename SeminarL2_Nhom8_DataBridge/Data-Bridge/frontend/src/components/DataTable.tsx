'use client';

import React, { useEffect, useMemo, useState } from 'react';
import { ArrowDown, ArrowUp, Copy, Download, Search, Table as TableIcon, Layers, Columns as ColumnsIcon, Clock, Filter, List } from 'lucide-react';

interface DataTableProps {
  columns: string[];
  rows: Record<string, unknown>[];
  rowCount: number;
  truncated?: boolean;
  tableName?: string;
  dbType?: string | null;
  totalRows?: number | null;
  columnInfo?: Array<{ name: string; type: string }>;
  limit?: number;
  loadedAt?: Date | null;
  onLimitChange?: (limit: number) => void;
}

type SortState = { column: string; direction: 'asc' | 'desc' } | null;
type NullFilter = 'all' | 'only-null' | 'not-null';

export default function DataTable({
  columns,
  rows,
  rowCount,
  truncated = false,
  tableName,
  dbType,
  totalRows,
  columnInfo = [],
  limit = 50,
  loadedAt,
  onLimitChange,
}: DataTableProps) {
  const [search, setSearch] = useState('');
  const [sort, setSort] = useState<SortState>(null);
  const [filterColumn, setFilterColumn] = useState(columns[0] || '');
  const [nullFilter, setNullFilter] = useState<NullFilter>('all');

  useEffect(() => {
    if (!columns.includes(filterColumn)) {
      setFilterColumn(columns[0] || '');
    }
  }, [columns, filterColumn]);

  const typeByColumn = useMemo(
    () => new Map(columnInfo.map((column) => [column.name, column.type])),
    [columnInfo]
  );

  const stats = useMemo(() => buildColumnStats(columns, rows, typeByColumn), [columns, rows, typeByColumn]);
  const quality = useMemo(() => buildQualityInsights(stats, rows.length), [stats, rows.length]);

  const filteredRows = useMemo(() => {
    const query = search.trim().toLowerCase();
    let nextRows = rows.filter((row) => {
      const matchesSearch = !query || columns.some((column) => String(row[column] ?? '').toLowerCase().includes(query));
      const value = row[filterColumn];
      const isNullish = value === null || value === undefined || value === '';
      const matchesNullFilter =
        nullFilter === 'all' ||
        (nullFilter === 'only-null' && isNullish) ||
        (nullFilter === 'not-null' && !isNullish);
      return matchesSearch && matchesNullFilter;
    });

    if (sort) {
      nextRows = [...nextRows].sort((a, b) => compareValues(a[sort.column], b[sort.column], sort.direction));
    }

    return nextRows;
  }, [columns, filterColumn, nullFilter, rows, search, sort]);

  if (!columns.length) return null;

  const displayRows = filteredRows.slice(0, 500);
  const shownTotal = totalRows ?? rowCount;
  const duplicateRows = countDuplicateRows(rows, columns);

  const toggleSort = (column: string) => {
    setSort((current) => {
      if (!current || current.column !== column) return { column, direction: 'asc' };
      if (current.direction === 'asc') return { column, direction: 'desc' };
      return null;
    });
  };

  const exportCsv = () => {
    const csv = toCsv(columns, filteredRows);
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${tableName || 'preview'}-preview.csv`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const copyRows = async () => {
    await navigator.clipboard.writeText(toCsv(columns, filteredRows));
  };

  return (
    <div className="data-preview-shell fade-in-up stagger-4" style={{ padding: '0', background: 'transparent', border: 'none', boxShadow: 'none' }}>
      <div className="preview-header" style={{ marginBottom: '20px' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
          <div style={{ 
            fontSize: '11px', 
            fontWeight: 700, 
            textTransform: 'uppercase', 
            letterSpacing: '0.1em', 
            color: 'var(--accent-primary)',
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}>
            <TableIcon size={12} />
            Data Table Preview
          </div>
          <div style={{ fontSize: '24px', fontWeight: 800, color: 'var(--text-primary)', letterSpacing: '-0.5px' }}>
            {tableName || 'Selected table'}
          </div>
        </div>
        <div className="preview-actions">
          <button className="preview-tool-btn" onClick={copyRows} title="Copy visible rows" style={{ borderRadius: '10px', height: '38px', padding: '0 16px' }}>
            <Copy size={14} />
            Copy
          </button>
          <button className="preview-tool-btn" onClick={exportCsv} title="Export visible rows as CSV" style={{ borderRadius: '10px', height: '38px', padding: '0 16px', background: 'var(--accent-primary)', color: '#fff', border: 'none' }}>
            <Download size={14} />
            Export CSV
          </button>
        </div>
      </div>

      <div className="preview-summary-grid" style={{ gap: '16px', marginBottom: '24px' }}>
        <SummaryCard 
          icon={<List size={18} />}
          label="Total rows" 
          value={formatNumber(shownTotal)} 
          detail={totalRows === null || totalRows === undefined ? 'current sample' : 'schema estimate'} 
          color="rgba(37, 99, 235, 0.1)"
          textColor="var(--accent-primary)"
        />
        <SummaryCard 
          icon={<Layers size={18} />}
          label="Preview rows" 
          value={formatNumber(rowCount)} 
          detail={truncated ? `limit: ${limit}` : 'all loaded'} 
          color="rgba(16, 185, 129, 0.1)"
          textColor="var(--accent-success)"
        />
        <SummaryCard 
          icon={<ColumnsIcon size={18} />}
          label="Columns" 
          value={formatNumber(columns.length)} 
          detail={dbType ? dbType.toUpperCase() : 'DATABASE'} 
          color="rgba(245, 158, 11, 0.1)"
          textColor="var(--accent-warning)"
        />
        <SummaryCard 
          icon={<Clock size={18} />}
          label="Loaded at" 
          value={loadedAt ? loadedAt.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }) : '--'} 
          detail="local time" 
          color="rgba(107, 114, 128, 0.1)"
          textColor="var(--text-secondary)"
        />
      </div>

      <div className="preview-toolbar" style={{ 
        background: 'var(--bg-secondary)', 
        padding: '16px', 
        borderRadius: '16px', 
        border: '1px solid var(--border-primary)',
        boxShadow: 'var(--shadow-sm)',
        marginBottom: '20px',
        display: 'flex',
        alignItems: 'center',
        gap: '16px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flex: 1 }}>
          <div className="preview-search" style={{ 
            flex: 1, 
            height: '40px', 
            borderRadius: '12px', 
            background: 'var(--bg-tertiary)',
            border: '1px solid var(--border-primary)',
            padding: '0 12px'
          }}>
            <Search size={16} />
            <input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search in preview..." />
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <label className="preview-field" style={{ gap: '8px' }}>
            <span style={{ fontWeight: 600, color: 'var(--text-secondary)' }}>Limit</span>
            <select 
              value={limit} 
              onChange={(event) => onLimitChange?.(Number(event.target.value))}
              style={{ height: '40px', borderRadius: '10px', padding: '0 12px', background: 'var(--bg-tertiary)' }}
            >
              {[10, 50, 100, 500].map((value) => (
                <option key={value} value={value}>{value}</option>
              ))}
            </select>
          </label>
          
          <div style={{ width: '1px', height: '24px', background: 'var(--border-primary)' }} />

          <label className="preview-field" style={{ gap: '8px' }}>
            <Filter size={14} />
            <select 
              value={filterColumn} 
              onChange={(event) => setFilterColumn(event.target.value)}
              style={{ height: '40px', borderRadius: '10px', padding: '0 12px', background: 'var(--bg-tertiary)' }}
            >
              {columns.map((column) => (
                <option key={column} value={column}>{column}</option>
              ))}
            </select>
          </label>

          <select 
            value={nullFilter} 
            onChange={(event) => setNullFilter(event.target.value as NullFilter)}
            style={{ height: '40px', borderRadius: '10px', padding: '0 12px', background: 'var(--bg-tertiary)', border: '1px solid var(--border-primary)' }}
          >
            <option value="all">All Values</option>
            <option value="only-null">Only Null</option>
            <option value="not-null">Not Null</option>
          </select>
        </div>
      </div>

      <div className="table-wrapper" style={{ 
        border: '1px solid var(--border-primary)', 
        borderRadius: '16px', 
        overflow: 'hidden',
        background: 'var(--bg-secondary)',
        boxShadow: 'var(--shadow-sm)'
      }}>
        <table className="data-table">
          <thead>
            <tr>
              <th style={{ width: '50px', textAlign: 'center' }}>#</th>
              {columns.map((col) => (
                <th key={col}>
                  <button className="sortable-heading" onClick={() => toggleSort(col)}>
                    {col}
                    {sort?.column === col && (sort.direction === 'asc' ? <ArrowUp size={12} /> : <ArrowDown size={12} />)}
                  </button>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {displayRows.length ? displayRows.map((row, i) => (
              <tr key={i}>
                <td style={{ color: 'var(--text-muted)', textAlign: 'center', fontWeight: 500 }}>{i + 1}</td>
                {columns.map((col) => (
                  <td key={col} style={{ borderBottom: '1px solid var(--border-primary)' }}>
                    {formatCell(row[col])}
                  </td>
                ))}
              </tr>
            )) : (
              <tr>
                <td colSpan={columns.length + 1} style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '48px' }}>
                  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '12px' }}>
                    <Search size={32} style={{ opacity: 0.2 }} />
                    No rows match the current filters.
                  </div>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      <div className="table-footer" style={{ marginTop: '12px', padding: '0 8px' }}>
        Showing <strong>{displayRows.length}</strong> of <strong>{filteredRows.length}</strong> filtered rows · Total <strong>{rowCount}</strong> loaded
      </div>

      <div className="preview-detail-grid">
        <section className="preview-panel">
          <div className="preview-panel-title">Column Metadata</div>
          <div className="metadata-list">
            {columns.map((column) => (
              <div className="metadata-row" key={column}>
                <span className="metadata-name">{column}</span>
                <span className="metadata-type">{typeByColumn.get(column) || inferType(rows.map((row) => row[column]))}</span>
                <span className="metadata-flags">{getColumnFlags(column, stats[column])}</span>
              </div>
            ))}
          </div>
        </section>

        <section className="preview-panel">
          <div className="preview-panel-title">Quick Stats</div>
          <div className="stats-list">
            {columns.map((column) => (
              <div className="stats-row" key={column}>
                <div className="stats-name">{column}</div>
                <div className="stats-values">
                  <span>{stats[column].nullCount} null</span>
                  <span>{stats[column].uniqueCount} unique</span>
                  {stats[column].range && <span>{stats[column].range}</span>}
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="preview-panel">
          <div className="preview-panel-title">Data Quality</div>
          <div className="quality-list">
            <QualityItem label="Duplicate sample rows" value={formatNumber(duplicateRows)} tone={duplicateRows > 0 ? 'warn' : 'ok'} />
            {quality.map((item) => (
              <QualityItem key={item.label} label={item.label} value={item.value} tone={item.tone} />
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}

function SummaryCard({ label, value, detail, icon, color, textColor }: { label: string; value: string; detail: string, icon: React.ReactNode, color: string, textColor: string }) {
  return (
    <div className="preview-summary-card" style={{ 
      background: 'var(--bg-secondary)', 
      border: '1px solid var(--border-primary)', 
      borderRadius: '16px', 
      padding: '16px',
      display: 'flex',
      alignItems: 'flex-start',
      gap: '16px',
      boxShadow: 'var(--shadow-sm)'
    }}>
      <div style={{ 
        width: '40px', 
        height: '40px', 
        borderRadius: '12px', 
        background: color, 
        color: textColor, 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center',
        flexShrink: 0
      }}>
        {icon}
      </div>
      <div style={{ minWidth: 0 }}>
        <div className="preview-summary-label" style={{ fontWeight: 600, color: 'var(--text-muted)', fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{label}</div>
        <div className="preview-summary-value" style={{ fontSize: '20px', margin: '2px 0' }}>{value}</div>
        <div className="preview-summary-detail" style={{ fontSize: '11px', opacity: 0.8 }}>{detail}</div>
      </div>
    </div>
  );
}

function QualityItem({ label, value, tone }: { label: string; value: string; tone: 'ok' | 'warn' | 'info' }) {
  return (
    <div className={`quality-item ${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function formatCell(value: unknown): string {
  if (value === null || value === undefined || value === '') return '--';
  if (typeof value === 'number') {
    if (Number.isInteger(value)) return value.toLocaleString();
    return value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }
  return String(value);
}

function formatNumber(value: number): string {
  return Number.isFinite(value) ? value.toLocaleString() : '--';
}

function compareValues(a: unknown, b: unknown, direction: 'asc' | 'desc') {
  const modifier = direction === 'asc' ? 1 : -1;
  if (a === b) return 0;
  if (a === null || a === undefined || a === '') return 1;
  if (b === null || b === undefined || b === '') return -1;
  if (typeof a === 'number' && typeof b === 'number') return (a - b) * modifier;
  return String(a).localeCompare(String(b), undefined, { numeric: true }) * modifier;
}

function buildColumnStats(columns: string[], rows: Record<string, unknown>[], typeByColumn: Map<string, string>) {
  return Object.fromEntries(columns.map((column) => {
    const values = rows.map((row) => row[column]);
    const nonEmpty = values.filter((value) => value !== null && value !== undefined && value !== '');
    const uniqueValues = new Set(nonEmpty.map((value) => String(value)));
    const type = (typeByColumn.get(column) || inferType(values)).toLowerCase();
    const numericValues = nonEmpty.map(Number).filter((value) => Number.isFinite(value));
    const dateValues = nonEmpty.map((value) => new Date(String(value)).getTime()).filter((value) => Number.isFinite(value));
    let range = '';

    if ((type.includes('int') || type.includes('num') || type.includes('decimal') || type.includes('float') || type.includes('double')) && numericValues.length) {
      range = `${formatNumber(Math.min(...numericValues))} - ${formatNumber(Math.max(...numericValues))}`;
    } else if ((type.includes('date') || type.includes('time')) && dateValues.length) {
      range = `${new Date(Math.min(...dateValues)).toLocaleDateString()} - ${new Date(Math.max(...dateValues)).toLocaleDateString()}`;
    } else if (nonEmpty.length) {
      const lengths = nonEmpty.map((value) => String(value).length);
      range = `${Math.min(...lengths)}-${Math.max(...lengths)} chars`;
    }

    return [column, {
      nullCount: values.length - nonEmpty.length,
      uniqueCount: uniqueValues.size,
      range,
      type,
    }];
  })) as Record<string, { nullCount: number; uniqueCount: number; range: string; type: string }>;
}

function buildQualityInsights(stats: Record<string, { nullCount: number; uniqueCount: number; type: string }>, rowCount: number) {
  const items: Array<{ label: string; value: string; tone: 'ok' | 'warn' | 'info' }> = [];
  const columns = Object.keys(stats);
  const nullHeavy = columns.filter((column) => rowCount > 0 && stats[column].nullCount / rowCount >= 0.4);
  const idLike = columns.filter((column) => /(^id$|_id$)/i.test(column));
  const dateLike = columns.filter((column) => /date|time|created|updated/i.test(column) || stats[column].type.includes('date') || stats[column].type.includes('time'));
  const numericLike = columns.filter((column) => /amount|price|total|count|qty|quantity|score/i.test(column) || /int|num|decimal|float|double/.test(stats[column].type));

  items.push({ label: 'High-null columns', value: nullHeavy.length ? nullHeavy.join(', ') : 'None in sample', tone: nullHeavy.length ? 'warn' : 'ok' });
  items.push({ label: 'ID-like columns', value: idLike.length ? idLike.join(', ') : 'None detected', tone: 'info' });
  items.push({ label: 'Date/time-like columns', value: dateLike.length ? dateLike.join(', ') : 'None detected', tone: 'info' });
  items.push({ label: 'Numeric/measure columns', value: numericLike.length ? numericLike.join(', ') : 'None detected', tone: 'info' });

  return items;
}

function getColumnFlags(column: string, stat: { nullCount: number; uniqueCount: number }) {
  const flags = [];
  if (/^id$/i.test(column)) flags.push('PK-like');
  if (/_id$/i.test(column) && !/^id$/i.test(column)) flags.push('FK-like');
  if (stat.nullCount > 0) flags.push('nullable');
  if (stat.uniqueCount > 0) flags.push(`${stat.uniqueCount} unique`);
  return flags.join(' · ') || 'sampled';
}

function inferType(values: unknown[]) {
  const sample = values.find((value) => value !== null && value !== undefined && value !== '');
  if (sample === undefined) return 'unknown';
  if (typeof sample === 'number') return Number.isInteger(sample) ? 'integer' : 'number';
  if (typeof sample === 'boolean') return 'boolean';
  if (!Number.isNaN(Date.parse(String(sample))) && /\d{4}-\d{1,2}-\d{1,2}/.test(String(sample))) return 'datetime';
  return 'text';
}

function countDuplicateRows(rows: Record<string, unknown>[], columns: string[]) {
  const seen = new Set<string>();
  let duplicates = 0;
  rows.forEach((row) => {
    const key = JSON.stringify(columns.map((column) => row[column] ?? null));
    if (seen.has(key)) duplicates += 1;
    seen.add(key);
  });
  return duplicates;
}

function toCsv(columns: string[], rows: Record<string, unknown>[]) {
  const escape = (value: unknown) => {
    const text = value === null || value === undefined ? '' : String(value);
    return /[",\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
  };
  return [columns.join(','), ...rows.map((row) => columns.map((column) => escape(row[column])).join(','))].join('\n');
}
