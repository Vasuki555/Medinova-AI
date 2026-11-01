/**
 * Public Route Component
 * Redirects authenticated users away from auth pages (login, register)
 * Prevents authenticated users from accessing login/register pages
 */

import { Navigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';

const PublicRoute = ({ children }) => {
  const { isAuthenticated, user, loading } = useAuth();

  // Show loading state while checking authentication
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  // Redirect authenticated users to their respective dashboards
  if (isAuthenticated) {
    switch (user?.role) {
      case 'patient':
        return <Navigate to="/patient/dashboard" replace />;
      case 'doctor':
        return <Navigate to="/doctor/dashboard" replace />;
      case 'admin':
        return <Navigate to="/admin/dashboard" replace />;
      default:
        return <Navigate to="/" replace />;
    }
  }

  return children;
};

export default PublicRoute;
