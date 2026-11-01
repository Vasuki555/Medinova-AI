/**
 * Toast Context
 * Provides visual toast feedback to users with premium animations and glassmorphism.
 */

import { createContext, useContext, useState, useCallback } from 'react';
import { AlertCircle, CheckCircle, Info, X, AlertTriangle } from 'lucide-react';

const ToastContext = createContext(null);

export const useToast = () => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
};

export const ToastProvider = ({ children }) => {
  const [toasts, setToasts] = useState([]);

  const showToast = useCallback((message, type = 'info', duration = 4000) => {
    const id = Date.now().toString();
    setToasts((prev) => [...prev, { id, message, type, duration }]);
    
    setTimeout(() => {
      removeToast(id);
    }, duration);
  }, []);

  const removeToast = useCallback((id) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  }, []);

  const getIcon = (type) => {
    switch (type) {
      case 'success':
        return <CheckCircle className="w-5 h-5 text-emerald-500" />;
      case 'error':
        return <AlertCircle className="w-5 h-5 text-rose-500" />;
      case 'warning':
        return <AlertTriangle className="w-5 h-5 text-amber-500" />;
      default:
        return <Info className="w-5 h-5 text-sky-500" />;
    }
  };

  const getColorClasses = (type) => {
    // Premium Glassmorphism styling matching the theme
    switch (type) {
      case 'success':
        return 'bg-emerald-950/45 text-emerald-100 border-emerald-500/30';
      case 'error':
        return 'bg-rose-950/45 text-rose-100 border-rose-500/30';
      case 'warning':
        return 'bg-amber-950/45 text-amber-100 border-amber-500/30';
      default:
        return 'bg-sky-950/45 text-sky-100 border-sky-500/30';
    }
  };

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      
      {/* Toast container overlay */}
      <div className="fixed top-6 right-6 z-[9999] flex flex-col gap-3 w-full max-w-sm pointer-events-none">
        {toasts.map((toast) => (
          <div
            key={toast.id}
            className={`flex items-start gap-3 p-4 rounded-2xl border backdrop-blur-lg shadow-2xl pointer-events-auto transition-all duration-300 transform animate-slide-in-right ${getColorClasses(
              toast.type
            )}`}
          >
            <div className="flex-shrink-0 mt-0.5">{getIcon(toast.type)}</div>
            <div className="flex-grow text-sm font-medium tracking-wide">{toast.message}</div>
            <button
              onClick={() => removeToast(toast.id)}
              className="flex-shrink-0 p-1 hover:bg-white/10 rounded-lg transition-colors text-white/50 hover:text-white"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
};

export default ToastContext;
