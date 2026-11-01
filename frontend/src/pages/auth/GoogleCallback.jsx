/**
 * Google OAuth Callback Page
 * Handles the redirect from Google after OAuth authorization
 */

import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { useGoogleAuth } from '@/hooks/useGoogleAuth';
import { Loader2, AlertCircle, CheckCircle } from 'lucide-react';

const GoogleCallback = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { setUser, setIsAuthenticated } = useAuth();
  const { handleGoogleCallback } = useGoogleAuth();
  const [status, setStatus] = useState('processing'); // processing, success, error
  const [message, setMessage] = useState('Completing sign in with Google...');

  useEffect(() => {
    const processCallback = async () => {
      // Get authorization code and state from URL
      const code = searchParams.get('code');
      const state = searchParams.get('state');
      const error = searchParams.get('error');

      // Check for OAuth errors
      if (error) {
        setStatus('error');
        setMessage(
          error === 'access_denied'
            ? 'You cancelled the sign-in process.'
            : 'Google authentication failed. Please try again.'
        );
        setTimeout(() => navigate('/login'), 3000);
        return;
      }

      // Validate required parameters
      if (!code || !state) {
        setStatus('error');
        setMessage('Invalid callback parameters. Please try signing in again.');
        setTimeout(() => navigate('/login'), 3000);
        return;
      }

      // Exchange code for tokens
      const result = await handleGoogleCallback(code, state);

      if (result.success) {
        setStatus('success');
        setMessage(
          result.isNewUser
            ? 'Account created successfully! Redirecting...'
            : 'Welcome back! Redirecting...'
        );

        // Update auth context
        setUser(result.user);
        setIsAuthenticated(true);

        // Redirect based on role
        setTimeout(() => {
          const role = result.user.role;
          if (role === 'admin') {
            navigate('/admin/dashboard');
          } else if (role === 'doctor') {
            navigate('/doctor/dashboard');
          } else {
            navigate('/patient/dashboard');
          }
        }, 1500);
      } else {
        setStatus('error');
        setMessage(result.error || 'Failed to complete Google sign-in');
        setTimeout(() => navigate('/login'), 3000);
      }
    };

    processCallback();
  }, [searchParams, navigate, handleGoogleCallback, setUser, setIsAuthenticated]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-cyan-50 dark:from-neutral-900 dark:to-neutral-800 p-4">
      <div className="bg-white dark:bg-neutral-800 rounded-2xl shadow-2xl p-8 max-w-md w-full text-center">
        {status === 'processing' && (
          <>
            <Loader2 className="w-16 h-16 text-primary-500 animate-spin mx-auto mb-4" />
            <h2 className="text-xl font-bold text-neutral-900 dark:text-white mb-2">
              Processing Sign In
            </h2>
            <p className="text-neutral-600 dark:text-neutral-400">{message}</p>
          </>
        )}

        {status === 'success' && (
          <>
            <CheckCircle className="w-16 h-16 text-emerald-500 mx-auto mb-4" />
            <h2 className="text-xl font-bold text-neutral-900 dark:text-white mb-2">
              Success!
            </h2>
            <p className="text-neutral-600 dark:text-neutral-400">{message}</p>
          </>
        )}

        {status === 'error' && (
          <>
            <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
            <h2 className="text-xl font-bold text-neutral-900 dark:text-white mb-2">
              Sign In Failed
            </h2>
            <p className="text-neutral-600 dark:text-neutral-400 mb-4">{message}</p>
            <button
              onClick={() => navigate('/login')}
              className="px-6 py-2 bg-primary-500 hover:bg-primary-600 text-white rounded-xl font-medium transition-colors"
            >
              Back to Login
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default GoogleCallback;
