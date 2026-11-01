/**
 * Authentication Context
 * Manages authentication state across the application.
 * Provides login, register, logout, and user state management.
 *
 * MULTI-TAB SUPPORT:
 * Uses sessionStorage (tab-specific) for auth tokens instead of localStorage.
 * This allows different user accounts to be logged in simultaneously in different tabs.
 * Each tab maintains its own independent session.
 *
 * KEY FIX: All storage keys use consistent camelCase names:
 *   - 'accessToken'  (was sometimes 'access_token' in constants.js)
 *   - 'refreshToken' (was sometimes 'refresh_token' in constants.js)
 * The api.js request interceptor also reads 'accessToken' so all
 * API calls will automatically include the Authorization header.
 */

import { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { API_BASE_URL } from '@/utils/constants';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Helper to determine storage type based on multi-tab preference
const getStorage = () => {
  // Check if user wants multi-tab support (can be toggled via localStorage preference)
  const multiTabEnabled = localStorage.getItem('multiTabEnabled') !== 'false';
  return multiTabEnabled ? sessionStorage : localStorage;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [multiTabMode, setMultiTabMode] = useState(localStorage.getItem('multiTabEnabled') !== 'false');
  const navigate = useNavigate();

  // Redirect helper based on role
  const redirectByRole = (role) => {
    if (role === 'admin') navigate('/admin/dashboard');
    else if (role === 'doctor') navigate('/doctor/dashboard');
    else navigate('/patient/dashboard');
  };

  // Restore session from stored token on mount
  useEffect(() => {
    const initializeAuth = async () => {
      const storage = getStorage();
      const token = storage.getItem('accessToken');

      if (token) {
        try {
          const response = await axios.get(`${API_BASE_URL}/auth/me`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          // axios returns the full response; .data is the JSON body
          setUser(response.data);
          setIsAuthenticated(true);
        } catch (error) {
          // Token is invalid or expired — clear stored credentials
          storage.removeItem('accessToken');
          storage.removeItem('refreshToken');
          setUser(null);
          setIsAuthenticated(false);
        }
      }

      setLoading(false);
    };

    initializeAuth();
  }, []);

  // Register new user
  const register = async (userData) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/register`, userData);
      const { access_token, refresh_token, user: userDataResponse } = response.data;

      // Store tokens with consistent camelCase keys (uses sessionStorage for multi-tab)
      const storage = getStorage();
      storage.setItem('accessToken', access_token);
      storage.setItem('refreshToken', refresh_token);

      setUser(userDataResponse);
      setIsAuthenticated(true);

      // Navigate to role-specific dashboard
      redirectByRole(userDataResponse.role);

      return { success: true, user: userDataResponse };
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail || 'Registration failed. Please try again.';
      return { success: false, error: errorMessage };
    }
  };

  // Login existing user
  const login = async (credentials) => {
    if (import.meta.env.DEV) {
      console.log('🔐 Login attempt:', credentials.email);
      console.log('🌐 API URL:', `${API_BASE_URL}/auth/login`);
    }
    
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/login`, credentials);
      if (import.meta.env.DEV) {
        console.log('✅ Login response received:', response.data);
      }
      
      const { access_token, refresh_token, user: userDataResponse } = response.data;

      // Store tokens with consistent camelCase keys (uses sessionStorage for multi-tab)
      const storage = getStorage();
      storage.setItem('accessToken', access_token);
      storage.setItem('refreshToken', refresh_token);

      setUser(userDataResponse);
      setIsAuthenticated(true);

      // Navigate to role-specific dashboard
      redirectByRole(userDataResponse.role);

      return { success: true, user: userDataResponse };
    } catch (error) {
      if (import.meta.env.DEV) {
        console.error('❌ Login error:', error);
        console.error('❌ Error response:', error.response?.data);
        console.error('❌ Error status:', error.response?.status);
      }
      
      const errorMessage =
        error.response?.data?.detail || 'Login failed. Please check your credentials.';
      return { success: false, error: errorMessage };
    }
  };

  // Logout and clear all credentials
  const logout = () => {
    const storage = getStorage();
    storage.removeItem('accessToken');
    storage.removeItem('refreshToken');
    setUser(null);
    setIsAuthenticated(false);
    navigate('/login');
  };

  // Toggle multi-tab mode
  const toggleMultiTabMode = (enabled) => {
    localStorage.setItem('multiTabEnabled', enabled.toString());
    setMultiTabMode(enabled);
    // Note: User needs to refresh/re-login for this to take full effect
  };

  // Update partial user data in context
  const updateUser = (userData) => {
    setUser((prevUser) => ({ ...prevUser, ...userData }));
  };

  // Role helpers
  const hasRole = (role) => user?.role === role;
  const hasAnyRole = (roles) => roles.includes(user?.role);

  const value = {
    user,
    loading,
    isAuthenticated,
    multiTabMode,
    register,
    login,
    logout,
    updateUser,
    hasRole,
    hasAnyRole,
    toggleMultiTabMode,
    setUser,
    setIsAuthenticated,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthContext;
