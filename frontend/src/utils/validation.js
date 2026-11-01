/**
 * Validation Utilities
 * Functions for form validation
 */

// Email validation
export const validateEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// Password validation
export const validatePassword = (password) => {
  const checks = {
    minLength: password.length >= 8,
    hasUppercase: /[A-Z]/.test(password),
    hasLowercase: /[a-z]/.test(password),
    hasNumber: /\d/.test(password),
    hasSpecialChar: /[!@#$%^&*(),.?":{}|<>]/.test(password),
  };

  const isValid = Object.values(checks).every((check) => check);

  return { isValid, checks };
};

// Phone number validation (basic E.164 format)
export const validatePhone = (phone) => {
  // Remove spaces and dashes
  const cleanPhone = phone.replace(/[\s-]/g, '');
  
  // Check if it starts with + and has 10-15 digits
  const phoneRegex = /^\+?[1-9]\d{9,14}$/;
  return phoneRegex.test(cleanPhone);
};

// Name validation
export const validateName = (name) => {
  return name.trim().length >= 2;
};

// Confirm password validation
export const validatePasswordMatch = (password, confirmPassword) => {
  return password === confirmPassword && password.length > 0;
};

// Full form validation
export const validateRegisterForm = (formData) => {
  const errors = {};

  // First name validation
  if (!formData.first_name || !validateName(formData.first_name)) {
    errors.first_name = 'Please enter a valid first name (at least 2 characters)';
  }

  // Last name validation
  if (!formData.last_name || !validateName(formData.last_name)) {
    errors.last_name = 'Please enter a valid last name (at least 2 characters)';
  }

  // Email validation
  if (!formData.email || !validateEmail(formData.email)) {
    errors.email = 'Please enter a valid email address';
  }

  // Phone validation (optional)
  if (formData.phone && !validatePhone(formData.phone)) {
    errors.phone = 'Please enter a valid phone number (e.g., +14155552671)';
  }

  // Password validation
  const passwordCheck = validatePassword(formData.password);
  if (!passwordCheck.isValid) {
    errors.password = 'Password does not meet all requirements';
  }

  // Confirm password validation
  if (!validatePasswordMatch(formData.password, formData.confirmPassword)) {
    errors.confirmPassword = 'Passwords do not match';
  }

  // Role validation
  if (!formData.role || !['patient', 'doctor'].includes(formData.role)) {
    errors.role = 'Please select a valid account type';
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors,
  };
};

// Login form validation
export const validateLoginForm = (formData) => {
  const errors = {};

  // Email validation
  if (!formData.email || !validateEmail(formData.email)) {
    errors.email = 'Please enter a valid email address';
  }

  // Password validation (just check if not empty for login)
  if (!formData.password || formData.password.length === 0) {
    errors.password = 'Please enter your password';
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors,
  };
};

// Forgot password form validation
export const validateForgotPasswordForm = (email) => {
  if (!email || !validateEmail(email)) {
    return {
      isValid: false,
      error: 'Please enter a valid email address',
    };
  }

  return {
    isValid: true,
    error: null,
  };
};
