import { AskResponse, Dashboard, DashboardRefreshResponse, SpeechModel, TranscriptionResponse } from '@/types';
import { createClient } from '@/lib/supabase';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

async function getAuthHeaders(): Promise<Record<string, string>> {
  try {
    const supabase = createClient();
    const { data: { session } } = await supabase.auth.getSession();
    if (session?.access_token) {
      return { 'Content-Type': 'application/json', Authorization: `Bearer ${session.access_token}` };
    }
  } catch {
    // ignore — unauthenticated requests fall back to public user on the backend
  }
  return { 'Content-Type': 'application/json' };
}

function getSelectedConnectionId(): string | null {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('selected_connection_id');
  }
  return null;
}

export async function askQuestion(question: string, connectionId?: string): Promise<AskResponse> {
  const connId = connectionId || getSelectedConnectionId();
  const res = await fetch(`${API_URL}/ask`, {
    method: 'POST',
    headers: await getAuthHeaders(),
    body: JSON.stringify({ question, connection_id: connId }),
  });
  if (!res.ok) throw new Error(`API error: ${res.status} ${res.statusText}`);
  return res.json();
}

export async function explainSQL(sql_query: string, connectionId?: string): Promise<{ success: boolean; explanation: string; error?: string }> {
  const connId = connectionId || getSelectedConnectionId();
  const res = await fetch(`${API_URL}/explain`, {
    method: 'POST',
    headers: await getAuthHeaders(),
    body: JSON.stringify({ sql_query, connection_id: connId }),
  });
  if (!res.ok) throw new Error(`API error: ${res.status} ${res.statusText}`);
  return res.json();
}

export async function runManualQuery(payload: {
  sql_query: string;
  question?: string | null;
  sql_original?: string | null;
  connection_id?: string | null;
}): Promise<AskResponse> {
  const connId = payload.connection_id || getSelectedConnectionId();
  const res = await fetch(`${API_URL}/query/manual`, {
    method: 'POST',
    headers: await getAuthHeaders(),
    body: JSON.stringify({ ...payload, connection_id: connId }),
  });
  if (!res.ok) throw new Error(`API error: ${res.status} ${res.statusText}`);
  return res.json();
}

export async function getHistory(limit: number = 20) {
  const res = await fetch(`${API_URL}/history?limit=${limit}`, { headers: await getAuthHeaders() });
  if (!res.ok) throw new Error(`API error: ${res.status} ${res.statusText}`);
  return res.json();
}

// ── Connection Management ───────────────────────────────────────────────────

export interface CreateConnectionPayload {
  name: string;
  db_type: string;
  host?: string | null;
  port?: number | null;
  database_name: string;
  username?: string | null;
  password?: string | null;
  connection_string?: string | null;
}

export interface TableSchema {
  name: string;
  columns: { name: string; type: string }[];
  estimated_rows?: number | null;
}

export interface SavedConnection {
  id: string;
  name: string;
  db_type: string;
  host?: string | null;
  port?: number | null;
  database_name: string;
  username?: string | null;
  is_active: boolean;
  created_at?: string | null;
  last_used_at?: string | null;
}

export async function listConnections(): Promise<{ success: boolean; connections: any[]; error?: string }> {
  const res = await fetch(`${API_URL}/connections`, { headers: await getAuthHeaders() });
  if (!res.ok) throw new Error(`API error: ${res.status} ${res.statusText}`);
  return res.json();
}

export async function createConnection(payload: any): Promise<{ success: boolean; connection?: any; error?: string }> {
  const res = await fetch(`${API_URL}/connections`, {
    method: 'POST',
    headers: await getAuthHeaders(),
    body: JSON.stringify(payload),
  });
  return res.json();
}

export async function updateConnection(connectionId: string, payload: any): Promise<{ success: boolean; connection?: any; error?: string }> {
  const res = await fetch(`${API_URL}/connections/${connectionId}`, {
    method: 'PUT',
    headers: await getAuthHeaders(),
    body: JSON.stringify(payload),
  });
  return res.json();
}

export async function testConnection(connectionId: string): Promise<{ success: boolean; database?: string; error?: string }> {
  const res = await fetch(`${API_URL}/connections/${connectionId}/test`, {
    method: 'POST',
    headers: await getAuthHeaders(),
  });
  return res.json();
}

export async function deleteConnection(connectionId: string): Promise<{ success: boolean; error?: string }> {
  const res = await fetch(`${API_URL}/connections/${connectionId}`, {
    method: 'DELETE',
    headers: await getAuthHeaders(),
  });
  return res.json();
}

