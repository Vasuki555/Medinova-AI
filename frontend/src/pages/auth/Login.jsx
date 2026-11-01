/**
 * Login Page
 * Allows existing users to authenticate and access their accounts
 */

import { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Mail, Lock, Heart, ChevronLeft, ArrowRight } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { useGoogleAuth } from '@/hooks/useGoogleAuth';
import Input from '@/components/common/Input';
import Button from '@/components/common/Button';
import Toast from '@/components/common/Toast';
import { validateLoginForm } from '@/utils/validation';

const Login = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();
  const { initiateGoogleLogin, loading: googleLoading } = useGoogleAuth();

  const [formData, setFormData] = useState({
    email: '',
    password: '',
    rememberMe: false,
  });

  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState(null);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
    
    // Clear error for this field
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate form
    const validation = validateLoginForm(formData);
    if (!validation.isValid) {
      setErrors(validation.errors);
      return;
    }

    setLoading(true);
    setErrors({});

    // Attempt login
    const result = await login({
      email: formData.email,
      password: formData.password,
    });

    setLoading(false);

    if (result.success) {
      setToast({ type: 'success', message: 'Login successful! Redirecting...' });
      
      // Redirect to intended location or dashboard based on role
      const from = location.state?.from?.pathname || getDashboardPath(result.user.role);
      
      setTimeout(() => {
        navigate(from, { replace: true });
      }, 1000);
    } else {
      setToast({ type: 'error', message: result.error });
    }
  };

  const getDashboardPath = (role) => {
    switch (role) {
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
    <div className="min-h-screen flex">
      {/* Left Panel - Illustration (Desktop only) */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-primary-600 via-primary-700 to-primary-800 relative overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute inset-0" style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
          }} />
        </div>

        {/* Logo */}
        <div className="absolute top-8 left-8 flex items-center space-x-3 text-white">
          <Heart className="w-10 h-10 fill-current" />
          <span className="text-xl font-bold">MediNova AI</span>
        </div>

        {/* Content */}
        <div className="relative z-10 flex flex-col justify-center p-12 text-white">
          <h1 className="text-4xl font-bold mb-6">Secure Healthcare Access</h1>
          
          <div className="space-y-4">
            <div className="flex items-start space-x-3">
              <svg className="w-6 h-6 text-success-400 flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <div>
                <p className="text-white/90 text-lg">Bank-level encryption</p>
              </div>
            </div>

            <div className="flex items-start space-x-3">
              <svg className="w-6 h-6 text-success-400 flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <div>
                <p className="text-white/90 text-lg">HIPAA compliant</p>
              </div>
            </div>

            <div className="flex items-start space-x-3">
              <svg className="w-6 h-6 text-success-400 flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <div>
                <p className="text-white/90 text-lg">24/7 secure access</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Right Panel - Login Form */}
      <div className="w-full lg:w-1/2 overflow-y-auto bg-white">
        <div className="min-h-full flex items-center justify-center px-8 py-12">
          <div className="max-w-md w-full">
            {/* Back to Home (Mobile) */}
            <Link to="/" className="lg:hidden flex items-center gap-2 text-gray-600 hover:text-primary-600 mb-8">
              <ChevronLeft className="w-5 h-5" />
              <span>Back to Home</span>
            </Link>

            {/* Logo (Mobile) */}
            <div className="lg:hidden flex items-center justify-center space-x-3 mb-8">
              <Heart className="w-10 h-10 text-primary-600 fill-current" />
              <span className="text-xl font-bold text-gray-900">MediNova AI</span>
            </div>

            {/* Header */}
            <div className="mb-8">
              <h2 className="text-3xl lg:text-4xl font-bold font-heading text-gray-900 mb-2">
                Welcome Back
              </h2>
              <p className="text-base text-gray-600">
                Sign in to your MediNova account
              </p>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-5">
              <Input
                label="Email Address"
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="your.email@example.com"
                icon={Mail}
                error={errors.email}
                required
              />

              <Input
                label="Password"
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="Enter your password"
                icon={Lock}
                error={errors.password}
                required
              />

              {/* Remember Me & Forgot Password */}
              <div className="flex items-center justify-between">
                <label className="flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    name="rememberMe"
                    checked={formData.rememberMe}
                    onChange={handleChange}
                    className="w-4 h-4 rounded text-primary-600 focus:ring-4 focus:ring-primary-200 border-gray-300 cursor-pointer"
                  />
                  <span className="ml-2 text-sm text-gray-700">Remember me</span>
                </label>

                <Link
                  to="/forgot-password"
                  className="text-sm font-semibold text-primary-600 hover:text-primary-700 hover:underline"
                >
                  Forgot Password?
                </Link>
              </div>

              {/* Sign In Button */}
              <Button
                type="submit"
                variant="primary"
                fullWidth
                loading={loading}
                icon={ArrowRight}
                iconPosition="right"
              >
                {loading ? 'Signing in...' : 'Sign In'}
              </Button>
            </form>

            {/* Divider */}
            <div className="relative my-6">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="bg-white px-4 text-gray-500">or continue with</span>
              </div>
            </div>

            {/* Google Sign In */}
            <Button
              type="button"
              variant="secondary"
              fullWidth
              onClick={initiateGoogleLogin}
              disabled={googleLoading}
              loading={googleLoading}
            >
              <svg className="w-5 h-5" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
              {googleLoading ? 'Connecting to Google...' : 'Sign in with Google'}
            </Button>

            {/* Sign Up Link */}
            <div className="mt-8 text-center">
              <p className="text-sm text-gray-600">
                Don't have an account?{' '}
                <Link
                  to="/register"
                  className="font-semibold text-primary-600 hover:text-primary-700 hover:underline"
                >
                  Sign Up
                </Link>
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Toast Notifications */}
      {toast && (
        <Toast
          type={toast.type}
          message={toast.message}
          onClose={() => setToast(null)}
        />
      )}
    </div>
  );
};

export default Login;
