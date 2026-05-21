export interface AgentStep {
  agent: string;
  input_summary: string;
  output_summary: string;
  raw_output?: Record<string, unknown> | string | null;
}

export interface AskResponse {
  success: boolean;
  sql_query: string;
  explanation: string;
  data: {
    columns: string[];
    rows: Record<string, unknown>[];
    row_count: number;
  };
  metadata: {
    selected_tables?: string[];
    intermediate_steps?: AgentStep[];
    timestamp?: string;
    duration_ms?: number;
    truncated?: boolean;
    source?: 'ai' | 'manual';
    sql_original?: string | null;
  };
  error?: string | null;
}

export interface HistoryEntry {
  id: number;
  timestamp: string;
  question: string;
  sql_query: string;
  explanation: string;
  success: boolean;
  row_count: number;
}

export type ChartType = 'line' | 'bar';

export interface DashboardWidget {
  id: string;
  title: string;
  sql_source: string;
  chart_type?: ChartType | 'auto' | null;
  fields?: Record<string, unknown> | null;
  filters?: Record<string, unknown> | null;
}

export interface Dashboard {
  id: string;
  name: string;
  owner_id: string;
  description?: string | null;
  widgets: DashboardWidget[];
  created_at?: string | null;
  updated_at?: string | null;
}

export interface WidgetRefreshResult {
  widget_id: string;
  success: boolean;
  data: {
    columns: string[];
    rows: Record<string, unknown>[];
    row_count: number;
  };
  metadata: {
    duration_ms?: number;
    truncated?: boolean;
    timestamp?: string;
  };
  error?: string | null;
}

export interface DashboardRefreshResponse {
  success: boolean;
  results: WidgetRefreshResult[];
  error?: string | null;
}

export type SpeechModel = 'base' | 'small' | 'whisper-large-v3' | 'whisper-large-v3-turbo';

export interface TranscriptionResponse {
  success: boolean;
  text: string;
  provider: string;
  model: SpeechModel | string;
  language?: string | null;
  duration?: number | null;
  error?: string | null;
}
