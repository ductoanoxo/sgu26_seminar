'use client';

import React, { useEffect, useState } from 'react';
import { Database, Table, Key, Hash, Type, LayoutGrid, Network } from 'lucide-react';
import { getConnectionSchema, TableSchema, previewTableData } from '@/lib/api';
import MermaidERD from './MermaidERD';
import DataTable from './DataTable';

function getCleanTableName(name: string) {
  let clean = name.replace(/^imported_/, '');
  clean = clean.replace(/_[a-f0-9]{8,12}$/i, '');
  return clean.toLowerCase();
}

function toMermaidId(name: string, prefix = 'T'): string {
  const safe = name.replace(/[^a-zA-Z0-9_]/g, '_');
  return /^[a-zA-Z_]/.test(safe) && safe.length > 0 ? safe : `${prefix}_${safe || 'unknown'}`;
}

function generateERD(schemas: TableSchema[]) {
  let erd = 'erDiagram\n';

  // Pre-compute sanitized names to reuse in relationship lines
  const safeNameMap = new Map<string, string>(
    schemas.map(t => [t.name, toMermaidId(t.name)])
  );

  schemas.forEach(table => {
    const safeTable = safeNameMap.get(table.name)!;

    // Pre-detect FK columns: both "customer_id" pattern AND direct "customer" name match
    const fkTargets = new Map<string, string>(); // colName → matched table name
    table.columns.forEach(c => {
      const lname = c.name.toLowerCase();
      if (lname === 'id' || lname === '_id') return;
      const baseName = lname.endsWith('_id') ? lname.slice(0, -3) : lname;
      if (!baseName) return;
      const variants = [baseName, baseName + 's', baseName + 'es', baseName.replace(/y$/, 'ies')];
      const match = schemas.find(s => s.name !== table.name && variants.includes(getCleanTableName(s.name)));
      if (match) fkTargets.set(c.name, match.name);
    });

    erd += `  ${safeTable} {\n`;
    table.columns.forEach(c => {
      const lname = c.name.toLowerCase();
      const isPK = lname === 'id' || lname === '_id';
      const isFK = !isPK && (lname.endsWith('_id') || fkTargets.has(c.name));
      const constraint = isPK ? ' PK' : isFK ? ' FK' : '';
      const safeType = (c.type || 'TEXT').replace(/[^a-zA-Z0-9_]/g, '') || 'TEXT';
      const safeName = toMermaidId(c.name, 'col');
      erd += `    ${safeType} ${safeName}${constraint}\n`;
    });
    erd += `  }\n`;

    // Draw relationships — deduplicate in case both "customer" and "customer_id" exist
    const drawn = new Set<string>();
    fkTargets.forEach((targetTable) => {
      if (drawn.has(targetTable)) return;
      drawn.add(targetTable);
      erd += `  ${safeNameMap.get(targetTable)} ||--o{ ${safeTable} : "has"\n`;
    });
  });
  return erd;
}

interface DatabasePreviewProps {
  onClose?: () => void;
  activeConnectionName: string | null;
  inline?: boolean;
}

