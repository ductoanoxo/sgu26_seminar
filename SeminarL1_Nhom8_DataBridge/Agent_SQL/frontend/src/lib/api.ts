import { AskResponse, Dashboard, DashboardRefreshResponse } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function askQuestion(question: string): Promise<AskResponse> {
  const res = await fetch(`${API_URL}/ask`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }

  return res.json();
}

export async function explainSQL(sql_query: string): Promise<{ success: boolean; explanation: string; error?: string }> {
  const res = await fetch(`${API_URL}/explain`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sql_query }),
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }

  return res.json();
}

export async function runManualQuery(payload: {
  sql_query: string;
  question?: string | null;
  sql_original?: string | null;
}): Promise<AskResponse> {
  const res = await fetch(`${API_URL}/query/manual`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }

  return res.json();
}

export async function getHistory(limit: number = 20) {
  const res = await fetch(`${API_URL}/history?limit=${limit}`);
  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

export async function createDashboard(payload: {
  name: string;
  description?: string | null;
  widgets?: Dashboard['widgets'];
}): Promise<{ success: boolean; dashboard?: Dashboard; error?: string }> {
  const res = await fetch(`${API_URL}/dashboards`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }

  return res.json();
}

export async function listDashboards(limit: number = 20): Promise<{ success: boolean; dashboards?: Dashboard[]; error?: string }> {
  const res = await fetch(`${API_URL}/dashboards?limit=${limit}`);
  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

export async function refreshDashboard(dashboardId: string, widgetIds?: string[]): Promise<DashboardRefreshResponse> {
  const res = await fetch(`${API_URL}/dashboards/${dashboardId}/refresh`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ widget_ids: widgetIds && widgetIds.length ? widgetIds : null }),
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }

  return res.json();
}

export async function getDashboard(dashboardId: string): Promise<{ success: boolean; dashboard?: Dashboard; error?: string }> {
  const res = await fetch(`${API_URL}/dashboards/${dashboardId}`);
  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

export async function updateDashboard(dashboardId: string, payload: {
  name?: string | null;
  description?: string | null;
  widgets?: Dashboard['widgets'];
}): Promise<{ success: boolean; dashboard?: Dashboard; error?: string }> {
  const res = await fetch(`${API_URL}/dashboards/${dashboardId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }

  return res.json();
}
