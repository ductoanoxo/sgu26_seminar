'use client';

import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { X, CheckCircle, AlertCircle, Info, AlertTriangle } from 'lucide-react';

type ToastType = 'success' | 'error' | 'info' | 'warning';

interface Toast {
  id: string;
  message: string;
  type: ToastType;
  duration?: number;
}

interface ToastContextType {
  showToast: (message: string, type: ToastType, duration?: number) => void;
}

const ToastContext = createContext<ToastContextType | undefined>(undefined);

export function useToast() {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
}

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const showToast = useCallback((message: string, type: ToastType = 'info', duration = 4000) => {
    const id = Math.random().toString(36).substring(2, 9);
    setToasts((prev) => [...prev, { id, message, type, duration }]);

    if (duration !== Infinity) {
      setTimeout(() => {
        removeToast(id);
      }, duration);
    }
  }, []);

  const removeToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  }, []);

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      <div className="toast-container">
        {toasts.map((toast) => (
          <ToastItem key={toast.id} toast={toast} onRemove={() => removeToast(toast.id)} />
        ))}
      </div>

      <style jsx>{`
        .toast-container {
          position: fixed;
          top: 24px;
          right: 24px;
          display: flex;
          flex-direction: column;
          gap: 12px;
          z-index: 9999;
          pointer-events: none;
        }

        @media (max-width: 640px) {
          .toast-container {
            top: auto;
            bottom: 24px;
            left: 24px;
            right: 24px;
          }
        }
      `}</style>
    </ToastContext.Provider>
  );
}

function ToastItem({ toast, onRemove }: { toast: Toast; onRemove: () => void }) {
  const getIcon = () => {
    switch (toast.type) {
      case 'success': return <CheckCircle size={20} className="text-green-400" />;
      case 'error': return <AlertCircle size={20} className="text-red-400" />;
      case 'warning': return <AlertTriangle size={20} className="text-yellow-400" />;
      default: return <Info size={20} className="text-blue-400" />;
    }
  };

  return (
    <div className={`toast-item ${toast.type} animate-slide-in`}>
      <div className="toast-icon">{getIcon()}</div>
      <div className="toast-message">{toast.message}</div>
      <button className="toast-close" onClick={onRemove}>
        <X size={16} />
      </button>

      <style jsx>{`
        .toast-item {
          pointer-events: auto;
          display: flex;
          align-items: center;
          gap: 12px;
          min-width: 300px;
          max-width: 450px;
          padding: 14px 18px;
          background: rgba(26, 27, 30, 0.9);
          backdrop-filter: blur(12px);
          -webkit-backdrop-filter: blur(12px);
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-radius: 12px;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
          color: white;
          animation: slideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .toast-item.success { border-left: 4px solid #10b981; }
        .toast-item.error { border-left: 4px solid #ef4444; }
        .toast-item.warning { border-left: 4px solid #f59e0b; }
        .toast-item.info { border-left: 4px solid #3b82f6; }

        .toast-icon {
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .toast-message {
          flex: 1;
          font-size: 14px;
          line-height: 1.5;
          font-weight: 500;
        }

        .toast-close {
          background: transparent;
          border: none;
          color: rgba(255, 255, 255, 0.4);
          cursor: pointer;
          padding: 4px;
          border-radius: 6px;
          transition: all 0.2s;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .toast-close:hover {
          background: rgba(255, 255, 255, 0.1);
          color: white;
        }

        @keyframes slideIn {
          from {
            opacity: 0;
            transform: translateX(100%) scale(0.9);
          }
          to {
            opacity: 1;
            transform: translateX(0) scale(1);
          }
        }

        .animate-slide-in {
          animation: slideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }

        :global(.text-green-400) { color: #10b981; }
        :global(.text-red-400) { color: #ef4444; }
        :global(.text-yellow-400) { color: #f59e0b; }
        :global(.text-blue-400) { color: #3b82f6; }
      `}</style>
    </div>
  );
}
