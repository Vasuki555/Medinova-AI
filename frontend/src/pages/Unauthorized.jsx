/**
 * Unauthorized Page
 * Displayed when user tries to access a resource they don't have permission for
 */

import { Link, useNavigate } from 'react-router-dom';
import { ShieldAlert, Home, ArrowLeft } from 'lucide-react';
import Button from '@/components/common/Button';
import { useAuth } from '@/context/AuthContext';

const Unauthorized = () => {
  const navigate = useNavigate();
  const { user } = useAuth();

  const getDashboardPath = () => {
    switch (user?.role) {
      case 'patient':
        return '/patient/dashboard';
      case 'doctor':
        return '/doctor/dashboard';
      case 'admin':
        return '/admin/dashboard';
      default:
        return '/';
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12 bg-gradient-to-br from-gray-50 to-danger-50">
      <div className="max-w-lg w-full text-center">
        {/* Icon */}
        <div className="w-24 h-24 bg-danger-100 rounded-full flex items-center justify-center mx-auto mb-8">
          <ShieldAlert className="w-12 h-12 text-danger-600" />
        </div>

        {/* Error Code */}
        <div className="text-8xl font-bold text-danger-600 mb-4">
          403
        </div>

        {/* Heading */}
        <h1 className="text-4xl font-bold font-heading text-gray-900 mb-4">
          Access Denied
        </h1>

        {/* Description */}
        <p className="text-lg text-gray-600 mb-8 max-w-md mx-auto">
          You don't have permission to access this page. This area is restricted to authorized users only.
        </p>

        {/* User Info */}
        {user && (
          <div className="bg-white/70 backdrop-blur-xl border border-white/30 rounded-xl p-4 mb-8 max-w-sm mx-auto">
            <p className="text-sm text-gray-600 mb-1">Logged in as:</p>
            <p className="text-base font-semibold text-gray-900">
              {user.first_name} {user.last_name}
            </p>
            <p className="text-sm text-gray-500 capitalize">
              {user.role} Account
            </p>
          </div>
        )}

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button
            variant="secondary"
            onClick={() => navigate(-1)}
            icon={ArrowLeft}
          >
            Go Back
          </Button>

          {user ? (
            <Link to={getDashboardPath()}>
              <Button
                variant="primary"
                icon={Home}
              >
                Go to Dashboard
              </Button>
            </Link>
          ) : (
            <Link to="/">
              <Button
                variant="primary"
                icon={Home}
              >
                Go to Home
              </Button>
            </Link>
          )}
        </div>

        {/* Help Text */}
        <p className="text-sm text-gray-500 mt-8">
          If you believe this is an error, please{' '}
          <Link to="/contact" className="text-primary-600 hover:underline font-semibold">
            contact support
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Unauthorized;
