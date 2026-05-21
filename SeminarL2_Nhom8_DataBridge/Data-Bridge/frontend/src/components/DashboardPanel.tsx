'use client';

import React, { useState } from 'react';
import ChartVisualization from '@/components/ChartVisualization';
import { AskResponse, Dashboard, DashboardWidget, ChartType } from '@/types';

interface DashboardPanelProps {
  dashboard: Dashboard;
  widgetData: Record<string, AskResponse | null>;
  widgetLoading: Record<string, boolean>;
  widgetError: Record<string, string>;
  onRefreshWidget: (widget: DashboardWidget) => void;
  onRefreshAll: () => void;
  onUpdateWidget: (widgetId: string, updates: Partial<DashboardWidget>) => void;
  onRemoveWidget: (widgetId: string) => void;
  onMoveWidget: (widgetId: string, direction: 'up' | 'down') => void;
}

function toChartType(value?: string | null): ChartType | undefined {
  if (value === 'line' || value === 'bar') return value;
  return undefined;
}

export default function DashboardPanel({
  dashboard,
  widgetData,
  widgetLoading,
  widgetError,
  onRefreshWidget,
  onRefreshAll,
  onUpdateWidget,
  onRemoveWidget,
  onMoveWidget,
}: DashboardPanelProps) {
  const [editingWidgetId, setEditingWidgetId] = useState<string | null>(null);
  const [draftTitle, setDraftTitle] = useState('');
  const [draftChartType, setDraftChartType] = useState<ChartType | 'auto'>('auto');

  const startEditing = (widget: DashboardWidget) => {
    setEditingWidgetId(widget.id);
    setDraftTitle(widget.title);
    if (widget.chart_type === 'line' || widget.chart_type === 'bar') {
      setDraftChartType(widget.chart_type);
    } else {
      setDraftChartType('auto');
    }
  };

  const cancelEditing = () => {
    setEditingWidgetId(null);
  };

  const saveEditing = (widget: DashboardWidget) => {
    const nextTitle = draftTitle.trim() || widget.title;
    onUpdateWidget(widget.id, { title: nextTitle, chart_type: draftChartType });
    setEditingWidgetId(null);
  };

  return (
    <div className="dashboard-section">
      <div className="dashboard-header">
        <div>
          <div className="dashboard-title">{dashboard.name}</div>
          <div className="widget-meta">{dashboard.widgets.length} widgets</div>
        </div>
        <div className="dashboard-actions">
          <button className="dashboard-btn" type="button" onClick={onRefreshAll}>
            Refresh All
          </button>
        </div>
      </div>

      <div className="dashboard-grid">
        {dashboard.widgets.map((widget, index) => {
          const data = widgetData[widget.id];
          const isLoading = widgetLoading[widget.id];
          const error = widgetError[widget.id];
          const rows = data?.data?.rows || [];
          const columns = data?.data?.columns || [];
          const rowCount = data?.data?.row_count || 0;
          const isEditing = editingWidgetId === widget.id;
          const isFirst = index === 0;
          const isLast = index === dashboard.widgets.length - 1;

          return (
            <div key={widget.id} className="widget-card">
              <div className="widget-header">
                <div>
                  <div className="widget-title">{widget.title}</div>
                  <div className="widget-meta">
                    {rowCount} rows · {data?.metadata?.duration_ms ?? 0} ms
                  </div>
                </div>
                <div className="widget-actions">
                  <button
                    className="dashboard-btn"
                    type="button"
                    onClick={() => onMoveWidget(widget.id, 'up')}
                    disabled={isFirst}
                  >
                    Move up
                  </button>
                  <button
                    className="dashboard-btn"
                    type="button"
                    onClick={() => onMoveWidget(widget.id, 'down')}
                    disabled={isLast}
                  >
                    Move down
                  </button>
                  <button
                    className="dashboard-btn"
                    type="button"
                    onClick={() => onRefreshWidget(widget)}
                    disabled={isLoading}
                  >
                    {isLoading ? 'Refreshing...' : 'Refresh'}
                  </button>
                </div>
              </div>

              <div className="widget-action-row">
                <button
                  className="dashboard-btn"
                  type="button"
                  onClick={() => (isEditing ? cancelEditing() : startEditing(widget))}
                >
                  {isEditing ? 'Cancel' : 'Edit'}
                </button>
                <button
                  className="dashboard-btn"
                  type="button"
                  onClick={() => onRemoveWidget(widget.id)}
                >
                  Remove
                </button>
                {isEditing && (
                  <button
                    className="dashboard-btn primary"
                    type="button"
                    onClick={() => saveEditing(widget)}
                  >
                    Save
                  </button>
                )}
              </div>

              {isEditing && (
                <div className="widget-editor">
                  <label className="widget-label" htmlFor={`widget-title-${widget.id}`}>
                    Title
                  </label>
                  <input
                    id={`widget-title-${widget.id}`}
                    className="widget-input"
                    value={draftTitle}
                    onChange={(event) => setDraftTitle(event.target.value)}
                  />
                  <label className="widget-label" htmlFor={`widget-chart-${widget.id}`}>
                    Chart type
                  </label>
                  <select
                    id={`widget-chart-${widget.id}`}
                    className="widget-select"
                    value={draftChartType}
                    onChange={(event) => setDraftChartType(event.target.value as ChartType | 'auto')}
                  >
                    <option value="auto">Auto</option>
                    <option value="bar">Bar</option>
                    <option value="line">Line</option>
                  </select>
                </div>
              )}

              {error && <div className="sql-error">{error}</div>}

              {!error && rows.length > 0 ? (
                <ChartVisualization
                  columns={columns}
                  rows={rows}
                  compact
                  defaultType={toChartType(widget.chart_type)}
                  title={widget.title}
                />
              ) : (
                <div className="widget-meta">No data yet</div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
