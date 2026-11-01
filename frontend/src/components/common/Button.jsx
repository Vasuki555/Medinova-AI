/**
 * Button Component
 * Reusable button with multiple variants and states
 */

import { Loader2 } from 'lucide-react';

const Button = ({
  children,
  type = 'button',
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  icon: Icon,
  iconPosition = 'left',
  fullWidth = false,
  className = '',
  onClick,
  ...props
}) => {
  const baseClasses = 'font-semibold rounded-xl transition-all duration-200 focus:outline-none focus:ring-4 disabled:opacity-50 disabled:cursor-not-allowed inline-flex items-center justify-center gap-2';

  const variantClasses = {
    primary: 'bg-primary-600 text-white shadow-lg shadow-primary-500/30 hover:bg-primary-700 hover:scale-[1.02] active:scale-[0.98] focus:ring-primary-200',
    secondary: 'bg-transparent border-2 border-gray-300 text-gray-700 hover:bg-gray-50 hover:border-gray-400 active:bg-gray-100 focus:ring-gray-200',
    ghost: 'bg-transparent text-primary-600 hover:bg-primary-50 active:bg-primary-100 focus:ring-primary-100',
    success: 'bg-success-600 text-white shadow-lg shadow-success-500/20 hover:bg-success-700 focus:ring-success-200',
    danger: 'bg-danger-600 text-white shadow-lg shadow-danger-500/20 hover:bg-danger-700 focus:ring-danger-200',
    glass: 'bg-white/20 backdrop-blur-md text-white border border-white/30 shadow-xl hover:bg-white/30',
  };

  const sizeClasses = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-2.5 text-base',
    lg: 'px-8 py-3 text-lg',
    xl: 'px-10 py-4 text-xl',
  };

  const widthClass = fullWidth ? 'w-full' : '';

  const combinedClasses = `
    ${baseClasses}
    ${variantClasses[variant]}
    ${sizeClasses[size]}
    ${widthClass}
    ${className}
  `;

  return (
    <button
      type={type}
      disabled={disabled || loading}
      onClick={onClick}
      className={combinedClasses}
      {...props}
    >
      {loading && <Loader2 className="w-5 h-5 animate-spin" />}
      
      {!loading && Icon && iconPosition === 'left' && <Icon className="w-5 h-5" />}
      
      {children}
      
      {!loading && Icon && iconPosition === 'right' && <Icon className="w-5 h-5" />}
    </button>
  );
};

export default Button;
