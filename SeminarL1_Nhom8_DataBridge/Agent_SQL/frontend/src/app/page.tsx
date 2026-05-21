'use client';

import React, { useState, useCallback, useEffect, useRef } from 'react';
import VideoBackground from '@/components/VideoBackground';
import NavBar from '@/components/NavBar';
import HeroSearchInput from '@/components/HeroSearchInput';
import SqlPreview from '@/components/SqlPreview';
import Explanation from '@/components/Explanation';
import AgentPipeline from '@/components/AgentPipeline';
import DataTable from '@/components/DataTable';
import ChartVisualization from '@/components/ChartVisualization';
import LoadingSkeleton from '@/components/LoadingSkeleton';
import DashboardPanel from '@/components/DashboardPanel';
import { askQuestion, runManualQuery, createDashboard, listDashboards, updateDashboard, refreshDashboard } from '@/lib/api';
import { AskResponse, Dashboard, DashboardWidget, WidgetRefreshResult } from '@/types';

type AppState = 'idle' | 'loading' | 'success' | 'error';

function diffColumns(base: string[], compare: string[]) {
  const baseSet = new Set(base);
  const compareSet = new Set(compare);
  const added = compare.filter((col) => !baseSet.has(col));
  const removed = base.filter((col) => !compareSet.has(col));
  return { added, removed };
}

function formatColumnList(columns: string[], max: number = 6): string {
  if (columns.length <= max) return columns.join(', ');
  return `${columns.slice(0, max).join(', ')} +${columns.length - max} more`;
}

