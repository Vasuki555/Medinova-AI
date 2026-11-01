/**
 * API Service
 * Axios configuration and API utilities.
 *
 * MULTI-TAB SUPPORT:
 * The request interceptor now checks both sessionStorage (for multi-tab mode)
 * and localStorage (for single-session mode) for 'accessToken'.
 * This matches the storage strategy used in AuthContext.
 */

import axios from 'axios';
import { API_BASE_URL, API_TIMEOUT, API_UPLOAD_TIMEOUT } from '@/utils/constants';

// Helper to get token from appropriate storage
const getToken = () => {
  const multiTabEnabled = localStorage.getItem('multiTabEnabled') !== 'false';
  const storage = multiTabEnabled ? sessionStorage : localStorage;
  return storage.getItem('accessToken');
};

// Helper to clear tokens from appropriate storage
const clearTokens = () => {
  const multiTabEnabled = localStorage.getItem('multiTabEnabled') !== 'false';
  const storage = multiTabEnabled ? sessionStorage : localStorage;
  storage.removeItem('accessToken');
  storage.removeItem('refreshToken');
};

// Create axios instance with base configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ── Request interceptor ──────────────────────────────────────────────────────
api.interceptors.request.use(
  (config) => {
    // Read token using the helper that checks appropriate storage
    const token = getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    // Only log in development mode
    if (import.meta.env.DEV) {
      console.log('API Request:', {
        method: config.method?.toUpperCase(),
        url: config.url,
        data: config.data,
      });
    }

    return config;
  },
  (error) => {
    if (import.meta.env.DEV) {
      console.error('Request Error:', error);
    }
    return Promise.reject(error);
  }
);

// ── Response interceptor ─────────────────────────────────────────────────────
api.interceptors.response.use(
  (response) => {
    // Only log in development mode
    if (import.meta.env.DEV) {
      console.log('API Response:', {
        url: response.config.url,
        status: response.status,
        data: response.data,
      });
    }
    // Unwrap: callers receive the JSON body directly
    return response.data;
  },
  (error) => {
    if (error.response) {
      // Enhanced error logging only in development
      if (import.meta.env.DEV) {
        console.error('Response Error:', {
          status: error.response.status,
          message: error.response.data?.detail || error.response.data?.message || error.message,
          url: error.config?.url,
        });
      }

      // 401 from any route except /auth/* → clear session and go to login
      const isAuthRoute = error.config?.url?.includes('/auth/');
      if (error.response.status === 401 && !isAuthRoute) {
        clearTokens();
        // Avoid redirect loop — only redirect if not already on /login
        if (!window.location.pathname.includes('/login')) {
          window.location.href = '/login';
        }
      }
    } else if (error.request) {
      // Network error - backend may not be running
      if (import.meta.env.DEV) {
        console.error('Network Error — backend may not be running:', error.message);
      }
      // Provide user-friendly error message
      error.userMessage = 'Network error. Please check your internet connection or try again later.';
    } else {
      if (import.meta.env.DEV) {
        console.error('Request Setup Error:', error.message);
      }
      error.userMessage = 'An unexpected error occurred. Please try again.';
    }

    return Promise.reject(error);
  }
);

// ── Convenience methods ───────────────────────────────────────────────────────
export const apiService = {
  /** GET request — returns unwrapped JSON body */
  get: (url, config = {}) => api.get(url, config),

  /** POST request — returns unwrapped JSON body */
  post: (url, data = {}, config = {}) => api.post(url, data, config),

  /** PUT request — returns unwrapped JSON body */
  put: (url, data = {}, config = {}) => api.put(url, data, config),

  /** PATCH request — returns unwrapped JSON body */
  patch: (url, data = {}, config = {}) => api.patch(url, data, config),

  /** DELETE request — returns unwrapped JSON body */
  delete: (url, config = {}) => api.delete(url, config),

  /**
   * Upload file using multipart/form-data
   * @param {string} url - endpoint URL
   * @param {FormData} formData - FormData object containing the file
   * @param {function} onProgress - optional upload progress callback (0-100)
   */
  upload: (url, formData, onProgress) =>
    api.post(url, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: API_UPLOAD_TIMEOUT, // Use longer timeout for uploads
      onUploadProgress: onProgress
        ? (e) => onProgress(Math.round((e.loaded * 100) / (e.total || 1)))
        : undefined,
    }),

  /**
   * AI request with extended timeout
   * @param {string} url - endpoint URL
   * @param {object} data - request body
   */
  ai: (url, data = {}) =>
    api.post(url, data, {
      timeout: API_UPLOAD_TIMEOUT, // Use longer timeout for AI processing
    }),
};

// Health check helper
export const healthAPI = {
  check: () => apiService.get('/health'),
};

export default api;
