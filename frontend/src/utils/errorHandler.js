/**
 * Error Handling Utilities
 * Centralized error handling and user-friendly error messages
 */

/**
 * Extract user-friendly error message from API error
 * @param {Error} error - Error object from API call
 * @returns {string} - User-friendly error message
 */
export const getErrorMessage = (error) => {
  // Check if error has userMessage (set by axios interceptor)
  if (error.userMessage) {
    return error.userMessage;
  }

  // Check for API error response
  if (error.response) {
    const { status, data } = error.response;

    // Handle specific status codes
    switch (status) {
      case 400:
        return data?.detail || 'Invalid request. Please check your input.';
      case 401:
        return 'Session expired. Please log in again.';
      case 403:
        return data?.detail || 'Access denied. You do not have permission to perform this action.';
      case 404:
        return data?.detail || 'The requested resource was not found.';
      case 409:
        return data?.detail || 'This operation conflicts with existing data.';
      case 422:
        // Validation errors from Pydantic
        if (data?.detail && Array.isArray(data.detail)) {
          const errors = data.detail.map((err) => err.msg || err.message).join(', ');
          return `Validation error: ${errors}`;
        }
        return data?.detail || 'Validation error. Please check your input.';
      case 429:
        return 'Too many requests. Please slow down and try again in a few moments.';
      case 500:
        return 'Server error. Please try again later.';
      case 503:
        return 'Service temporarily unavailable. Please try again later.';
      default:
        return data?.detail || data?.message || 'An error occurred. Please try again.';
    }
  }

  // Network errors
  if (error.request) {
    return 'Network error. Please check your internet connection.';
  }

  // Generic error fallback
  return error.message || 'An unexpected error occurred. Please try again.';
};

/**
 * Handle async operation with try-catch and return result/error
 * @param {Promise} promise - Async function to execute
 * @returns {Promise<{success: boolean, data?: any, error?: string}>}
 */
export const handleAsync = async (promise) => {
  try {
    const data = await promise;
    return { success: true, data };
  } catch (error) {
    const errorMessage = getErrorMessage(error);
    return { success: false, error: errorMessage };
  }
};

/**
 * Log error to console in development mode
 * @param {string} context - Context where error occurred
 * @param {Error} error - Error object
 */
export const logError = (context, error) => {
  if (import.meta.env.DEV) {
    console.error(`[${context}] Error:`, error);
    if (error.response) {
      console.error('Response data:', error.response.data);
      console.error('Response status:', error.response.status);
    }
  }
};

/**
 * Format validation errors from Pydantic
 * @param {Array} errors - Array of validation errors
 * @returns {Object} - Object with field names as keys and error messages as values
 */
export const formatValidationErrors = (errors) => {
  if (!Array.isArray(errors)) return {};

  const formatted = {};
  errors.forEach((error) => {
    const field = error.loc ? error.loc[error.loc.length - 1] : 'unknown';
    formatted[field] = error.msg || error.message || 'Invalid value';
  });
  return formatted;
};

/**
 * Check if error is a network error
 * @param {Error} error - Error object
 * @returns {boolean}
 */
export const isNetworkError = (error) => {
  return !error.response && error.request;
};

/**
 * Check if error is an authentication error
 * @param {Error} error - Error object
 * @returns {boolean}
 */
export const isAuthError = (error) => {
  return error.response && (error.response.status === 401 || error.response.status === 403);
};

/**
 * Check if error is a validation error
 * @param {Error} error - Error object
 * @returns {boolean}
 */
export const isValidationError = (error) => {
  return error.response && (error.response.status === 400 || error.response.status === 422);
};

/**
 * Retry an async operation with exponential backoff
 * @param {Function} fn - Async function to retry
 * @param {number} maxRetries - Maximum number of retries (default: 3)
 * @param {number} delay - Initial delay in ms (default: 1000)
 * @returns {Promise}
 */
export const retryWithBackoff = async (fn, maxRetries = 3, delay = 1000) => {
  let lastError;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;

      // Don't retry on client errors (4xx)
      if (error.response && error.response.status >= 400 && error.response.status < 500) {
        throw error;
      }

      // Don't retry on last attempt
      if (attempt === maxRetries) {
        throw error;
      }

      // Wait before retrying (exponential backoff)
      const waitTime = delay * Math.pow(2, attempt);
      if (import.meta.env.DEV) {
        console.log(`Retry attempt ${attempt + 1}/${maxRetries} after ${waitTime}ms`);
      }
      await new Promise((resolve) => setTimeout(resolve, waitTime));
    }
  }

  throw lastError;
};

export default {
  getErrorMessage,
  handleAsync,
  logError,
  formatValidationErrors,
  isNetworkError,
  isAuthError,
  isValidationError,
  retryWithBackoff,
};
