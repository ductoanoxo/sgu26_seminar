'use client';

import React, { useState } from 'react';
import { UploadCloud } from 'lucide-react';
import { createClient } from '@/lib/supabase';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

async function getAuthHeaders(): Promise<Record<string, string>> {
  try {
    const supabase = createClient();
    const { data: { session } } = await supabase.auth.getSession();
    if (session?.access_token) {
      return { Authorization: `Bearer ${session.access_token}` };
    }
  } catch {
    // ignore
  }
  return {};
}

interface DataImportProps {
  onImportComplete?: (data: any) => void;
  onClose?: () => void;
  initialConnection?: any;
}

// ── thêm 'supabase' từ archive (connection string only) ──────────────────────
type DBType = 'postgresql' | 'mysql' | 'mongodb' | 'sqlite' | 'redis' | 'supabase';
type Tab = 'database' | 'file';
type Step = 'connect' | 'select' | 'importing' | 'done';

interface ColumnInfo { name: string; type: string; }
interface SourceInfo { name: string; estimated_rows?: number; columns: ColumnInfo[]; }
interface ImportedTable { source: string; destination_table: string; rows_imported: number; }

const DB_TYPES: { value: DBType; label: string; defaultPort: number; icon: string; hint?: string; useUri?: boolean }[] = [
  { value: 'postgresql', label: 'PostgreSQL', defaultPort: 5432,  icon: 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/postgresql/postgresql-original.svg' },
  { value: 'mysql',      label: 'MySQL',      defaultPort: 3306,  icon: 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/mysql/mysql-original.svg' },
  { value: 'mongodb',    label: 'MongoDB',    defaultPort: 27017, icon: 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/mongodb/mongodb-original.svg', useUri: true },
  { value: 'supabase',   label: 'Supabase',   defaultPort: 5432,  icon: 'https://supabase.com/favicon/favicon-32x32.png', useUri: true },
  { value: 'redis',      label: 'Redis',      defaultPort: 6379,  icon: 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/redis/redis-original.svg', hint: 'Database = DB index (0–15)' },
  { value: 'sqlite',     label: 'SQLite',     defaultPort: 0,     icon: 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/sqlite/sqlite-original.svg' },
];

const FILE_FORMATS = [
  { label: 'CSV',     icon: 'https://img.icons8.com/color/48/csv.png' },
  { label: 'Excel',   icon: 'https://img.icons8.com/color/48/microsoft-excel-2019.png' },
  { label: 'JSON',    icon: 'https://img.icons8.com/color/48/json--v1.png' },
  { label: 'Parquet', icon: '/icons/parquet.png' },
  { label: 'SQL',     icon: 'https://img.icons8.com/color/48/sql.png' },
];

export default function DataImport({ onImportComplete, onClose }: DataImportProps) {
  const [tab, setTab]   = useState<Tab>('database');
  const [step, setStep] = useState<Step>('connect');

  // DB connection
  const [dbType,   setDbType]   = useState<DBType>('postgresql');
  const [host,     setHost]     = useState('localhost');
  const [port,     setPort]     = useState('5432');
  const [database, setDatabase] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  // ── thêm từ archive: connection string / URI ────────────────────────────
  const [useUri,            setUseUri]            = useState(false);
  const [connectionString,  setConnectionString]  = useState('');
  const [connName,          setConnName]          = useState('');

  // Shared flow state
  const [loading,       setLoading]       = useState(false);
  const [error,         setError]         = useState('');
  const [sources,       setSources]       = useState<SourceInfo[]>([]);
  const [selected,      setSelected]      = useState<Set<string>>(new Set());
  const [imported,      setImported]      = useState<ImportedTable[]>([]);
  const [importErrors,  setImportErrors]  = useState<string[]>([]);

  // File upload
  const [isDragging,   setIsDragging]   = useState(false);
  const [fileId,       setFileId]       = useState('');
  const [fileSources,  setFileSources]  = useState<SourceInfo[]>([]);
  const [fileSelected, setFileSelected] = useState<Set<string>>(new Set());

  /* ------------------------------------------------------------------ */

  const reset = () => {
    setStep('connect');
    setError('');
    setSources([]);
    setSelected(new Set());
    setImported([]);
    setImportErrors([]);
    setFileId('');
    setFileSources([]);
    setFileSelected(new Set());
    setConnectionString('');
    setUseUri(false);
    setConnName('');
    setLoading(false);
  };

  const handleDbTypeChange = (type: DBType) => {
    setDbType(type);
    const found = DB_TYPES.find(d => d.value === type);
    if (found && found.defaultPort > 0) setPort(String(found.defaultPort));
    // auto-enable URI mode for types that require it (từ archive)
    setUseUri(found?.useUri ?? false);
    setConnectionString('');
  };

  /* ── Step 1: Test connection + list tables ── */
  const handleConnect = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const backendDbType = dbType === 'supabase' ? 'postgresql' : dbType;

      // Send connection_string directly to backend — avoids browser URL parsing issues
      // (new URL() rejects non-standard schemes like mongodb+srv://)
      const body: Record<string, any> = {
        db_type:  backendDbType,
        host:     host || 'localhost',
        port:     port ? Number(port) : null,
        database: database,
        username: username || null,
        password: password || null,
      };
      if (useUri && connectionString) {
        body.connection_string = connectionString;
      }

      const authHeaders = await getAuthHeaders();
      const testRes  = await fetch(`${API_URL}/import/test-connection`, {
        method: 'POST', headers: { 'Content-Type': 'application/json', ...authHeaders }, body: JSON.stringify(body),
      });
      const testData = await testRes.json();
      if (!testData.success) { setError(testData.message || 'Connection failed'); return; }

      const listRes  = await fetch(`${API_URL}/import/list-sources`, {
        method: 'POST', headers: { 'Content-Type': 'application/json', ...authHeaders }, body: JSON.stringify(body),
      });
      const listData = await listRes.json();
      if (!listData.success) { setError(listData.error || 'Could not list tables'); return; }

      setSources(listData.sources || []);
      setSelected(new Set((listData.sources as SourceInfo[]).map(s => s.name)));
      setStep('select');
    } catch (err: any) {
      setError(err.message || 'Network error');
    } finally {
      setLoading(false);
    }
  };

  /* ── Step 2: Import selected tables ── */
  const handleImport = async () => {
    setStep('importing');
    setLoading(true);
    try {
      const backendDbType = dbType === 'supabase' ? 'postgresql' : dbType;

      const body: Record<string, any> = {
        db_type:  backendDbType,
        host:     host || 'localhost',
        port:     port ? Number(port) : null,
        database: database,
        username: username || null,
        password: password || null,
        tables:   Array.from(selected),
      };
      if (useUri && connectionString) {
        body.connection_string = connectionString;
      }

      if (connName.trim()) body.name = connName.trim();

      const authHeaders = await getAuthHeaders();
      const res  = await fetch(`${API_URL}/import/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...authHeaders },
        body: JSON.stringify(body),
      });
      const data = await res.json();
      setImported(data.imported || []);
      setImportErrors(data.errors || []);
      setStep('done');
      onImportComplete?.(data);
    } catch (err: any) {
      setError(err.message || 'Import failed');
      setStep('select');
    } finally {
      setLoading(false);
    }
  };

  /* ── File upload ── */
  const handleFileUpload = async (file: File) => {
    const validExts = ['.csv', '.xlsx', '.xls', '.json', '.parquet', '.sql'];
    const ext = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
    if (!validExts.includes(ext)) {
      setError('Unsupported file. Use CSV, Excel (.xlsx/.xls), JSON, Parquet, or SQL dump (.sql).');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const authHeaders = await getAuthHeaders();
      const form = new FormData();
      form.append('file', file);
      const res  = await fetch(`${API_URL}/import/upload-file`, { method: 'POST', body: form, headers: authHeaders });
      const data = await res.json();
      if (!data.success) { setError(data.error || 'Upload failed'); return; }
      setFileId(data.file_id);
      setFileSources(data.sources || []);
      setFileSelected(new Set((data.sources as SourceInfo[]).map(s => s.name)));
      setStep('select');
    } catch (err: any) {
      setError(err.message || 'Upload error');
    } finally {
      setLoading(false);
    }
  };

  const handleFileImport = async () => {
    setStep('importing');
    setLoading(true);
    try {
      const authHeaders = await getAuthHeaders();
      const res  = await fetch(`${API_URL}/import/execute-file`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...authHeaders },
        body: JSON.stringify({
          file_id: fileId,
          tables: Array.from(fileSelected),
          ...(connName.trim() ? { name: connName.trim() } : {}),
        }),
      });
      const data = await res.json();
      setImported(data.imported || []);
      setImportErrors(data.errors || []);
      setStep('done');
      onImportComplete?.(data);
    } catch (err: any) {
      setError(err.message || 'Import failed');
      setStep('select');
    } finally {
      setLoading(false);
    }
  };

  /* ------------------------------------------------------------------ */

  const currentSources  = tab === 'database' ? sources      : fileSources;
  const currentSelected = tab === 'database' ? selected     : fileSelected;
  const currentSetter   = tab === 'database' ? setSelected  : setFileSelected;

  const toggleSource = (name: string) => {
    const next = new Set(currentSelected);
    if (next.has(name)) next.delete(name); else next.add(name);
    currentSetter(next);
  };

  const currentDbDef = DB_TYPES.find(d => d.value === dbType);

  /* ------------------------------------------------------------------ */

  return (
    <div className="data-import-overlay fade-in">
      <div className="data-import-modal">

        {/* Header */}
        <div className="modal-header">
          <div>
            <h2 className="modal-title">Connect Data Source</h2>
            <p className="modal-subtitle">
              {step === 'connect'   && 'Connect your database or upload a file to start analysing'}
              {step === 'select'    && `Found ${currentSources.length} table(s) — choose which to import`}
              {step === 'importing' && 'Importing data into Supabase…'}
              {step === 'done'      && 'Import complete — you can now query your data with AI'}
            </p>
          </div>
          <button className="modal-close" onClick={onClose}>Close</button>
        </div>

        {/* Tabs */}
        {step === 'connect' && (
          <div className="modal-tabs">
            <button
              className={`modal-tab ${tab === 'database' ? 'active' : ''}`}
              onClick={() => { setTab('database'); reset(); }}
            >
              Database Connection
            </button>
            <button
              className={`modal-tab ${tab === 'file' ? 'active' : ''}`}
              onClick={() => { setTab('file'); reset(); }}
            >
              Upload File
            </button>
          </div>
        )}

        <div className="modal-content">

          {/* ══ DATABASE CONNECT ══ */}
          {tab === 'database' && step === 'connect' && (
            <form className="connection-form" onSubmit={handleConnect}>

              {/* DB type buttons */}
              <div className="form-group full" style={{ marginBottom: 16 }}>
                <label>Database Type</label>
                <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginTop: 8 }}>
                  {DB_TYPES.map(d => (
                    <button
                      key={d.value} type="button"
                      onClick={() => handleDbTypeChange(d.value)}
                      style={{
                        padding: '8px 16px', borderRadius: 8, cursor: 'pointer',
                        border: `2px solid ${dbType === d.value ? '#6366f1' : '#374151'}`,
                        background: dbType === d.value ? '#1e1b4b' : 'transparent',
                        color: '#f1f5f9', fontWeight: 500,
                        display: 'flex', alignItems: 'center', gap: 8,
                      }}
                    >
                      <img src={d.icon} alt={d.label} style={{ width: 20, height: 20, objectFit: 'contain' }} />
                      {d.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Hint for current DB type */}
              {currentDbDef?.hint && (
                <p style={{ color: '#818cf8', fontSize: 13, marginBottom: 12, marginTop: -8 }}>
                  ℹ {currentDbDef.hint}
                </p>
              )}

              {/* ── thêm từ archive: toggle connection method ── */}
              {currentDbDef?.useUri && (
                <div className="form-group full" style={{ marginBottom: 4 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <label style={{ margin: 0 }}>Connection Method</label>
                    <button
                      type="button"
                      onClick={() => { setUseUri(!useUri); setConnectionString(''); }}
                      style={{ color: '#818cf8', background: 'none', border: 'none', cursor: 'pointer', fontSize: 13, padding: 0 }}
                    >
                      {useUri ? 'Use standard form instead' : 'Use connection string (URI)'}
                    </button>
                  </div>
                </div>
              )}

              {/* ── thêm từ archive: URI input OR standard form ── */}
              {useUri ? (
                <div className="form-grid">
                  <div className="form-group full">
                    <label>Connection String (URI)</label>
                    <input
                      type="text"
                      className="form-input"
                      placeholder={
                        dbType === 'mongodb'
                          ? 'mongodb+srv://<user>:<password>@cluster0.xxxxx.mongodb.net/mydb'
                          : 'postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:5432/postgres'
                      }
                      value={connectionString}
                      onChange={e => setConnectionString(e.target.value)}
                      required
                    />
                    <p style={{ color: '#94a3b8', fontSize: 12, marginTop: 4 }}>
                      Credentials are used only for the import and are never stored.
                    </p>
                  </div>
                </div>
              ) : (
                <div className="form-grid">
                  {dbType === 'sqlite' ? (
                    <div className="form-group full">
                      <label>File Path (accessible by import-service container)</label>
                      <input type="text" className="form-input" placeholder="/data/mydb.db"
                        value={database} onChange={e => setDatabase(e.target.value)} required />
                    </div>
                  ) : (
                    <>
                      <div className="form-group grow">
                        <label>Host</label>
                        <input type="text" className="form-input" placeholder="localhost"
                          value={host} onChange={e => setHost(e.target.value)} required />
                      </div>
                      <div className="form-group width-sm">
                        <label>Port</label>
                        <input type="text" className="form-input"
                          value={port} onChange={e => setPort(e.target.value)} />
                      </div>
                      <div className="form-group half">
                        <label>{dbType === 'redis' ? 'DB Index' : 'Database Name'}</label>
                        <input type="text" className="form-input"
                          placeholder={dbType === 'redis' ? '0' : 'my_database'}
                          value={database} onChange={e => setDatabase(e.target.value)} />
                      </div>
                      {dbType !== 'redis' && (
                        <div className="form-group half">
                          <label>
                            Username
                            {dbType === 'mongodb' && <span style={{ color: '#94a3b8', fontWeight: 400 }}> (optional)</span>}
                          </label>
                          <input type="text" className="form-input"
                            placeholder={dbType === 'mongodb' ? 'optional' : 'postgres'}
                            value={username} onChange={e => setUsername(e.target.value)}
                            required={dbType !== 'mongodb'} />
                        </div>
                      )}
                      <div className={`form-group ${dbType === 'redis' ? 'half' : 'full'}`}>
                        <label>
                          Password
                          {(dbType === 'mongodb' || dbType === 'redis') && (
                            <span style={{ color: '#94a3b8', fontWeight: 400 }}> (optional)</span>
                          )}
                        </label>
                        <input type="password" className="form-input" placeholder="••••••••"
                          value={password} onChange={e => setPassword(e.target.value)} />
                      </div>
                    </>
                  )}
                </div>
              )}

              {error && <p style={{ color: '#f87171', marginTop: 8, fontSize: 14 }}>{error}</p>}

              <div className="form-footer">
                <div />
                <button type="submit" className="btn-connect" disabled={loading}>
                  {loading
                    ? <><span className="spinner" /> Connecting…</>
                    : 'Connect & List Tables'
                  }
                </button>
              </div>
            </form>
          )}

          {/* ══ FILE UPLOAD ══ */}
          {tab === 'file' && step === 'connect' && (
            <div
              className={`upload-zone ${isDragging ? 'dragging' : ''}`}
              onDragOver={e => { e.preventDefault(); setIsDragging(true); }}
              onDragLeave={() => setIsDragging(false)}
              onDrop={e => { e.preventDefault(); setIsDragging(false); const f = e.dataTransfer.files[0]; if (f) handleFileUpload(f); }}
            >
              <input type="file" id="file-upload" className="hidden-input"
                accept=".csv,.xlsx,.xls,.json,.parquet,.sql"
                onChange={e => { const f = e.target.files?.[0]; if (f) handleFileUpload(f); }} />
              <label htmlFor="file-upload" className="upload-label">
                {loading
                  ? (
                    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 16 }}>
                      <div className="spinner-large" />
                      <div className="upload-text" style={{ color: '#94a3b8' }}>Parsing file…</div>
                    </div>
                  )
                  : (
                    <div className="upload-text">
                      <div className="upload-icon-container">
                        <UploadCloud size={32} />
                      </div>
                      <strong style={{ fontSize: 18, marginBottom: 8, color: '#f1f5f9' }}>Click to upload or drag and drop</strong>
                      <p style={{ fontSize: 14, color: '#94a3b8', marginBottom: 12 }}>Supported formats: CSV, Excel, JSON, Parquet, SQL</p>
                      <div className="format-badges-container">
                        {FILE_FORMATS.map(f => (
                          <div key={f.label} className="format-badge">
                            <img src={f.icon} alt={f.label} />
                            <span className="format-badge-label">{f.label}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )
                }
              </label>
              {error && <p style={{ color: '#f87171', marginTop: 12, fontSize: 14 }}>{error}</p>}
            </div>
          )}

          {/* ══ SELECT TABLES ══ */}
          {step === 'select' && (
            <div>
              {/* Connection name input */}
              <div style={{ marginBottom: 16 }}>
                <label style={{ display: 'block', fontSize: 13, color: '#94a3b8', marginBottom: 6 }}>
                  Connection Name <span style={{ color: '#4b5563' }}>(optional)</span>
                </label>
                <input
                  type="text"
                  className="form-input"
                  placeholder={
                    tab === 'file'
                      ? 'e.g. Sales Data Q1'
                      : `e.g. My ${DB_TYPES.find(d => d.value === dbType)?.label || 'Database'}`
                  }
                  value={connName}
                  onChange={e => setConnName(e.target.value)}
                  style={{ width: '100%' }}
                />
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
                <span style={{ color: '#94a3b8', fontSize: 14 }}>
                  {currentSelected.size} / {currentSources.length} selected
                </span>
                <div style={{ display: 'flex', gap: 8 }}>
                  <button type="button" style={{ color: '#6366f1', background: 'none', border: 'none', cursor: 'pointer', fontSize: 13 }}
                    onClick={() => currentSetter(new Set(currentSources.map(s => s.name)))}>
                    Select all
                  </button>
                  <button type="button" style={{ color: '#94a3b8', background: 'none', border: 'none', cursor: 'pointer', fontSize: 13 }}
                    onClick={() => currentSetter(new Set())}>
                    Clear
                  </button>
                </div>
              </div>
              <div style={{ maxHeight: 300, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 8 }}>
                {currentSources.map(src => (
                  <label key={src.name} style={{
                    display: 'flex', alignItems: 'center', gap: 12, padding: '10px 14px',
                    borderRadius: 8, cursor: 'pointer', border: '1px solid',
                    borderColor: currentSelected.has(src.name) ? '#6366f1' : '#374151',
                    background: currentSelected.has(src.name) ? 'rgba(99,102,241,0.08)' : 'transparent',
                  }}>
                    <input type="checkbox"
                      checked={currentSelected.has(src.name)}
                      onChange={() => toggleSource(src.name)}
                      style={{ accentColor: '#6366f1', width: 16, height: 16 }} />
                    <div style={{ flex: 1 }}>
                      <div style={{ fontWeight: 600, color: '#f1f5f9' }}>{src.name}</div>
                      <div style={{ fontSize: 12, color: '#94a3b8' }}>
                        {src.columns.length} columns
                        {src.estimated_rows != null && ` · ~${src.estimated_rows.toLocaleString()} rows`}
                      </div>
                    </div>
                    <span style={{ fontSize: 11, color: '#818cf8', background: 'rgba(99,102,241,0.15)', padding: '2px 8px', borderRadius: 12 }}>
                      → imported_{src.name.toLowerCase().replace(/[^a-z0-9]/g, '_')}
                    </span>
                  </label>
                ))}
              </div>
              {error && <p style={{ color: '#f87171', marginTop: 8, fontSize: 14 }}>{error}</p>}
              <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 16 }}>
                <button type="button" onClick={reset}
                  style={{ color: '#94a3b8', background: 'none', border: '1px solid #374151', borderRadius: 8, padding: '8px 16px', cursor: 'pointer' }}>
                  ← Back
                </button>
                <button type="button" className="btn-connect"
                  disabled={currentSelected.size === 0}
                  onClick={tab === 'database' ? handleImport : handleFileImport}>
                  Import {currentSelected.size} table{currentSelected.size !== 1 ? 's' : ''}
                </button>
              </div>
            </div>
          )}

          {/* ══ IMPORTING ══ */}
          {step === 'importing' && (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '48px 0', gap: 16 }}>
              <div className="spinner-large" />
              <p style={{ color: '#94a3b8' }}>Importing data into Supabase…</p>
            </div>
          )}

          {/* ══ DONE ══ */}
          {step === 'done' && (
            <div className="upload-success">
              <h3 className="success-header">
                {imported.length > 0 ? '✓ Import Complete!' : 'Finished with errors'}
              </h3>
              {imported.map(t => (
                <div key={t.destination_table} className="import-detail-item">
                  <div className="import-table-name">
                    <span className="import-table-source">{t.source}</span>
                    <span className="import-table-arrow">→</span>
                    <span className="import-table-dest">{t.destination_table}</span>
                  </div>
                  <span className="import-table-rows">{t.rows_imported.toLocaleString()} rows</span>
                </div>
              ))}
              {importErrors.map((e, i) => (
                <div key={i} style={{ fontSize: 13, color: '#f87171', marginBottom: 8, padding: '0 4px' }}>⚠ {e}</div>
              ))}
              <p className="success-message">You can now query your imported data using natural language.</p>
              <button className="btn-success-action" onClick={onClose}>Continue to Dashboard</button>
            </div>
          )}
        </div>

        {/* ── thêm từ archive: instructions panel ── */}
        <div className="modal-instructions-area">
          {tab === 'database' && step === 'connect' && dbType === 'mongodb' && (
            <div className="instruction-block">
              <h4>
                <img src="https://upload.wikimedia.org/wikipedia/commons/9/93/MongoDB_Logo.svg" alt="MongoDB" style={{ height: 16 }} />
                {' '}MongoDB Atlas
              </h4>
              <p>To connect your MongoDB Atlas cluster:</p>
              <ol style={{ paddingLeft: '16px', fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '16px' }}>
                <li>Log in to <strong>MongoDB Atlas</strong></li>
                <li>Click <strong>Connect</strong> on your cluster</li>
                <li>Choose <strong>Drivers</strong></li>
                <li>Copy the provided connection string</li>
              </ol>
              <p>Example URI:</p>
              <pre>mongodb+srv://&lt;username&gt;:&lt;password&gt;@cluster.mongodb.net/test</pre>
              <a href="https://www.mongodb.com/docs/atlas/tutorial/connect-to-your-cluster/" target="_blank" rel="noreferrer">View Official Guide →</a>
            </div>
          )}
          {tab === 'database' && step === 'connect' && dbType === 'supabase' && (
            <div className="instruction-block">
              <h4>
                <img src="https://supabase.com/favicon/favicon-32x32.png" alt="Supabase" style={{ height: 16 }} />
                {' '}Supabase
              </h4>
              <p>To connect your Supabase project:</p>
              <ol style={{ paddingLeft: '16px', fontSize: '13px', color: 'var(--text-secondary)', marginBottom: '16px' }}>
                <li>Go to <strong>Project Settings</strong> → <strong>Database</strong></li>
                <li>Scroll down to <strong>Connection String</strong></li>
                <li>Select the <strong>URI</strong> tab</li>
                <li>Use the <strong>Session Pooler</strong> (port 5432) for IPv4 compatibility</li>
              </ol>
              <p>Example URI:</p>
              <pre>postgresql://postgres:[PASSWORD]@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres</pre>
              <a href="https://supabase.com/docs/guides/database/connecting-to-postgres" target="_blank" rel="noreferrer">View Official Guide →</a>
            </div>
          )}
        </div>

        <div className="modal-footer">
          <p className="security-note">
            Credentials are used only for the import and are never stored on our servers.
          </p>
        </div>
      </div>
    </div>
  );
}

const logger = {
  error: (...args: any[]) => console.error('[DataImport]', ...args)
};