export async function activateConnection(connId: string): Promise<{ success: boolean }> {
  const res = await fetch(`${API_URL}/connections/${connId}/activate`, {
    method: 'POST',
    headers: await getAuthHeaders(),
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function getActiveConnection(): Promise<{ success: boolean; connection: SavedConnection | null }> {
  const res = await fetch(`${API_URL}/connections/active`, { headers: await getAuthHeaders() });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function shareConnection(connectionId: string, email: string, role: string = 'viewer'): Promise<{ success: boolean; error?: string }> {
  const res = await fetch(`${API_URL}/connections/${connectionId}/members`, {
    method: 'POST',
    headers: await getAuthHeaders(),
    body: JSON.stringify({ email, role }),
  });
  return res.json();
}

export async function listConnectionMembers(connectionId: string): Promise<{ success: boolean; members?: any[]; error?: string }> {
  const res = await fetch(`${API_URL}/connections/${connectionId}/members`, {
    method: 'GET',
    headers: await getAuthHeaders(),
  });
  return res.json();
}

export async function removeConnectionMember(connectionId: string, email: string): Promise<{ success: boolean; error?: string }> {
  const res = await fetch(`${API_URL}/connections/${connectionId}/members/${encodeURIComponent(email)}`, {
    method: 'DELETE',
    headers: await getAuthHeaders(),
  });
  return res.json();
}

export async function getConnectionSchema(): Promise<{
  success: boolean;
  schema?: string;
  raw_schema?: { name: string; columns: { name: string; type: string }[] }[];
  has_active?: boolean;
  connection_name?: string;
  db_type?: string;
  error?: string;
}> {
  const res = await fetch(`${API_URL}/connections/schema`, { headers: await getAuthHeaders() });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function previewTableData(tableName: string, limit: number = 10): Promise<{
  success: boolean;
  data?: { columns: string[]; rows: Record<string, any>[] };
  error?: string;
}> {
  const res = await fetch(
    `${API_URL}/connections/preview-data?table=${encodeURIComponent(tableName)}&limit=${limit}`,
    { headers: await getAuthHeaders() },
  );
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

// ── Import Registry ─────────────────────────────────────────────────────────

export interface ImportedDataset {
  source_type: string;
  source_name: string;
  destination_table: string;
  row_count: number;
  imported_at: string;
}

export async function listImportRegistry(): Promise<{ success: boolean; registry: ImportedDataset[] }> {
  const res = await fetch(`${API_URL}/import/registry`, { headers: await getAuthHeaders() });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

// ── Speech ──────────────────────────────────────────────────────────────────

export async function transcribeSpeech(file: Blob, model: SpeechModel): Promise<TranscriptionResponse> {
  const formData = new FormData();
  const extension = file.type.includes('mp4') ? 'mp4' : file.type.includes('mpeg') ? 'mp3' : 'webm';
  formData.append('file', file, `speech.${extension}`);
  formData.append('model', model);
  const res = await fetch(`${API_URL}/speech/transcribe`, { method: 'POST', body: formData });
  if (!res.ok) throw new Error(`API error: ${res.status} ${res.statusText}`);
  return res.json();
}

// ── Dashboards ──────────────────────────────────────────────────────────────

export async function createDashboard(payload: {
  name: string;
  description?: string | null;
  widgets?: Dashboard['widgets'];
}): Promise<{ success: boolean; dashboard?: Dashboard; error?: string }> {
  const res = await fetch(`${API_URL}/dashboards`, {
    method: 'POST',
    headers: await getAuthHeaders(),
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`API error: ${res.status} ${res.statusText}`);
  return res.json();
}

export async function listDashboards(limit: number = 20): Promise<{ success: boolean; dashboards?: Dashboard[]; error?: string }> {
  const res = await fetch(`${API_URL}/dashboards?limit=${limit}`, { headers: await getAuthHeaders() });
  if (!res.ok) throw new Error(`API error: ${res.status} ${res.statusText}`);
  return res.json();
}

export async function refreshDashboard(dashboardId: string, widgetIds?: string[]): Promise<DashboardRefreshResponse> {
  const res = await fetch(`${API_URL}/dashboards/${dashboardId}/refresh`, {
    method: 'POST',
    headers: await getAuthHeaders(),
    body: JSON.stringify({ widget_ids: widgetIds && widgetIds.length ? widgetIds : null }),
  });
  if (!res.ok) throw new Error(`API error: ${res.status} ${res.statusText}`);
  return res.json();
}

export async function getDashboard(dashboardId: string): Promise<{ success: boolean; dashboard?: Dashboard; error?: string }> {
  const res = await fetch(`${API_URL}/dashboards/${dashboardId}`, { headers: await getAuthHeaders() });
  if (!res.ok) throw new Error(`API error: ${res.status} ${res.statusText}`);
  return res.json();
}

export async function updateDashboard(dashboardId: string, payload: {
  name?: string | null;
  description?: string | null;
  widgets?: Dashboard['widgets'];
}): Promise<{ success: boolean; dashboard?: Dashboard; error?: string }> {
  const res = await fetch(`${API_URL}/dashboards/${dashboardId}`, {
    method: 'PUT',
    headers: await getAuthHeaders(),
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`API error: ${res.status} ${res.statusText}`);
  return res.json();
}
