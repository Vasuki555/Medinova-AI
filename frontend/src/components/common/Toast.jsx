/**
 * Toast Component
 * Displays temporary notification messages
 */

import { useEffect } from 'react';
import { CheckCircle, XCircle, AlertCircle, Info, X } from 'lucide-react';

const Toast = ({ type = 'info', message, onClose, duration = 5000 }) => {
  useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(() => {
        onClose();
      }, duration);

      return () => clearTimeout(timer);
    }
  }, [duration, onClose]);

  const icons = {
    success: <CheckCircle className="w-5 h-5" />,
    error: <XCircle className="w-5 h-5" />,
    warning: <AlertCircle className="w-5 h-5" />,
    info: <Info className="w-5 h-5" />,
  };

  const styles = {
    success: 'bg-success-50 border-success-500 text-success-800',
    error: 'bg-danger-50 border-danger-500 text-danger-800',
    warning: 'bg-warning-50 border-warning-500 text-warning-800',
    info: 'bg-info-50 border-info-500 text-info-800',
  };

  return (
    <div
      className={`
        fixed top-4 right-4 z-50 max-w-md w-full
        ${styles[type]}
        border-l-4 rounded-xl shadow-xl p-4
        animate-slide-in-right
      `}
    >
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0">
          {icons[type]}
        </div>
        
        <div className="flex-1">
          <p className="text-sm font-medium">{message}</p>
        </div>

        <button
          onClick={onClose}
          className="flex-shrink-0 text-current hover:opacity-70 transition-opacity"
        >
          <X className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
};

export default Toast;
