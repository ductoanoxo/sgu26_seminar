'use client';

import React, { useEffect, useState } from 'react';
import { listConnections, deleteConnection, shareConnection } from '@/lib/api';
import { Database, ChevronDown, Plus, Trash2, Edit2, UserPlus } from 'lucide-react';
import { useToast } from '@/context/ToastContext';
import ShareConnectionModal from './ShareConnectionModal';


interface Connection {
  id: string;
  name: string;
  db_type: string;
  host: string;
  port?: number;
  database_name: string;
  username?: string;
  ssl_enabled?: boolean;
  settings?: {
    uri?: string;
  };
}

export default function ConnectionSwitcher() {
  const [connections, setConnections] = useState<Connection[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [isOpen, setIsOpen] = useState(false);
  const [shareConnectionId, setShareConnectionId] = useState<string | null>(null);
  const { showToast } = useToast();


  useEffect(() => {
    loadConnections();
    
    // Initial sync with localStorage
    const savedId = localStorage.getItem('selected_connection_id');
    if (savedId) setSelectedId(savedId);

    // Sync on local storage changes
    const handleStorage = () => {
      setSelectedId(localStorage.getItem('selected_connection_id'));
    };
    window.addEventListener('storage', handleStorage);
    return () => window.removeEventListener('storage', handleStorage);
  }, []);

  const loadConnections = async () => {
    try {
      const res = await listConnections();
      if (res.success && res.connections) {
        setConnections(res.connections);
        
        // If no connection selected but we have list, pick the first one
        if (!localStorage.getItem('selected_connection_id') && res.connections.length > 0) {
          selectConnection(res.connections[0]);
        }
      }
    } catch (err) {
      console.error('Failed to load connections', err);
    }
  };

  const handleDelete = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    if (!confirm('Are you sure you want to delete this connection?')) return;
    
    try {
      const res = await deleteConnection(id);
      if (res.success) {
        showToast('Connection deleted', 'success');
        if (selectedId === id) {
          localStorage.removeItem('selected_connection_id');
          localStorage.removeItem('selected_connection_name');
          setSelectedId(null);
        }
        loadConnections();
      } else {
        showToast(res.error || 'Failed to delete connection', 'error');
      }
    } catch (err) {
      showToast('Error deleting connection', 'error');
    }
  };

  const handleEdit = (e: React.MouseEvent, connection: Connection) => {
    e.stopPropagation();
    // Dispatch an event that DataImport will listen to
    window.dispatchEvent(new CustomEvent('edit-connection', { detail: connection }));
    setIsOpen(false);
  };

  const handleShare = async (e: React.MouseEvent, connectionId: string) => {
    e.stopPropagation();
    setShareConnectionId(connectionId);
    setIsOpen(false);
  };


  const selectConnection = (conn: Connection) => {
    localStorage.setItem('selected_connection_id', conn.id);
    localStorage.setItem('selected_connection_name', conn.name);
    setSelectedId(conn.id);
    setIsOpen(false);
    // Dispatch event for other components
    window.dispatchEvent(new Event('storage'));
  };

  const selectedConnection = connections.find(c => c.id === selectedId);

  return (
    <div className="connection-switcher">
      <button className="switcher-toggle" onClick={() => setIsOpen(!isOpen)}>
        <Database size={16} />
        <span className="selected-name">
          {selectedConnection ? selectedConnection.name : 'Select Connection'}
        </span>
        <ChevronDown size={14} />
      </button>

      {isOpen && (
        <div className="switcher-dropdown animate-scale-in">
          <div className="dropdown-header">Your Connections</div>
          <div className="dropdown-list">
            {connections.length === 0 ? (
              <div className="no-connections">No connections found</div>
            ) : (
              connections.map(conn => (
                <div 
                  key={conn.id} 
                  className={`dropdown-item ${conn.id === selectedId ? 'active' : ''}`}
                  onClick={() => selectConnection(conn)}
                >
                  <div className="item-info">
                    <span className="item-name">{conn.name}</span>
                    <span className="item-meta">{conn.host} • {conn.database_name}</span>
                  </div>
                  <div className="item-actions">
                    <button 
                      className="action-icon-btn edit" 
                      onClick={(e) => handleEdit(e, conn)}
                      title="Edit connection"
                    >
                      <Edit2 size={14} />
                    </button>
                    <button 
                      className="action-icon-btn share" 
                      onClick={(e) => handleShare(e, conn.id)}
                      title="Share connection"
                    >
                      <UserPlus size={14} />
                    </button>
                    <button 
                      className="action-icon-btn delete" 
                      onClick={(e) => handleDelete(e, conn.id)}
                      title="Delete connection"
                    >
                      <Trash2 size={14} />
                    </button>
                    {conn.id === selectedId && <div className="active-dot" />}
                  </div>
                </div>
              ))
            )}
          </div>
          <button className="add-connection-btn" onClick={() => {
            setIsOpen(false);
            window.dispatchEvent(new CustomEvent('open-data-import'));
          }}>
            <Plus size={14} />
            Add New Connection
          </button>
        </div>
      )}

      {shareConnectionId && (
        <ShareConnectionModal 
          connectionId={shareConnectionId} 
          onClose={() => setShareConnectionId(null)} 
        />
      )}

      <style jsx>{`
        .connection-switcher {
          position: relative;
          font-family: inherit;
        }
        .switcher-toggle {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 8px 14px;
          background: #f8fafc;
          border: 1px solid #e2e8f0;
          border-radius: 9999px;
          color: var(--text-secondary);
          font-family: var(--font-inter);
          cursor: pointer;
          transition: all 0.2s ease;
          min-width: 140px;
        }
        .switcher-toggle:hover {
          background: #f1f5f9;
          border-color: #cbd5e1;
          color: var(--text-primary);
        }
        .selected-name {
          flex: 1;
          text-align: left;
          font-size: 13px;
          font-weight: 500;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
        .switcher-dropdown {
          position: absolute;
          top: calc(100% + 8px);
          right: 0;
          width: 340px;
          background: #ffffff;
          border: 1px solid rgba(0, 0, 0, 0.1);
          border-radius: 16px;
          box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
          z-index: 1000;
          overflow: hidden;
          animation: slideDown 0.2s ease-out;
        }
        .dropdown-header {
          padding: 12px 16px;
          font-size: 11px;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 0.05em;
          color: var(--text-muted, #94a3b8);
          border-bottom: 1px solid rgba(0, 0, 0, 0.05);
          background: rgba(0, 0, 0, 0.01);
        }
        .dropdown-list {
          max-height: 300px;
          overflow-y: auto;
        }
        .dropdown-item {
          display: flex;
          align-items: center;
          justify-content: space-between;
          width: 100%;
          padding: 12px 20px;
          background: transparent;
          border: none;
          border-bottom: 1px solid rgba(0, 0, 0, 0.03);
          color: var(--text-primary);
          text-align: left;
          cursor: pointer;
          transition: all 0.2s;
        }
        .dropdown-item:hover {
          background: rgba(0, 0, 0, 0.02);
        }
        .dropdown-item.active {
          background: rgba(37, 99, 235, 0.05);
          color: var(--accent-primary);
        }
        .item-actions {
          display: flex;
          align-items: center;
          gap: 12px;
          padding-left: 12px;
        }
        .action-icon-btn {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 28px;
          height: 28px;
          border-radius: 6px;
          border: none;
          background: transparent;
          color: var(--text-muted);
          cursor: pointer;
          transition: all 0.2s;
        }
        .action-icon-btn:hover {
          background: rgba(0, 0, 0, 0.05);
        }
        .action-icon-btn.edit:hover {
          color: var(--accent-primary);
          background: rgba(37, 99, 235, 0.1);
        }
        .action-icon-btn.delete:hover {
          color: var(--accent-error);
          background: rgba(239, 68, 68, 0.1);
        }
        .item-info {
          display: flex;
          flex-direction: column;
          gap: 2px;
        }
        .item-name {
          font-size: 14px;
          font-weight: 600;
        }
        .item-meta {
          font-size: 11px;
          color: var(--text-muted);
        }
        .active-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: #3b82f6;
          box-shadow: 0 0 12px rgba(59, 130, 246, 0.6);
          flex-shrink: 0;
        }
        .add-connection-btn {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 8px;
          width: 100%;
          padding: 14px;
          background: rgba(0, 0, 0, 0.02);
          border: none;
          color: var(--accent-primary);
          font-size: 13px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s;
        }
        .add-connection-btn:hover {
          background: rgba(37, 99, 235, 0.08);
          color: var(--accent-secondary);
        }
        .no-connections {
          padding: 24px;
          text-align: center;
          color: rgba(255, 255, 255, 0.3);
          font-size: 13px;
        }
      `}</style>
    </div>
  );
}
