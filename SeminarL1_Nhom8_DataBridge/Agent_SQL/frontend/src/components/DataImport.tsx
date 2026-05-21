'use client';

import React, { useState, useCallback } from 'react';

interface DataImportProps {
  onImportComplete?: (data: any) => void;
  onClose?: () => void;
}

export default function DataImport({ onImportComplete, onClose }: DataImportProps) {
  const [activeTab, setActiveTab] = useState<'file' | 'connection'>('file');
  const [isDragging, setIsDragging] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
  const [fileName, setFileName] = useState<string | null>(null);

  const [connParams, setConnParams] = useState({
    host: '',
    port: '5432',
    database: '',
    user: '',
    password: '',
    ssl: true
  });

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelect(files[0]);
    }
  };

  const handleFileSelect = (file: File) => {
    const validExtensions = ['.sql', '.xlsx', '.csv', '.db'];
    const extension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
    
    if (validExtensions.includes(extension)) {
      setFileName(file.name);
      simulateUpload();
    } else {
      alert('Invalid file type. Please upload .sql, .xlsx, .csv, or .db');
    }
  };

  const simulateUpload = () => {
    setUploadStatus('uploading');
    setTimeout(() => {
      setUploadStatus('success');
      if (onImportComplete) onImportComplete({ type: 'file', name: fileName });
    }, 2000);
  };

  const handleConnect = (e: React.FormEvent) => {
    e.preventDefault();
    setUploadStatus('uploading');
    setTimeout(() => {
      setUploadStatus('success');
      if (onImportComplete) onImportComplete({ type: 'connection', params: connParams });
    }, 2000);
  };

  return (
    <div className="data-import-overlay fade-in">
      <div className="data-import-modal">
        <div className="modal-header">
          <div className="modal-title-group">
            <div className="modal-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="17 8 12 3 7 8"></polyline>
                <line x1="12" y1="3" x2="12" y2="15"></line>
              </svg>
            </div>
            <div>
              <h2 className="modal-title">Connect Data Source</h2>
              <p className="modal-subtitle">Import your database to start analyzing with AI</p>
            </div>
          </div>
          <button className="modal-close" onClick={onClose}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <div className="modal-tabs">
          <button 
            className={`modal-tab ${activeTab === 'file' ? 'active' : ''}`}
            onClick={() => setActiveTab('file')}
          >
            Upload File
          </button>
          <button 
            className={`modal-tab ${activeTab === 'connection' ? 'active' : ''}`}
            onClick={() => setActiveTab('connection')}
          >
            Database Connection
          </button>
        </div>

        <div className="modal-content">
          {activeTab === 'file' ? (
            <div 
              className={`upload-zone ${isDragging ? 'dragging' : ''} ${uploadStatus === 'success' ? 'success' : ''}`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
            >
              <input 
                type="file" 
                id="file-upload" 
                className="hidden-input" 
                onChange={(e) => e.target.files?.[0] && handleFileSelect(e.target.files[0])}
                accept=".sql,.xlsx,.csv,.db"
              />
              
              {uploadStatus === 'idle' || uploadStatus === 'uploading' ? (
                <label htmlFor="file-upload" className="upload-label">
                  <div className="upload-icon-container">
                    {uploadStatus === 'uploading' ? (
                      <div className="spinner-large"></div>
                    ) : (
                      <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                        <polyline points="14 2 14 8 20 8"></polyline>
                        <line x1="12" y1="18" x2="12" y2="12"></line>
                        <line x1="9" y1="15" x2="15" y2="15"></line>
                      </svg>
                    )}
                  </div>
                  <div className="upload-text">
                    {uploadStatus === 'uploading' ? 'Uploading your data...' : (
                      <>
                        <strong>Click to upload</strong> or drag and drop
                        <span>SQL, XLSX, CSV, or SQLite DB</span>
                      </>
                    )}
                  </div>
                </label>
              ) : uploadStatus === 'success' ? (
                <div className="upload-success">
                  <div className="success-icon">
                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                  </div>
                  <h3>Successfully Connected!</h3>
                  <p>{fileName} has been parsed and indexed.</p>
                  <button className="btn-finish" onClick={onClose}>Continue to Dashboard</button>
                </div>
              ) : null}
            </div>
          ) : (
            <form className="connection-form" onSubmit={handleConnect}>
              <div className="form-grid">
                <div className="form-group full">
                  <label>Database Type</label>
                  <select className="form-input">
                    <option>PostgreSQL</option>
                    <option>MySQL</option>
                    <option>SQL Server</option>
                    <option>Oracle</option>
                  </select>
                </div>
                <div className="form-group grow">
                  <label>Host</label>
                  <input 
                    type="text" 
                    className="form-input" 
                    placeholder="localhost" 
                    value={connParams.host}
                    onChange={e => setConnParams({...connParams, host: e.target.value})}
                    required
                  />
                </div>
                <div className="form-group width-sm">
                  <label>Port</label>
                  <input 
                    type="text" 
                    className="form-input" 
                    placeholder="5432" 
                    value={connParams.port}
                    onChange={e => setConnParams({...connParams, port: e.target.value})}
                  />
                </div>
                <div className="form-group half">
                  <label>Database Name</label>
                  <input 
                    type="text" 
                    className="form-input" 
                    placeholder="my_database"
                    value={connParams.database}
                    onChange={e => setConnParams({...connParams, database: e.target.value})}
                    required
                  />
                </div>
                <div className="form-group half">
                  <label>Username</label>
                  <input 
                    type="text" 
                    className="form-input" 
                    placeholder="postgres"
                    value={connParams.user}
                    onChange={e => setConnParams({...connParams, user: e.target.value})}
                    required
                  />
                </div>
                <div className="form-group full">
                  <label>Password</label>
                  <input 
                    type="password" 
                    className="form-input" 
                    placeholder="••••••••"
                    value={connParams.password}
                    onChange={e => setConnParams({...connParams, password: e.target.value})}
                    required
                  />
                </div>
              </div>
              
              <div className="form-footer">
                <div className="ssl-toggle">
                  <input 
                    type="checkbox" 
                    id="ssl" 
                    checked={connParams.ssl}
                    onChange={e => setConnParams({...connParams, ssl: e.target.checked})}
                  />
                  <label htmlFor="ssl">Use SSL connection</label>
                </div>
                <button type="submit" className="btn-connect" disabled={uploadStatus === 'uploading'}>
                  {uploadStatus === 'uploading' ? (
                    <><div className="spinner"></div> Connecting...</>
                  ) : 'Connect Database'}
                </button>
              </div>
            </form>
          )}
        </div>
        
        <div className="modal-footer">
          <p className="security-note">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
            Your credentials are encrypted and never stored on our servers.
          </p>
        </div>
      </div>
    </div>
  );
}
