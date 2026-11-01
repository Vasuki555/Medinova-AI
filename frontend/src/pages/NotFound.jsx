/**
 * 404 Not Found Page
 * Displayed when user navigates to a non-existent route
 */

import { Link, useNavigate } from 'react-router-dom';
import { FileQuestion, Home, ArrowLeft, Search } from 'lucide-react';
import Button from '@/components/common/Button';
import { useAuth } from '@/context/AuthContext';

const NotFound = () => {
  const navigate = useNavigate();
  const { isAuthenticated, user } = useAuth();

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

  const quickLinks = [
    { name: 'Home', path: '/' },
    { name: 'About Us', path: '/about' },
    { name: 'Contact', path: '/contact' },
    { name: 'FAQ', path: '/faq' },
  ];

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12 bg-gradient-to-br from-gray-50 to-primary-50">
      <div className="max-w-2xl w-full text-center">
        {/* Icon */}
        <div className="w-24 h-24 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-8 animate-bounce">
          <FileQuestion className="w-12 h-12 text-primary-600" />
        </div>

        {/* Error Code */}
        <div className="text-9xl font-bold text-primary-600 mb-4 animate-pulse">
          404
        </div>

        {/* Heading */}
        <h1 className="text-4xl font-bold font-heading text-gray-900 mb-4">
          Page Not Found
        </h1>

        {/* Description */}
        <p className="text-lg text-gray-600 mb-8 max-w-md mx-auto">
          Oops! The page you're looking for doesn't exist. It might have been moved or deleted.
        </p>

        {/* Search Box (UI Only) */}
        <div className="max-w-md mx-auto mb-8">
          <div className="relative">
            <input
              type="text"
              placeholder="Search for a page..."
              className="w-full px-4 py-3 pl-12 rounded-xl border-2 border-gray-300 focus:border-primary-500 focus:ring-4 focus:ring-primary-200 focus:outline-none transition-all duration-200"
              disabled
            />
            <Search className="w-5 h-5 text-gray-400 absolute left-4 top-1/2 -translate-y-1/2" />
          </div>
          <p className="text-xs text-gray-500 mt-2">
            Search functionality coming soon
          </p>
        </div>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
          <Button
            variant="secondary"
            onClick={() => navigate(-1)}
            icon={ArrowLeft}
          >
            Go Back
          </Button>

          {isAuthenticated ? (
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

        {/* Quick Links */}
        <div className="bg-white/70 backdrop-blur-xl border border-white/30 rounded-2xl p-6 max-w-md mx-auto">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Quick Links
          </h3>
          <div className="grid grid-cols-2 gap-3">
            {quickLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className="text-sm text-primary-600 hover:text-primary-700 hover:underline font-medium"
              >
                {link.name}
              </Link>
            ))}
          </div>
        </div>

        {/* Help Text */}
        <p className="text-sm text-gray-500 mt-8">
          Need help?{' '}
          <Link to="/contact" className="text-primary-600 hover:underline font-semibold">
            Contact our support team
          </Link>
        </p>
      </div>
    </div>
  );
};

export default NotFound;
