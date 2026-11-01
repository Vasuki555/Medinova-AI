/**
 * Input Component
 * Reusable input field with label, error handling, and icons
 */

import { useState } from 'react';
import { Eye, EyeOff, AlertCircle, CheckCircle } from 'lucide-react';

const Input = ({
  label,
  type = 'text',
  name,
  value,
  onChange,
  onBlur,
  placeholder,
  error,
  success,
  required = false,
  disabled = false,
  icon: Icon,
  className = '',
  helperText = '',
}) => {
  const [showPassword, setShowPassword] = useState(false);
  const isPassword = type === 'password';
  const inputType = isPassword && showPassword ? 'text' : type;

  return (
    <div className={`mb-5 ${className}`}>
      {label && (
        <label htmlFor={name} className="block text-sm font-medium text-gray-700 mb-2">
          {label}
          {required && <span className="text-danger-500 ml-1">*</span>}
        </label>
      )}

      <div className="relative">
        {Icon && (
          <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">
            <Icon className="w-5 h-5" />
          </div>
        )}

        <input
          id={name}
          name={name}
          type={inputType}
          value={value}
          onChange={onChange}
          onBlur={onBlur}
          placeholder={placeholder}
          disabled={disabled}
          className={`
            w-full px-4 py-3 rounded-xl border-2 
            text-gray-900 placeholder-gray-400 bg-white
            focus:outline-none transition-all duration-200
            disabled:bg-gray-100 disabled:cursor-not-allowed
            ${Icon ? 'pl-12' : ''}
            ${isPassword ? 'pr-12' : ''}
            ${error 
              ? 'border-danger-500 focus:border-danger-500 focus:ring-4 focus:ring-danger-200' 
              : success
              ? 'border-success-500 focus:border-success-500 focus:ring-4 focus:ring-success-200'
              : 'border-gray-300 focus:border-primary-500 focus:ring-4 focus:ring-primary-200'
            }
          `}
        />

        {isPassword && (
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 focus:outline-none"
            tabIndex={-1}
          >
            {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
          </button>
        )}

        {success && !isPassword && (
          <div className="absolute right-4 top-1/2 -translate-y-1/2 text-success-600">
            <CheckCircle className="w-5 h-5" />
          </div>
        )}
      </div>

      {helperText && !error && !success && (
        <p className="text-xs text-gray-500 mt-1.5 flex items-center">
          {helperText}
        </p>
      )}

      {error && (
        <p className="text-xs text-danger-600 mt-1.5 flex items-center">
          <AlertCircle className="w-4 h-4 mr-1" />
          {error}
        </p>
      )}

      {success && (
        <p className="text-xs text-success-600 mt-1.5 flex items-center">
          <CheckCircle className="w-4 h-4 mr-1" />
          {success}
        </p>
      )}
    </div>
  );
};

export default Input;
