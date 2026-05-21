'use client';

import React, { useState, useEffect, useCallback } from 'react';
import {
  SavedConnection,
  CreateConnectionPayload,
  listConnections,
  createConnection,
  deleteConnection,
  activateConnection,
} from '@/lib/api';

interface Props {
  onClose: () => void;
  onActiveChange?: (conn: SavedConnection | null) => void;
}

const DB_TYPES = [
  { value: 'postgresql', label: 'PostgreSQL', defaultPort: 5432 },
  { value: 'mysql',      label: 'MySQL',      defaultPort: 3306 },
  { value: 'mongodb',    label: 'MongoDB',    defaultPort: 27017 },
  { value: 'redis',      label: 'Redis',      defaultPort: 6379 },
  { value: 'sqlite',     label: 'SQLite',     defaultPort: 0 },
];

const DB_ICONS: Record<string, string> = {
  postgresql: 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg',
  mysql:      'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original.svg',
  mongodb:    'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mongodb/mongodb-original.svg',
  redis:      'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/redis/redis-original.svg',
  sqlite:     'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlite/sqlite-original.svg',
  file:       "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23818cf8' stroke-width='2'><path d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'/><polyline points='14,2 14,8 20,8'/></svg>",
};

export default function ConnectionSidebar({ onClose, onActiveChange }: Props) {
  const [connections, setConnections] = useState<SavedConnection[]>([]);
  const [loading, setLoading]         = useState(false);
  const [error, setError]             = useState('');
  const [showForm, setShowForm]       = useState(false);
  const [saving, setSaving]           = useState(false);

  const [form, setForm] = useState<CreateConnectionPayload & { port_str: string }>({
    name: '',
    db_type: 'postgresql',
    host: 'localhost',
    port: 5432,
    port_str: '5432',
    database_name: '',
    username: '',
    password: '',
  });

  const load = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const res = await listConnections();
      if (res.success) setConnections(res.connections);
    } catch (e: any) {
      setError(e.message || 'Failed to load connections');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const handleDbTypeChange = (val: string) => {
    const meta = DB_TYPES.find(t => t.value === val);
    const p = meta?.defaultPort || 0;
    setForm(f => ({ ...f, db_type: val, port: p, port_str: p > 0 ? String(p) : '' }));
  };

  const handlePortChange = (val: string) => {
    const n = parseInt(val);
    setForm(f => ({ ...f, port_str: val, port: isNaN(n) ? null : n }));
  };

  const handleSave = async () => {
    if (!form.name.trim()) { setError('Name is required'); return; }
    setSaving(true);
    setError('');
    try {
      const payload: CreateConnectionPayload = {
        name: form.name.trim(),
        db_type: form.db_type,
        host: form.host || 'localhost',
        port: form.port || null,
        database_name: form.database_name || '',
        username: form.username || null,
        password: form.password || null,
      };
      const res = await createConnection(payload);
      if (res.success && res.connection) {
        setConnections(prev => [res.connection!, ...prev]);
        setShowForm(false);
        setForm({ name: '', db_type: 'postgresql', host: 'localhost', port: 5432, port_str: '5432', database_name: '', username: '', password: '' });
      } else {
        setError(res.error || 'Failed to save connection');
      }
    } catch (e: any) {
      setError(e.message || 'Failed to save connection');
    } finally {
      setSaving(false);
    }
  };

  const handleActivate = async (conn: SavedConnection) => {
    try {
      await activateConnection(conn.id);
      setConnections(prev => prev.map(c => ({ ...c, is_active: c.id === conn.id })));
      onActiveChange?.({ ...conn, is_active: true });
    } catch (e: any) {
      setError(e.message || 'Failed to activate');
    }
  };

  const handleDelete = async (connId: string) => {
    try {
      await deleteConnection(connId);
      setConnections(prev => prev.filter(c => c.id !== connId));
    } catch (e: any) {
      setError(e.message || 'Failed to delete');
    }
  };

  const activeConn = connections.find(c => c.is_active);

  return (
    <div className="conn-sidebar-overlay" onClick={onClose}>
      <aside className="conn-sidebar" onClick={e => e.stopPropagation()}>
        {/* Header */}
        <div className="conn-sidebar-header">
          <span className="conn-sidebar-title">Connections</span>
          <button className="conn-close-btn" onClick={onClose} type="button">✕</button>
        </div>

        {activeConn && (
          <div className="conn-active-banner">
            {DB_ICONS[activeConn.db_type] && <img src={DB_ICONS[activeConn.db_type]} alt="" width={16} height={16} />}
            <span>Active: <b>{activeConn.name}</b></span>
          </div>
        )}

        {error && <div className="conn-error">{error}</div>}

        {/* Add new */}
        {!showForm ? (
          <button className="conn-add-btn" onClick={() => { setShowForm(true); setError(''); }} type="button">
            + New Connection
          </button>
        ) : (
          <div className="conn-form">
            <div className="conn-form-grid">
              <div className="conn-form-row full">
                <label>Display Name</label>
                <input value={form.name} onChange={e => setForm(f => ({ ...f, name: e.target.value }))} placeholder="Production Database" />
              </div>
              <div className="conn-form-row full">
                <label>Database Type</label>
                <select value={form.db_type} onChange={e => handleDbTypeChange(e.target.value)}>
                  {DB_TYPES.map(t => <option key={t.value} value={t.value}>{t.label}</option>)}
                </select>
              </div>
              {form.db_type !== 'sqlite' && (
                <>
                  <div className="conn-form-row">
                    <label>Host</label>
                    <input value={form.host ?? ''} onChange={e => setForm(f => ({ ...f, host: e.target.value }))} placeholder="localhost" />
                  </div>
                  <div className="conn-form-row">
                    <label>Port</label>
                    <input value={form.port_str} onChange={e => handlePortChange(e.target.value)} placeholder="5432" />
                  </div>
                </>
              )}
              <div className="conn-form-row full">
                <label>{form.db_type === 'sqlite' ? 'File path' : form.db_type === 'redis' ? 'DB index' : 'Database Name'}</label>
                <input value={form.database_name} onChange={e => setForm(f => ({ ...f, database_name: e.target.value }))} placeholder={form.db_type === 'sqlite' ? '/data/mydb.db' : form.db_type === 'redis' ? '0' : 'mydb'} />
              </div>
              {form.db_type !== 'sqlite' && form.db_type !== 'redis' && (
                <>
                  <div className="conn-form-row">
                    <label>Username</label>
                    <input value={form.username || ''} onChange={e => setForm(f => ({ ...f, username: e.target.value }))} placeholder="user" />
                  </div>
                  <div className="conn-form-row">
                    <label>Password</label>
                    <input type="password" value={form.password || ''} onChange={e => setForm(f => ({ ...f, password: e.target.value }))} placeholder="••••••" />
                  </div>
                </>
              )}
            </div>
            <div className="conn-form-actions">
              <button className="conn-save-btn" onClick={handleSave} disabled={saving} type="button">
                {saving ? 'Saving...' : 'Save Connection'}
              </button>
              <button className="conn-cancel-btn" onClick={() => { setShowForm(false); setError(''); }} type="button">Cancel</button>
            </div>
          </div>
        )}

        <div className="conn-list-header">Saved Connections</div>

        {/* Connection list */}
        <div className="conn-list">
          {loading && <div className="conn-empty">Loading...</div>}
          {!loading && connections.length === 0 && (
            <div className="conn-empty">No saved connections</div>
          )}
          {connections.map(conn => (
            <div key={conn.id} className={`conn-item${conn.is_active ? ' conn-item-active' : ''}`}>
              <img src={DB_ICONS[conn.db_type] || ''} alt={conn.db_type} width={20} height={20} className="conn-item-icon" />
              <div className="conn-item-info">
                <div className="conn-item-name">{conn.name}</div>
                <div className="conn-item-meta">{conn.db_type === 'file' ? 'file · imported' : `${conn.db_type}${conn.host ? ` · ${conn.host}` : ''}`}</div>
              </div>
              <div className="conn-item-actions">
                {conn.is_active ? (
                  <span className="conn-active-badge">Active</span>
                ) : (
                  <button className="conn-use-btn" onClick={() => handleActivate(conn)} type="button">Use</button>
                )}
                <button className="conn-del-btn" onClick={() => handleDelete(conn.id)} type="button" title="Delete">✕</button>
              </div>
            </div>
          ))}
        </div>
      </aside>
    </div>
  );
}
