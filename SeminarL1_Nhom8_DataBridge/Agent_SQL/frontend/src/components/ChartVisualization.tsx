'use client';

import React, { useState, useMemo } from 'react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from 'recharts';
import { ChartType } from '@/types';

interface ChartVisualizationProps {
  columns: string[];
  rows: Record<string, unknown>[];
  compact?: boolean;
  defaultType?: ChartType;
  title?: string;
}

const CHART_COLORS = ['#6c63ff', '#a855f7', '#ec4899', '#f59e0b', '#22c55e', '#06b6d4', '#8b5cf6'];

const TIME_KEYWORDS = ['date', 'time', 'month', 'year', 'day', 'week', 'quarter', 'period', 'created', 'updated'];

function detectChartType(columns: string[]): ChartType {
  const hasTimeCol = columns.some((col) =>
    TIME_KEYWORDS.some((kw) => col.toLowerCase().includes(kw))
  );
  return hasTimeCol ? 'line' : 'bar';
}

function getAxisColumns(columns: string[], rows: Record<string, unknown>[]) {
  if (columns.length < 2 || rows.length === 0) return null;

  // Find label column (first string-like column)
  let labelCol = columns[0];
  const numericCols: string[] = [];

  for (const col of columns) {
    const sample = rows[0][col];
    if (typeof sample === 'number') {
      numericCols.push(col);
    } else {
      labelCol = col;
    }
  }

  // If no numeric columns found, try to detect them
  if (numericCols.length === 0) {
    for (const col of columns) {
      if (col === labelCol) continue;
      const val = rows[0][col];
      if (val !== null && val !== undefined && !isNaN(Number(val))) {
        numericCols.push(col);
      }
    }
  }

  if (numericCols.length === 0) return null;

  return { labelCol, numericCols };
}

// Custom tooltip style matching the dark theme
const CustomTooltip = ({ active, payload, label }: { active?: boolean; payload?: Array<{ name: string; value: number; color: string }>; label?: string }) => {
  if (!active || !payload) return null;
  return (
    <div style={{
      background: '#1a1a2e',
      border: '1px solid #2a2a3e',
      borderRadius: '8px',
      padding: '10px 14px',
      fontSize: '12px',
    }}>
      <div style={{ color: '#8888a0', marginBottom: '6px' }}>{label}</div>
      {payload.map((entry, i) => (
        <div key={i} style={{ color: entry.color, marginBottom: '2px' }}>
          {entry.name}: <strong>{typeof entry.value === 'number' ? entry.value.toLocaleString() : entry.value}</strong>
        </div>
      ))}
    </div>
  );
};

export default function ChartVisualization({
  columns,
  rows,
  compact = false,
  defaultType,
  title = 'Visualization',
}: ChartVisualizationProps) {
  const autoType = useMemo(() => detectChartType(columns), [columns]);
  const [chartType, setChartType] = useState<ChartType>(defaultType || autoType);

  React.useEffect(() => {
    setChartType(defaultType || autoType);
  }, [defaultType, autoType]);

  const axisInfo = useMemo(() => getAxisColumns(columns, rows), [columns, rows]);

  if (!axisInfo || rows.length === 0) return null;

  const { labelCol, numericCols } = axisInfo;

  // Convert values to numbers for charting
  const chartData = rows.slice(0, 50).map((row) => {
    const point: Record<string, unknown> = { [labelCol]: String(row[labelCol] ?? '') };
    for (const col of numericCols) {
      point[col] = Number(row[col]) || 0;
    }
    return point;
  });

  const chartContent = (
    <>
      <div className="chart-toggles">
        <button
          className={`chart-toggle-btn ${chartType === 'line' ? 'active' : ''}`}
          onClick={() => setChartType('line')}
          type="button"
        >
          📈 Line
        </button>
        <button
          className={`chart-toggle-btn ${chartType === 'bar' ? 'active' : ''}`}
          onClick={() => setChartType('bar')}
          type="button"
        >
          📊 Bar
        </button>
      </div>

      <div className="chart-container">
        <ResponsiveContainer width="100%" height="100%">
          {chartType === 'line' ? (
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#2a2a3e" />
              <XAxis
                dataKey={labelCol}
                tick={{ fill: '#8888a0', fontSize: 11 }}
                axisLine={{ stroke: '#2a2a3e' }}
                tickLine={false}
              />
              <YAxis
                tick={{ fill: '#8888a0', fontSize: 11 }}
                axisLine={{ stroke: '#2a2a3e' }}
                tickLine={false}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend
                wrapperStyle={{ fontSize: '12px', color: '#8888a0' }}
              />
              {numericCols.map((col, i) => (
                <Line
                  key={col}
                  type="monotone"
                  dataKey={col}
                  stroke={CHART_COLORS[i % CHART_COLORS.length]}
                  strokeWidth={2}
                  dot={{ r: 4, fill: CHART_COLORS[i % CHART_COLORS.length] }}
                  activeDot={{ r: 6 }}
                />
              ))}
            </LineChart>
          ) : (
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#2a2a3e" />
              <XAxis
                dataKey={labelCol}
                tick={{ fill: '#8888a0', fontSize: 11 }}
                axisLine={{ stroke: '#2a2a3e' }}
                tickLine={false}
              />
              <YAxis
                tick={{ fill: '#8888a0', fontSize: 11 }}
                axisLine={{ stroke: '#2a2a3e' }}
                tickLine={false}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend
                wrapperStyle={{ fontSize: '12px', color: '#8888a0' }}
              />
              {numericCols.map((col, i) => (
                <Bar
                  key={col}
                  dataKey={col}
                  fill={CHART_COLORS[i % CHART_COLORS.length]}
                  radius={[4, 4, 0, 0]}
                />
              ))}
            </BarChart>
          )}
        </ResponsiveContainer>
      </div>
    </>
  );

  if (compact) {
    return <div className="chart-compact">{chartContent}</div>;
  }

  return (
    <div className="card fade-in-up stagger-5">
      <div className="card-title">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M18 20V10M12 20V4M6 20v-6" />
        </svg>
        {title}
      </div>
      {chartContent}
    </div>
  );
}