export default function DatabasePreview({ onClose, activeConnectionName, inline }: DatabasePreviewProps) {
  const [schemas, setSchemas] = useState<TableSchema[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [dbType, setDbType] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'tables' | 'erd' | 'data'>('tables');
  
  const [activeDataTable, setActiveDataTable] = useState<string | null>(null);
  const [dataPreviewLoading, setDataPreviewLoading] = useState(false);
  const [dataPreview, setDataPreview] = useState<{ columns: string[], rows: any[] } | null>(null);
  const [dataPreviewError, setDataPreviewError] = useState('');
  const [dataPreviewLimit, setDataPreviewLimit] = useState(50);
  const [dataPreviewLoadedAt, setDataPreviewLoadedAt] = useState<Date | null>(null);

  const loadTableData = async (tableName: string, limit = dataPreviewLimit) => {
    setActiveDataTable(tableName);
    setViewMode('data');
    setDataPreviewLoading(true);
    setDataPreviewError('');
    try {
      const res = await previewTableData(tableName, limit);
      if (res.success && res.data) {
        setDataPreview(res.data);
        setDataPreviewLimit(limit);
        setDataPreviewLoadedAt(new Date());
      } else {
        setDataPreviewError(res.error || 'Failed to load data preview.');
      }
    } catch (err: any) {
      setDataPreviewError(err.message || 'Error loading data preview.');
    } finally {
      setDataPreviewLoading(false);
    }
  };

  useEffect(() => {
    const fetchSchema = async () => {
      setLoading(true);
      setError('');
      try {
        const data = await getConnectionSchema();
        if (data.success && data.raw_schema) {
          setSchemas(data.raw_schema);
          setDbType(data.db_type || null);
        } else if (data.success && !data.has_active) {
          setError('No active database connection found. Please connect to a database first.');
        } else {
          setError(data.error || 'Failed to load database schema');
        }
      } catch (err: any) {
        setError(err.message || 'Network error occurred while fetching schema');
      } finally {
        setLoading(false);
      }
    };
    fetchSchema();
  }, []);

  const activeTableSchema = activeDataTable
    ? schemas.find((schema) => schema.name === activeDataTable)
    : undefined;

  const content = (
    <div style={{ 
      padding: inline ? '0' : '24px', 
      backgroundColor: inline ? 'transparent' : 'var(--bg-secondary)', 
      maxHeight: inline ? '700px' : '75vh', 
      overflowY: viewMode === 'erd' ? 'hidden' : 'auto', // Prevent double scroll in ERD mode
      display: 'flex',
      flexDirection: 'column'
    }}>
      {loading ? (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '64px 0', gap: 16 }}>
          <div className="spinner-large" />
          <p style={{ color: 'var(--text-muted)' }}>Analyzing database schema...</p>
        </div>
      ) : error ? (
        <div style={{ color: 'var(--accent-error)', padding: '20px', textAlign: 'center', background: 'rgba(239, 68, 68, 0.1)', borderRadius: '8px', border: '1px solid rgba(239, 68, 68, 0.2)' }}>
          {error}
        </div>
      ) : schemas.length === 0 ? (
        <div style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '64px 0' }}>
          <LayoutGrid size={48} style={{ opacity: 0.5, margin: '0 auto 16px' }} />
          <p style={{ fontSize: 16 }}>No tables found in this database.</p>
          <p style={{ fontSize: 13, marginTop: 8, opacity: 0.7 }}>It might be empty or the credentials may lack read permissions.</p>
        </div>
      ) : viewMode === 'erd' ? (
        <div style={{ width: '100%', flex: 1, minHeight: '500px' }}>
          <MermaidERD chart={generateERD(schemas)} />
        </div>
      ) : viewMode === 'data' && activeDataTable ? (
        <div style={{ width: '100%', display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <button 
              onClick={() => setViewMode('tables')} 
              style={{ 
                padding: '8px 16px', 
                background: 'var(--bg-secondary)', 
                border: '1px solid var(--border-primary)', 
                borderRadius: '10px', 
                cursor: 'pointer', 
                color: 'var(--text-primary)',
                fontWeight: 600,
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                boxShadow: 'var(--shadow-sm)',
                transition: 'all 0.2s'
              }}
              className="hover-lift"
            >
              &larr; Back to Tables
            </button>
          </div>
          {dataPreviewLoading ? (
            <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-secondary)' }}>Loading data...</div>
          ) : dataPreviewError ? (
            <div style={{ padding: '20px', color: '#ef4444', background: '#fef2f2', borderRadius: '8px' }}>{dataPreviewError}</div>
          ) : dataPreview ? (
            <DataTable 
              columns={dataPreview.columns} 
              rows={dataPreview.rows} 
              rowCount={dataPreview.rows.length} 
              truncated={dataPreview.rows.length === dataPreviewLimit}
              tableName={activeDataTable}
              dbType={dbType}
              totalRows={activeTableSchema?.estimated_rows ?? null}
              columnInfo={activeTableSchema?.columns ?? []}
              limit={dataPreviewLimit}
              loadedAt={dataPreviewLoadedAt}
              onLimitChange={(limit) => loadTableData(activeDataTable, limit)}
            />
          ) : null}
        </div>
      ) : (

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '20px' }}>
          {schemas.map((table) => (
            <div key={table.name} style={{
              background: 'var(--bg-secondary)',
              borderRadius: '12px',
              border: '1px solid var(--border-primary)',
              overflow: 'hidden',
              display: 'flex',
              flexDirection: 'column',
              maxHeight: '350px',
              boxShadow: 'var(--shadow-sm)'
            }}>
              {/* Table Header */}
              <div style={{
                background: 'var(--bg-tertiary)',
                padding: '10px 14px',
                borderBottom: '1px solid var(--border-primary)',
                display: 'flex',
                flexDirection: 'column',
                gap: '6px',
                flexShrink: 0
              }}>
                {/* Row 1: icon + name + preview button */}
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '6px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--text-primary)', fontWeight: 600, fontSize: '13px', minWidth: 0 }}>
                    <Table size={14} color="var(--accent-primary)" style={{ flexShrink: 0 }} />
                    <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {table.name}
                    </span>
                  </div>
                  <button 
                    onClick={() => loadTableData(table.name)}
                    title="Preview table data"
                    style={{ 
                      background: 'var(--accent-primary)', 
                      border: 'none', 
                      padding: '3px 8px', 
                      borderRadius: '4px', 
                      fontSize: '11px', 
                      cursor: 'pointer', 
                      color: '#fff', 
                      fontWeight: 600,
                      whiteSpace: 'nowrap',
                      flexShrink: 0
                    }}
                  >
                    Preview
                  </button>
                </div>
                {/* Row 2: row count badge */}
                {table.estimated_rows !== undefined && table.estimated_rows !== null && (
                  <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
                    ~{table.estimated_rows.toLocaleString()} rows · {table.columns.length} cols
                  </div>
                )}
              </div>
              
              {/* Columns */}
              <div style={{ padding: '8px 0', overflowY: 'auto', flex: 1 }}>
                {table.columns.map((col) => (
                  <div key={col.name} style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    padding: '6px 16px',
                    fontSize: '13px',
                    borderBottom: '1px solid var(--border-primary)'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-secondary)' }}>
                      {(col.name.toLowerCase() === 'id' || col.name.toLowerCase() === '_id') ? (
                        <Key size={13} color="var(--accent-warning)" />
                      ) : col.name.toLowerCase().endsWith('_id') ? (
                        <Key size={13} color="var(--text-muted)" />
                      ) : col.type.toLowerCase().includes('char') || col.type.toLowerCase().includes('text') ? (
                        <Type size={13} color="var(--text-muted)" />
                      ) : (
                        <Hash size={13} color="var(--text-muted)" />
                      )}
                      <span style={{
                        fontWeight: (col.name.toLowerCase() === 'id' || col.name.toLowerCase() === '_id') ? 600 : 400,
                        color: (col.name.toLowerCase() === 'id' || col.name.toLowerCase() === '_id') ? 'var(--text-primary)' : 'var(--text-secondary)'
                      }}>
                        {col.name}
                      </span>
                    </div>
                    <div style={{ color: 'var(--accent-secondary)', fontFamily: 'monospace', fontSize: '11.5px', opacity: 0.9 }}>
                      {col.type}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );

  if (inline) {
    return (
      <div className="card fade-in-up" style={{ marginTop: '24px', textAlign: 'left', width: '100%', maxWidth: '100%', marginLeft: 'auto', marginRight: 'auto' }}>
        <div className="card-title" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Database size={20} color="var(--accent-primary)" />
            <span style={{ color: 'var(--text-secondary)' }}>DATABASE EXPLORER:</span> 
            <span style={{ color: 'var(--text-primary)', fontWeight: 600 }}>{activeConnectionName || 'Default Connection'}</span>
            {dbType && <span style={{ marginLeft: 8, fontSize: '11px', background: 'rgba(99,102,241,0.1)', color: 'var(--accent-primary)', padding: '2px 8px', borderRadius: '12px', fontWeight: 'bold' }}>{dbType.toUpperCase()}</span>}
          </div>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{ display: 'flex', background: 'var(--bg-tertiary)', borderRadius: '8px', padding: '4px' }}>
              <button 
                onClick={() => setViewMode('tables')}
                style={{ 
                  display: 'flex', alignItems: 'center', gap: '6px', padding: '6px 12px', fontSize: '12px', fontWeight: 500, borderRadius: '6px', border: 'none', cursor: 'pointer',
                  background: viewMode === 'tables' ? 'var(--bg-secondary)' : 'transparent',
                  color: viewMode === 'tables' ? 'var(--text-primary)' : 'var(--text-secondary)',
                  boxShadow: viewMode === 'tables' ? 'var(--shadow-sm)' : 'none'
                }}>
                <LayoutGrid size={14} />
                Tables
              </button>
              <button 
                onClick={() => setViewMode('erd')}
                style={{ 
                  display: 'flex', alignItems: 'center', gap: '6px', padding: '6px 12px', fontSize: '12px', fontWeight: 500, borderRadius: '6px', border: 'none', cursor: 'pointer',
                  background: viewMode === 'erd' ? 'var(--bg-secondary)' : 'transparent',
                  color: viewMode === 'erd' ? 'var(--text-primary)' : 'var(--text-secondary)',
                  boxShadow: viewMode === 'erd' ? 'var(--shadow-sm)' : 'none'
                }}>
                <Network size={14} />
                ER Diagram
              </button>
            </div>
            
            {onClose && (
              <button onClick={onClose} style={{ 
                background: 'transparent', 
                border: 'none', 
                color: 'var(--text-muted)', 
                cursor: 'pointer', 
                fontSize: '12px', 
                textDecoration: 'underline',
                display: 'flex',
                alignItems: 'center',
                gap: '4px'
              }}>
                Hide Preview
              </button>
            )}
          </div>
        </div>
        {content}
      </div>
    );
  }

  return (
    <div className="data-import-overlay fade-in">
      <div className="data-import-modal" style={{ maxWidth: '850px', width: '90%' }}>
        <div className="modal-header">
          <div>
            <h2 className="modal-title" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Database size={24} />
              Database Explorer
            </h2>
            <p className="modal-subtitle">
              Schema preview for: <strong>{activeConnectionName || 'Default Connection'}</strong>
              {dbType && <span style={{ marginLeft: 8, fontSize: '11px', background: 'rgba(99,102,241,0.2)', color: '#818cf8', padding: '2px 8px', borderRadius: '12px' }}>{dbType}</span>}
            </p>
          </div>
          {onClose && <button className="modal-close" onClick={onClose}>Close</button>}
        </div>
        <div className="modal-content">
          {content}
        </div>
      </div>
    </div>
  );
}
