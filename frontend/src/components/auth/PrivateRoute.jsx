/**
 * Private Route Component
 * Protects routes that require authentication
 * Redirects to login if user is not authenticated
 */

import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';

const PrivateRoute = ({ children, roles = [] }) => {
  const { isAuthenticated, user, loading } = useAuth();
  const location = useLocation();

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

  // Redirect to login if not authenticated
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Check role-based access
  if (roles.length > 0 && !roles.includes(user?.role)) {
    return <Navigate to="/unauthorized" replace />;
  }

  return children;
};

export default PrivateRoute;
