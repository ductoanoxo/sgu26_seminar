'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import VideoBackground from '@/components/VideoBackground';
import NavBar from '@/components/NavBar';
import { Mail, Lock, ArrowRight } from 'lucide-react';
import { createClient } from '@/lib/supabase';
import { useToast } from '@/context/ToastContext';


type AuthMode = 'login' | 'register';

export default function LoginPage() {
  const router = useRouter();
  const supabase = createClient();
  const { showToast } = useToast();

  const [mode, setMode] = useState<AuthMode>('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [isRedirecting, setIsRedirecting] = useState(false);

  useEffect(() => {
    // Check session immediately
    const checkAuth = async () => {
      const { data: { session } } = await supabase.auth.getSession();
      if (session?.user) {
        setIsRedirecting(true);
        window.location.href = '/';
      }
    };
    
    checkAuth();

    const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {
      if (session?.user && (event === 'SIGNED_IN' || event === 'INITIAL_SESSION')) {
        setIsRedirecting(true);
        window.location.href = '/';
      }
    });

    return () => subscription.unsubscribe();
  }, [supabase.auth]);

  const toggleMode = () => {
    setMode(mode === 'login' ? 'register' : 'login');
    setError('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      if (mode === 'register') {
        if (password !== confirmPassword) {
          throw new Error('Passwords do not match.');
        }
        const registerResponse = await fetch('/api/auth/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password }),
        });

        const registerData = await registerResponse.json().catch(() => ({}));
        if (!registerResponse.ok || !registerData.success) {
          const fallbackMessage = String(registerData.error || 'Registration failed.');
          const canFallbackToLogin = fallbackMessage.toLowerCase().includes('not configured');

          if (canFallbackToLogin) {
            const { error: signInError } = await supabase.auth.signInWithPassword({
              email,
              password,
            });

            if (!signInError) {
              setIsRedirecting(true);
              window.location.href = '/';
              return;
            }
          }

          throw new Error(fallbackMessage);
        }

        const { error: signInError } = await supabase.auth.signInWithPassword({
          email,
          password,
        });

        if (signInError) throw signInError;
        setIsRedirecting(true);
        window.location.href = '/';
        return;
      } else {
        const { error: signInError } = await supabase.auth.signInWithPassword({
          email,
          password,
        });
        if (signInError) throw signInError;
        setIsRedirecting(true);
        window.location.href = '/';
      }
    } catch (err: any) {
      const message = String(err?.message || 'Đã có lỗi xảy ra.');
      setError(message);
      showToast(message, 'error');
    } finally {

      setIsLoading(false);
    }
  };

  const handleGoogleLogin = async () => {
    try {
      const { error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo: `${window.location.origin}/auth/callback`,
        },
      });
      if (error) throw error;
    } catch (err: any) {
      setError(err.message || 'Lỗi đăng nhập Google');
    }
  };

  if (isRedirecting) {
    return (
      <main className="hero-section" style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <VideoBackground />
        <div className="flex-center flex-col gap-4" style={{ position: 'relative', zIndex: 100 }}>
          <div className="spinner" style={{ width: '40px', height: '40px' }} />
          <p className="text-white font-medium">Redirecting to dashboard...</p>
        </div>
      </main>
    );
  }


  return (
    <main className="hero-section" style={{ minHeight: '100vh', position: 'relative', overflow: 'hidden' }}>
      <VideoBackground />
      <div className="hero-content-wrapper" style={{ 
        position: 'relative', 
        zIndex: 20, 
        display: 'flex', 
        flexDirection: 'column', 
        minHeight: '100vh',
        width: '100%'
      }}>
        <NavBar />
        
        <div style={{ 
          flex: 1, 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center', 
          padding: '40px 20px',
          width: '100%'
        }}>
          <div className="auth-card fade-in-up" style={{ 
            width: '100%', 
            maxWidth: '440px',
            display: 'flex',
            flexDirection: 'column',
            margin: '0 auto'
          }}>
            <div className="auth-header">
              <div className="auth-icon-wrapper">
                <div className="auth-icon">
                  <Lock size={20} />
                </div>
              </div>
              <h1 className="auth-title">
                {mode === 'login' ? 'Welcome back' : 'Create an account'}
              </h1>
              <p className="auth-subtitle">
                {mode === 'login'
                  ? 'Sign in to save your query history'
                  : 'Sign up to experience the power of Data Bridge'}
              </p>
            </div>

            {error && (
              <div className="auth-error">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="auth-form" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              <div className="input-group" style={{ marginBottom: 0 }}>
                <label>Email address</label>
                <div className="input-wrapper">
                  <Mail className="input-icon" size={18} />
                  <input
                    type="email"
                    placeholder="name@company.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
              </div>

              <div className="input-group" style={{ marginBottom: 0 }}>
                <div className="label-row">
                  <label>Password</label>
                  {mode === 'login' && (
                    <a href="#" className="forgot-password">Forgot password?</a>
                  )}
                </div>
                <div className="input-wrapper">
                  <Lock className="input-icon" size={18} />
                  <input
                    type="password"
                    placeholder="••••••••"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </div>
              </div>

              {mode === 'register' && (
                <div className="input-group" style={{ marginBottom: 0 }}>
                  <div className="label-row">
                    <label>Confirm Password</label>
                  </div>
                  <div className="input-wrapper">
                    <Lock className="input-icon" size={18} />
                    <input
                      type="password"
                      placeholder="••••••••"
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      required
                    />
                  </div>
                </div>
              )}

              <button
                type="submit"
                className="auth-submit btn-primary"
                disabled={isLoading}
                style={{ marginTop: '4px' }}
              >
                {isLoading ? (
                  <div className="spinner" />
                ) : (
                  <>
                    {mode === 'login' ? 'Log in' : 'Sign up'}
                    <ArrowRight size={18} />
                  </>
                )}
              </button>

              <div className="auth-divider">
                <span>Or continue with</span>
              </div>

              <button
                type="button"
                onClick={handleGoogleLogin}
                className="google-btn btn-secondary"
                style={{ 
                  margin: 0,
                  width: '100%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '12px',
                  height: '48px',
                  borderRadius: '16px',
                  background: '#ffffff',
                  border: '1px solid var(--border-primary)',
                  fontWeight: 600,
                  fontSize: '14px',
                  cursor: 'pointer'
                }}
              >
                <svg width="18" height="18" viewBox="0 0 24 24">
                  <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                  <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                  <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z" fill="#FBBC05"/>
                  <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                </svg>
                <span>Continue with Google</span>
              </button>
            </form>

            <div className="auth-footer">
              <p>
                {mode === 'login'
                  ? "Don't have an account? "
                  : 'Already have an account? '}
                <button type="button" onClick={toggleMode} className="auth-toggle">
                  {mode === 'login' ? 'Create an account' : 'Log in'}
                </button>
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
