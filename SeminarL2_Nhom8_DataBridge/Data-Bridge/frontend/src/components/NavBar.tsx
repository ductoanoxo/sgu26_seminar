'use client';

import React, { useEffect, useState } from 'react';
import { createClient } from '@/lib/supabase';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { LogOut, User, Layers, Zap, Sparkles } from 'lucide-react';

interface NavBarProps {
  onConnectClick?: () => void;
}

export default function NavBar({ onConnectClick }: NavBarProps) {
  const [user, setUser] = useState<any>(null);
  const supabase = createClient();
  const router = useRouter();

  useEffect(() => {
    // Get initial session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
    });

    // Listen for changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null);
    });

    return () => subscription.unsubscribe();
  }, [supabase.auth]);

  const handleLogout = async () => {
    localStorage.removeItem('activeConnection');
    await supabase.auth.signOut();
    router.push('/login');
    router.refresh();
  };

  return (
    <nav className="hero-nav">
      <div className="hero-nav-container">
        {/* Logo */}
        <Link href="/" className="hero-logo" style={{ textDecoration: 'none' }}>
          <div className="logo-icon-wrapper">
            <Layers size={22} strokeWidth={2.5} />
            <Zap 
              size={14} 
              fill="currentColor" 
              style={{ 
                position: 'absolute', 
                bottom: '-2px', 
                right: '-2px', 
                color: '#ec4899' 
              }} 
            />
            <Sparkles className="logo-sparkle" size={12} style={{ top: '-4px', right: '-4px' }} />
          </div>
          <span className="shimmer-text">
            Data Bridge
          </span>
        </Link>

        {/* Menu Items */}
        <ul className="hero-menu">
          <li><a href="#platform">Platform</a></li>
          <li>
            <a href="#features" className="hero-menu-item-with-icon">
              Features
            </a>
          </li>
          <li><a href="#projects">Projects</a></li>
          <li><a href="#community">Community</a></li>
          <li><a href="#contact">Contact</a></li>
        </ul>

        {/* Right side buttons */}
        <div className="hero-auth-buttons">
          <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
            {user ? (
              <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-secondary)' }}>
                  <User size={18} />
                  <span style={{ fontSize: '14px', fontWeight: 500 }}>{user.email}</span>
                </div>
                <button onClick={handleLogout} className="hero-btn-login" style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <LogOut size={16} />
                  Log Out
                </button>
              </div>
            ) : (
              <>
                <a href="/login" className="hero-btn-login">Log In</a>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
