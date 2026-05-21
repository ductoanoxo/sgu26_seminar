'use client';

import React, { useEffect, useRef, useState, FormEvent } from 'react';
import { Loader2, Mic, Square } from 'lucide-react';
import { transcribeSpeech } from '@/lib/api';
import { SpeechModel } from '@/types';

interface HeroSearchInputProps {
  onSubmit: (query: string) => void;
  isLoading?: boolean;
  onConnectClick?: () => void;
  onConnectionsClick?: () => void;
  activeConnectionName?: string | null;
  importedTables?: string[];
  onPreviewClick?: () => void;
}

export default function HeroSearchInput({ 
  onSubmit, 
  isLoading = false, 
  onConnectClick, 
  onConnectionsClick, 
  activeConnectionName,
  importedTables = [],
  onPreviewClick
}: HeroSearchInputProps) {
  const [query, setQuery] = useState('');
  const [speechModel, setSpeechModel] = useState<SpeechModel>('whisper-large-v3-turbo');
  const [isRecording, setIsRecording] = useState(false);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const [speechError, setSpeechError] = useState('');
  const [showConnectMenu, setShowConnectMenu] = useState(false);
  const connectMenuRef = useRef<HTMLDivElement | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const chunksRef = useRef<BlobPart[]>([]);

  useEffect(() => {
    return () => {
      streamRef.current?.getTracks().forEach((track) => track.stop());
    };
  }, []);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (connectMenuRef.current && !connectMenuRef.current.contains(e.target as Node)) {
        setShowConnectMenu(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (query.trim() && !isLoading) {
      onSubmit(query.trim());
    }
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    setIsRecording(false);
  };

  const handleVoiceClick = async () => {
    if (isRecording) {
      stopRecording();
      return;
    }

    if (!navigator.mediaDevices?.getUserMedia || typeof MediaRecorder === 'undefined') {
      setSpeechError('Browser does not support audio recording.');
      return;
    }

    setSpeechError('');
    chunksRef.current = [];

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;
      const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
        ? 'audio/webm;codecs=opus'
        : 'audio/webm';
      const recorder = new MediaRecorder(stream, { mimeType });

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      recorder.onstop = async () => {
        stream.getTracks().forEach((track) => track.stop());
        streamRef.current = null;
        const audioBlob = new Blob(chunksRef.current, { type: mimeType });
        if (!audioBlob.size) return;

        setIsTranscribing(true);
        try {
          const result = await transcribeSpeech(audioBlob, speechModel);
          if (!result.success) {
            setSpeechError(result.error || 'Transcription failed.');
            return;
          }
          setQuery(result.text);
        } catch (err) {
          setSpeechError(err instanceof Error ? err.message : 'Transcription failed.');
        } finally {
          setIsTranscribing(false);
        }
      };

      mediaRecorderRef.current = recorder;
      recorder.start();
      setIsRecording(true);
    } catch (err) {
      setSpeechError(err instanceof Error ? err.message : 'Microphone permission denied.');
    }
  };

  const speechBusy = isRecording || isTranscribing;

  return (
    <div className="hero-search-box">
      {/* Top row: Credit info & powered by */}
      <div className="hero-search-top">
        <div className="hero-credits">
          <span>60/450 credits</span>
          <button className="hero-btn-upgrade">Upgrade</button>
        </div>
        <div className="hero-powered-by">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>
          <span>Powered by GPT-4o</span>
        </div>
      </div>

      {/* Main input area */}
      <form onSubmit={handleSubmit} className="hero-search-main">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask any question about your data..."
          className="hero-input-field"
          disabled={isLoading || isTranscribing}
          maxLength={3000}
        />
        <button type="submit" className="hero-btn-submit" disabled={isLoading || !query.trim()}>
          {isLoading ? (
            <div className="hero-spinner"></div>
          ) : (
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m5 12 7-7 7 7"/><path d="M12 19V5"/></svg>
          )}
        </button>
      </form>

      {/* Bottom row: actions & counter */}
      <div className="hero-search-bottom">
        <div className="hero-search-actions">
          <div style={{ position: 'relative' }} ref={connectMenuRef}>
            <button
              type="button"
              className={`hero-action-btn${activeConnectionName ? ' hero-action-btn-active' : ''}`}
              onClick={() => setShowConnectMenu(prev => !prev)}
            >
              {activeConnectionName ? (
                <>
                  <span style={{ width: 7, height: 7, borderRadius: '50%', background: '#22c55e', display: 'inline-block', marginRight: 5 }} />
                  {activeConnectionName}
                </>
              ) : 'Connect Data'}
            </button>
            {showConnectMenu && (
              <div className="connect-dropdown">
                <div className="connect-dropdown-header">
                  <span>Connection Hub</span>
                  {activeConnectionName && (
                    <div className="connect-card-status-dot active"
                         style={{ background: '#22c55e', width: 8, height: 8 }} />
                  )}
                </div>

                {/* Active source card or placeholder */}
                {(activeConnectionName || importedTables.length > 0) ? (
                  <div className="connect-active-card">
                    <div className="connect-card-icon">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14a9 3 0 0 0 18 0V5"/><path d="M3 12a9 3 0 0 0 18 0"/></svg>
                    </div>
                    <div className="connect-card-info">
                      <div className="connect-card-label">Currently Active</div>
                      <div className="connect-card-title">
                        {activeConnectionName || 'Supabase (Imported)'}
                      </div>
                      <div className="connect-card-status">
                        <span className="connect-card-status-text" style={{ fontSize: 10, fontFamily: 'JetBrains Mono' }}>
                          {activeConnectionName ? 'Direct Connection' : `${importedTables.length} tables available`}
                        </span>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="connect-active-card" style={{ opacity: 0.6, borderStyle: 'dashed' }}>
                    <div className="connect-card-icon" style={{ background: 'rgba(255,255,255,0.05)', color: 'rgba(255,255,255,0.3)' }}>
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/></svg>
                    </div>
                    <div className="connect-card-info">
                      <div className="connect-card-label">No Active Source</div>
                      <div className="connect-card-title" style={{ fontSize: 12 }}>Connect to start querying</div>
                    </div>
                  </div>
                )}

                <div className="connect-dropdown-actions">

                  <button
                    type="button"
                    className="connect-dropdown-item"
                    onClick={() => { setShowConnectMenu(false); onConnectionsClick?.(); }}
                  >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>
                    Manage Connections
                  </button>
                  <button
                    type="button"
                    className="connect-dropdown-item"
                    onClick={() => { setShowConnectMenu(false); onConnectClick?.(); }}
                  >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
                    Import New Data
                  </button>
                </div>
              </div>
            )}
          </div>
          <button
            type="button"
            className="hero-action-btn"
            onClick={() => onPreviewClick?.()}
            title="Preview Database Schema"
          >
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>
            Preview Schema
          </button>
          <button
            type="button"
            className={`hero-action-btn ${isRecording ? 'recording' : ''}`}
            onClick={handleVoiceClick}
            disabled={isLoading || isTranscribing}
            title={isRecording ? 'Stop recording' : 'Record voice'}
          >
            {isTranscribing ? <Loader2 size={15} className="spin-icon" /> : isRecording ? <Square size={15} /> : <Mic size={15} />}
            {isTranscribing ? 'Transcribing' : isRecording ? 'Stop' : 'Voice'}
          </button>
          <select
            className="hero-stt-select"
            value={speechModel}
            onChange={(e) => setSpeechModel(e.target.value as SpeechModel)}
            disabled={isLoading || speechBusy}
            aria-label="Speech-to-text model"
          >
            <option value="base">Whisper base</option>
            <option value="small">Whisper small</option>
            <option value="whisper-large-v3">Groq large v3</option>
            <option value="whisper-large-v3-turbo">Groq turbo</option>
          </select>
        </div>
        <div className="hero-char-counter">
          {query.length}/3,000
        </div>
      </div>
      {speechError && <div className="hero-speech-error">{speechError}</div>}
    </div>
  );
}