export default function HomePage() {
  const [state, setState] = useState<AppState>('idle');
  const [result, setResult] = useState<AskResponse | null>(null);
  const [manualResult, setManualResult] = useState<AskResponse | null>(null);
  const [manualSql, setManualSql] = useState<string>('');
  const [manualError, setManualError] = useState<string>('');
  const [manualRunning, setManualRunning] = useState<boolean>(false);
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [dashboardLoading, setDashboardLoading] = useState<boolean>(false);
  const [dashboardError, setDashboardError] = useState<string>('');
  const [widgetData, setWidgetData] = useState<Record<string, AskResponse | null>>({});
  const [widgetLoading, setWidgetLoading] = useState<Record<string, boolean>>({});
  const [widgetError, setWidgetError] = useState<Record<string, string>>({});
  const [error, setError] = useState<string>('');
  const [apiOnline, setApiOnline] = useState<boolean | null>(null);
  const [lastQuestion, setLastQuestion] = useState<string>('');
  const [showImport, setShowImport] = useState<boolean>(false);
  const resultsRef = useRef<HTMLDivElement>(null);

  // Check API health on mount
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/`
        );
        setApiOnline(res.ok);
      } catch {
        setApiOnline(false);
      }
    };
    checkHealth();
  }, []);

  useEffect(() => {
    const loadDashboards = async () => {
      try {
        const data = await listDashboards(1);
        if (data.success && data.dashboards && data.dashboards.length > 0) {
          setDashboard(data.dashboards[0]);
        }
      } catch (err) {
        setDashboardError(err instanceof Error ? err.message : 'Failed to load dashboards');
      }
    };
    loadDashboards();
  }, []);

  const buildWidget = useCallback((sqlSource: string, title: string) => ({
    id: crypto.randomUUID(),
    title: title || 'Saved Query',
    sql_source: sqlSource,
    chart_type: 'auto',
  }), []);

  const persistDashboard = useCallback(async (widgets: DashboardWidget[]) => {
    setDashboardLoading(true);
    setDashboardError('');
    try {
      if (dashboard) {
        const updated = await updateDashboard(dashboard.id, { widgets });
        if (updated.success && updated.dashboard) {
          setDashboard(updated.dashboard);
          return updated.dashboard;
        }
        setDashboardError(updated.error || 'Failed to update dashboard');
        return null;
      }

      const created = await createDashboard({
        name: 'My Dashboard',
        widgets,
      });
      if (created.success && created.dashboard) {
        setDashboard(created.dashboard);
        return created.dashboard;
      }
      setDashboardError(created.error || 'Failed to create dashboard');
      return null;
    } catch (err) {
      setDashboardError(err instanceof Error ? err.message : 'Failed to save dashboard');
      return null;
    } finally {
      setDashboardLoading(false);
    }
  }, [dashboard]);

  const handleAutoSaveToDashboard = useCallback(async (data: AskResponse, question: string) => {
    if (!data?.success) return;
    const sqlSource = data.sql_query?.trim();
    if (!sqlSource) return;

    const existingWidgets = dashboard?.widgets || [];
    const duplicate = existingWidgets.some((widget) => widget.sql_source.trim() === sqlSource);
    if (duplicate) return;

    const widget = buildWidget(sqlSource, question || 'Saved Query');
    const saved = await persistDashboard([...existingWidgets, widget]);
    if (saved) {
      setWidgetData((prev) => ({ ...prev, [widget.id]: data }));
    }
  }, [buildWidget, dashboard, persistDashboard]);

  const handleSubmit = useCallback(async (query: string) => {
    setState('loading');
    setError('');
    setResult(null);
    setManualResult(null);
    setManualError('');
    setManualSql('');
    setLastQuestion(query);

    // Scroll to results section smoothly
    setTimeout(() => {
      if (resultsRef.current) {
        resultsRef.current.scrollIntoView({ behavior: 'smooth' });
      }
    }, 100);

    try {
      const data = await askQuestion(query);
      if (data.success) {
        setResult(data);
        setManualSql(data.sql_query);
        setState('success');
        void handleAutoSaveToDashboard(data, query);
      } else {
        setError(data.error || 'An unknown error occurred');
        setResult(data);
        setState('error');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to connect to the API');
      setState('error');
    }
  }, [handleAutoSaveToDashboard]);

  const handleManualRun = useCallback(async (sql: string) => {
    if (!sql.trim()) return;
    setManualRunning(true);
    setManualError('');

    try {
      const data = await runManualQuery({
        sql_query: sql,
        question: lastQuestion,
        sql_original: result?.sql_query || null,
      });
      if (data.success) {
        setManualResult({
          ...data,
          explanation: data.explanation || result?.explanation || '',
        });
      } else {
        setManualResult(null);
        setManualError(data.error || 'Manual SQL execution failed');
      }
    } catch (err) {
      setManualResult(null);
      setManualError(err instanceof Error ? err.message : 'Manual SQL execution failed');
    } finally {
      setManualRunning(false);
    }
  }, [lastQuestion, result]);

  const mapWidgetResult = useCallback((resultData: WidgetRefreshResult) => ({
    success: resultData.success,
    sql_query: '',
    explanation: '',
    data: {
      columns: resultData.data?.columns || [],
      rows: resultData.data?.rows || [],
      row_count: resultData.data?.row_count || 0,
    },
    metadata: resultData.metadata || {},
    error: resultData.error || null,
  }), []);

  const refreshWidget = useCallback(async (widget: DashboardWidget) => {
    if (!dashboard) return;
    setWidgetLoading((prev) => ({ ...prev, [widget.id]: true }));
    setWidgetError((prev) => ({ ...prev, [widget.id]: '' }));
    try {
      const response = await refreshDashboard(dashboard.id, [widget.id]);
      if (!response.success || !response.results) {
        setWidgetError((prev) => ({ ...prev, [widget.id]: response.error || 'Widget refresh failed' }));
        return;
      }
      const resultItem = response.results.find((item) => item.widget_id === widget.id);
      if (!resultItem) {
        setWidgetError((prev) => ({ ...prev, [widget.id]: 'Widget refresh failed' }));
        return;
      }
      if (resultItem.success) {
        setWidgetData((prev) => ({ ...prev, [widget.id]: mapWidgetResult(resultItem) }));
      } else {
        setWidgetError((prev) => ({ ...prev, [widget.id]: resultItem.error || 'Widget refresh failed' }));
      }
    } catch (err) {
      setWidgetError((prev) => ({ ...prev, [widget.id]: err instanceof Error ? err.message : 'Widget refresh failed' }));
    } finally {
      setWidgetLoading((prev) => ({ ...prev, [widget.id]: false }));
    }
  }, [dashboard, mapWidgetResult]);

  const handleRefreshAll = useCallback(async () => {
    if (!dashboard) return;
    setDashboardError('');
    const nextLoading = dashboard.widgets.reduce((acc, widget) => {
      acc[widget.id] = true;
      return acc;
    }, {} as Record<string, boolean>);
    setWidgetLoading((prev) => ({ ...prev, ...nextLoading }));
    setWidgetError((prev) => ({
      ...prev, ...Object.keys(nextLoading).reduce((acc, key) => {
        acc[key] = '';
        return acc;
      }, {} as Record<string, string>)
    }));

    try {
      const response = await refreshDashboard(dashboard.id);
      if (!response.success || !response.results) {
        setDashboardError(response.error || 'Dashboard refresh failed');
        return;
      }
      response.results.forEach((resultItem) => {
        if (resultItem.success) {
          setWidgetData((prev) => ({ ...prev, [resultItem.widget_id]: mapWidgetResult(resultItem) }));
          setWidgetError((prev) => ({ ...prev, [resultItem.widget_id]: '' }));
        } else {
          setWidgetError((prev) => ({ ...prev, [resultItem.widget_id]: resultItem.error || 'Widget refresh failed' }));
        }
      });
    } catch (err) {
      setDashboardError(err instanceof Error ? err.message : 'Dashboard refresh failed');
    } finally {
      setWidgetLoading((prev) => ({
        ...prev,
        ...dashboard.widgets.reduce((acc, widget) => {
          acc[widget.id] = false;
          return acc;
        }, {} as Record<string, boolean>),
      }));
    }
  }, [dashboard, mapWidgetResult]);

  const handleUpdateWidget = useCallback(async (widgetId: string, updates: Partial<DashboardWidget>) => {
    if (!dashboard) return;
    const widgets = dashboard.widgets.map((widget) => (
      widget.id === widgetId ? { ...widget, ...updates } : widget
    ));
    setDashboardLoading(true);
    setDashboardError('');
    try {
      const updated = await updateDashboard(dashboard.id, { widgets });
      if (updated.success && updated.dashboard) {
        setDashboard(updated.dashboard);
      } else {
        setDashboardError(updated.error || 'Failed to update widget');
      }
    } catch (err) {
      setDashboardError(err instanceof Error ? err.message : 'Failed to update widget');
    } finally {
      setDashboardLoading(false);
    }
  }, [dashboard]);

  const handleRemoveWidget = useCallback(async (widgetId: string) => {
    if (!dashboard) return;
    const widgets = dashboard.widgets.filter((widget) => widget.id !== widgetId);
    setDashboardLoading(true);
    setDashboardError('');
    try {
      const updated = await updateDashboard(dashboard.id, { widgets });
      if (updated.success && updated.dashboard) {
        setDashboard(updated.dashboard);
        setWidgetData((prev) => ({ ...prev, [widgetId]: null }));
      } else {
        setDashboardError(updated.error || 'Failed to remove widget');
      }
    } catch (err) {
      setDashboardError(err instanceof Error ? err.message : 'Failed to remove widget');
    } finally {
      setDashboardLoading(false);
    }
  }, [dashboard]);

  const handleMoveWidget = useCallback(async (widgetId: string, direction: 'up' | 'down') => {
    if (!dashboard) return;
    const index = dashboard.widgets.findIndex((widget) => widget.id === widgetId);
    if (index < 0) return;
    const nextIndex = direction === 'up' ? index - 1 : index + 1;
    if (nextIndex < 0 || nextIndex >= dashboard.widgets.length) return;

    const widgets = [...dashboard.widgets];
    const [moved] = widgets.splice(index, 1);
    widgets.splice(nextIndex, 0, moved);

    setDashboardLoading(true);
    setDashboardError('');
    try {
      const updated = await updateDashboard(dashboard.id, { widgets });
      if (updated.success && updated.dashboard) {
        setDashboard(updated.dashboard);
      } else {
        setDashboardError(updated.error || 'Failed to reorder widgets');
      }
    } catch (err) {
      setDashboardError(err instanceof Error ? err.message : 'Failed to reorder widgets');
    } finally {
      setDashboardLoading(false);
    }
  }, [dashboard]);

  const handleSaveToDashboard = useCallback(async () => {
    if (!result) return;

    const sqlSource = manualSql.trim() || result.sql_query;
    if (!sqlSource) return;

    const widget = buildWidget(sqlSource, lastQuestion || 'Saved Query');
    const widgets = [...(dashboard?.widgets || []), widget];
    const saved = await persistDashboard(widgets);
    if (saved) {
      const dataToStore = manualResult?.success ? manualResult : result;
      if (dataToStore?.success) {
        setWidgetData((prev) => ({ ...prev, [widget.id]: dataToStore }));
      }
    }
  }, [buildWidget, dashboard, lastQuestion, manualResult, manualSql, persistDashboard, result]);

  const activeResult = manualResult || result;
  const showComparison = Boolean(manualResult && result);
  const columnDiff = showComparison
    ? diffColumns(result?.data?.columns || [], manualResult?.data?.columns || [])
    : null;
  const rowDelta = showComparison
    ? (manualResult?.data?.row_count ?? 0) - (result?.data?.row_count ?? 0)
    : 0;
  const rowDeltaLabel = rowDelta === 0 ? 'Row delta: 0' : `Row delta: ${rowDelta > 0 ? '+' : ''}${rowDelta}`;

  return (
    <main className="hero-section">
      <VideoBackground />

      <div className="hero-content-wrapper">
        <NavBar />

        {showImport && <DataImport onClose={() => setShowImport(false)} />}
        <div className="hero-main-content">
          <div className="hero-badge">
            <span className="hero-badge-dark">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"></path>
              </svg>
              New
            </span>
            <span className="hero-badge-text">Discover what's possible</span>
          </div>

          <h1 className="hero-headline">Transform Data Quickly</h1>

          <p className="hero-subtitle">
            Upload your information and get powerful insights right away. Work smarter and achieve goals effortlessly.
          </p>

          <HeroSearchInput
            onSubmit={handleSubmit}
            isLoading={state === 'loading'}
            onConnectClick={() => setShowImport(true)}
          />
        </div>

        {/* Results Container below Hero */}
        {(state !== 'idle') && (
          <div ref={resultsRef} className="hero-results-container fade-in-up mt-8">
            {state === 'loading' && <LoadingSkeleton />}

            {state === 'error' && (
              <div className="card error-card fade-in-up" style={{ animation: 'shake 0.4s ease-out' }}>
                <div className="card-title" style={{ color: 'var(--accent-error)' }}>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="10" />
                    <path d="M15 9l-6 6M9 9l6 6" />
                  </svg>
                  Error
                </div>
                <p className="error-message">{error}</p>
                <button className="retry-btn" onClick={() => setState('idle')} type="button">
                  ← Try Again
                </button>
              </div>
            )}

            {state === 'success' && result && (
              <div className="results-section">
                {/* SQL + Explanation side by side */}
                <div className="two-col">
                  <SqlPreview
                    sql={manualSql || result.sql_query}
                    tables={result.metadata?.selected_tables || []}
                    editable
                    isRunning={manualRunning}
                    error={manualError}
                    onRun={handleManualRun}
                    onSqlChange={setManualSql}
                  />
                  <Explanation text={result.explanation} />
                </div>

                {/* Agent Pipeline */}
                <AgentPipeline steps={result.metadata?.intermediate_steps || []} />

                <div className="dashboard-actions">
                  <button
                    className="dashboard-btn primary"
                    type="button"
                    onClick={handleSaveToDashboard}
                    disabled={dashboardLoading || !result?.sql_query}
                  >
                    {dashboardLoading ? 'Saving...' : 'Save to Dashboard'}
                  </button>
                </div>
                {dashboardError && <div className="sql-error">{dashboardError}</div>}

                {/* Data Table */}
                {showComparison && (
                  <div className="card fade-in-up">
                    <div className="card-title">Result Comparison</div>
                    <div className="comparison-grid">
                      <div>
                        <div className="comparison-label">AI Result</div>
                        <div className="comparison-value">
                          {result?.data?.row_count ?? 0} rows
                        </div>
                        <div className="comparison-sub">
                          {result?.metadata?.duration_ms ?? 0} ms
                        </div>
                      </div>
                      <div>
                        <div className="comparison-label">Manual Result</div>
                        <div className="comparison-value">
                          {manualResult?.data?.row_count ?? 0} rows
                        </div>
                        <div className="comparison-sub">
                          {manualResult?.metadata?.duration_ms ?? 0} ms
                        </div>
                        <div className="comparison-sub">
                          {rowDeltaLabel}
                        </div>
                      </div>
                    </div>
                    {columnDiff && (
                      <div className="comparison-diff">
                        {columnDiff.added.length === 0 && columnDiff.removed.length === 0 ? (
                          <div className="comparison-sub">Columns: match</div>
                        ) : (
                          <>
                            {columnDiff.added.length > 0 && (
                              <div className="comparison-sub">
                                Columns added: {formatColumnList(columnDiff.added)}
                              </div>
                            )}
                            {columnDiff.removed.length > 0 && (
                              <div className="comparison-sub">
                                Columns removed: {formatColumnList(columnDiff.removed)}
                              </div>
                            )}
                          </>
                        )}
                      </div>
                    )}
                  </div>
                )}

                {activeResult?.data && activeResult.data.rows && activeResult.data.rows.length > 0 && (
                  <DataTable
                    columns={activeResult.data.columns}
                    rows={activeResult.data.rows}
                    rowCount={activeResult.data.row_count}
                    truncated={Boolean(activeResult.metadata?.truncated)}
                  />
                )}

                {/* Chart */}
                {activeResult?.data && activeResult.data.rows && activeResult.data.rows.length > 0 && (
                  <ChartVisualization
                    columns={activeResult.data.columns}
                    rows={activeResult.data.rows}
                  />
                )}

                {dashboard && (
                  <DashboardPanel
                    dashboard={dashboard}
                    widgetData={widgetData}
                    widgetLoading={widgetLoading}
                    widgetError={widgetError}
                    onRefreshWidget={refreshWidget}
                    onRefreshAll={handleRefreshAll}
                    onUpdateWidget={handleUpdateWidget}
                    onRemoveWidget={handleRemoveWidget}
                    onMoveWidget={handleMoveWidget}
                  />
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  );
}
