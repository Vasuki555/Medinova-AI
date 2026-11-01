/**
 * Google OAuth Hook
 * Handles Google Sign-In integration
 */

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiService } from '@/services/api';

export const useGoogleAuth = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const initiateGoogleLogin = async () => {
    try {
      setLoading(true);
      setError(null);

      // Get Google OAuth URL from backend
      const response = await apiService.get('/oauth/google/url');
      const { auth_url, state } = response;

      // Store state for CSRF protection
      sessionStorage.setItem('google_oauth_state', state);

      // Redirect to Google OAuth
      window.location.href = auth_url;
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to initiate Google login');
      setLoading(false);
    }
  };

  const handleGoogleCallback = async (code, state) => {
    try {
      setLoading(true);
      setError(null);

      // Verify state matches (CSRF protection)
      const savedState = sessionStorage.getItem('google_oauth_state');
      if (state !== savedState) {
        throw new Error('Invalid state parameter. Possible CSRF attack.');
      }

      // Exchange code for tokens
      const response = await apiService.post('/oauth/google/callback', {
        code: code,
        redirect_uri: import.meta.env.VITE_GOOGLE_REDIRECT_URI || 'http://localhost:5173/auth/google/callback'
      });

      const { access_token, refresh_token, user, is_new_user } = response;

      // Store tokens
      const storage = sessionStorage; // Use sessionStorage for multi-tab support
      storage.setItem('accessToken', access_token);
      storage.setItem('refreshToken', refresh_token);

      // Clean up OAuth state
      sessionStorage.removeItem('google_oauth_state');

      return {
        success: true,
        user,
        isNewUser: is_new_user
      };
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to complete Google login');
      sessionStorage.removeItem('google_oauth_state');
      return {
        success: false,
        error: err.response?.data?.detail || 'Google login failed'
      };
    } finally {
      setLoading(false);
    }
  };

  return {
    initiateGoogleLogin,
    handleGoogleCallback,
    loading,
    error
  };
};

export default useGoogleAuth;
