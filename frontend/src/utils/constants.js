/**
 * Application Constants
 * Centralized configuration values
 */

// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
export const API_TIMEOUT = import.meta.env.VITE_API_TIMEOUT || 60000; // 60 seconds for general requests
export const API_UPLOAD_TIMEOUT = 180000; // 3 minutes for file uploads and AI processing

// Application Info
export const APP_NAME = import.meta.env.VITE_APP_NAME || 'MediNova AI';
export const APP_VERSION = import.meta.env.VITE_APP_VERSION || '1.0.0';
export const ENVIRONMENT = import.meta.env.VITE_ENVIRONMENT || 'development';

// Routes
export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  DASHBOARD: '/dashboard',
  PROFILE: '/profile',
  APPOINTMENTS: '/appointments',
  SYMPTOM_CHECKER: '/symptom-checker',
  DOCUMENTS: '/documents',
  HEALTH_RECORDS: '/health-records',
};

// User Roles
export const USER_ROLES = {
  PATIENT: 'patient',
  DOCTOR: 'doctor',
  ADMIN: 'admin',
};

// Storage Keys — must match what AuthContext.jsx and api.js use
export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'accessToken',
  REFRESH_TOKEN: 'refreshToken',
  USER_DATA: 'userData',
};

// API Endpoints
export const API_ENDPOINTS = {
  HEALTH: '/health',
  // Future endpoints will be added here
};

// Date Formats
export const DATE_FORMATS = {
  DISPLAY: 'MMM DD, YYYY',
  DISPLAY_WITH_TIME: 'MMM DD, YYYY HH:mm',
  API: 'YYYY-MM-DD',
  API_WITH_TIME: 'YYYY-MM-DDTHH:mm:ss',
};

// Pagination
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 10,
  PAGE_SIZE_OPTIONS: [10, 20, 50, 100],
};

// File Upload
export const FILE_UPLOAD = {
  MAX_SIZE: 10 * 1024 * 1024, // 10 MB
  ALLOWED_TYPES: ['image/jpeg', 'image/png', 'application/pdf'],
};

export default {
  API_BASE_URL,
  API_TIMEOUT,
  APP_NAME,
  APP_VERSION,
  ENVIRONMENT,
  ROUTES,
  USER_ROLES,
  STORAGE_KEYS,
  API_ENDPOINTS,
  DATE_FORMATS,
  PAGINATION,
  FILE_UPLOAD,
};
