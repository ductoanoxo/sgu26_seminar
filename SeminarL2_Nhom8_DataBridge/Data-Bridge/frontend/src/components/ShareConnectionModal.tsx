'use client';

import React, { useState, useEffect } from 'react';
import { X, UserPlus, Trash2, Shield, User } from 'lucide-react';
import { shareConnection, listConnectionMembers, removeConnectionMember } from '@/lib/api';
import { useToast } from '@/context/ToastContext';

interface Member {
  email: string;
  role: string;
  granted_at: string;
}

interface ShareConnectionModalProps {
  connectionId: string;
  onClose: () => void;
}

export default function ShareConnectionModal({ connectionId, onClose }: ShareConnectionModalProps) {
  const [email, setEmail] = useState('');
  const [members, setMembers] = useState<Member[]>([]);
  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(true);
  const { showToast } = useToast();

  useEffect(() => {
    fetchMembers();
  }, [connectionId]);

  const fetchMembers = async () => {
    setFetching(true);
    try {
      const res = await listConnectionMembers(connectionId);
      if (res.success && res.members) {
        setMembers(res.members);
      } else {
        showToast(res.error || 'Failed to load members', 'error');
      }
    } catch (err: any) {
      showToast(err.message || 'Error loading members', 'error');
    } finally {
      setFetching(false);
    }
  };

  const handleShare = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim()) return;

    setLoading(true);
    try {
      const res = await shareConnection(connectionId, email.trim(), 'viewer');
      if (res.success) {
        showToast(`Connection shared with ${email}`, 'success');
        setEmail('');
        fetchMembers(); // Refresh list
      } else {
        showToast(res.error || 'Failed to share connection', 'error');
      }
    } catch (err: any) {
      showToast(err.message || 'An error occurred', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleRemove = async (targetEmail: string) => {
    if (!window.confirm(`Are you sure you want to remove access for ${targetEmail}?`)) return;

    try {
      const res = await removeConnectionMember(connectionId, targetEmail);
      if (res.success) {
        showToast(`Removed access for ${targetEmail}`, 'success');
        fetchMembers();
      } else {
        showToast(res.error || 'Failed to remove member', 'error');
      }
    } catch (err: any) {
      showToast(err.message || 'An error occurred', 'error');
    }
  };

  return (
    <div className="data-import-overlay fade-in">
      <div className="share-modal">
        <div className="modal-header">
          <div className="modal-header-content">
            <div>
              <h2 className="modal-title">Share Connection</h2>
              <p className="modal-subtitle">Manage who has access to this database</p>
            </div>
          </div>
          <button className="modal-close" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        <div className="share-modal-body">
          <form className="share-input-group" onSubmit={handleShare}>
            <input
              type="email"
              className="form-input"
              placeholder="Enter user's email address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <button type="submit" className="btn-share" disabled={loading || !email.trim()}>
              {loading ? <div className="spinner-small" /> : <UserPlus size={16} />}
              Share
            </button>
          </form>

          <div className="members-section">
            <h3 className="members-title">People with access</h3>
            
            {fetching ? (
              <div className="members-loading">Loading members...</div>
            ) : members.length === 0 ? (
              <div className="no-members">No one else has access yet.</div>
            ) : (
              <div className="members-list">
                {members.map((member) => (
                  <div key={member.email} className="member-item">
                    <div className="member-info">
                      <div className="member-avatar">
                        <User size={16} />
                      </div>
                      <div className="member-details">
                        <span className="member-email">{member.email}</span>
                        <span className="member-role">
                          {member.role === 'admin' ? <Shield size={12} className="admin-icon" /> : null}
                          {member.role.charAt(0).toUpperCase() + member.role.slice(1)}
                        </span>
                      </div>
                    </div>
                    {member.role !== 'admin' && (
                      <button 
                        className="btn-remove-member"
                        onClick={() => handleRemove(member.email)}
                        title="Remove access"
                      >
                        <Trash2 size={16} />
                      </button>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
