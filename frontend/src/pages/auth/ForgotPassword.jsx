/**
 * Forgot Password Page
 * Allows users to request password reset
 * UI Only - Backend implementation pending
 */

import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Mail, Lock, ChevronLeft, Send } from 'lucide-react';
import Input from '@/components/common/Input';
import Button from '@/components/common/Button';
import Toast from '@/components/common/Toast';
import { validateEmail } from '@/utils/validation';

const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState(null);
  const [emailSent, setEmailSent] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate email
    if (!email || !validateEmail(email)) {
      setError('Please enter a valid email address');
      return;
    }

    setLoading(true);
    setError('');

    // Simulate API call (Backend not implemented yet)
    setTimeout(() => {
      setLoading(false);
      setEmailSent(true);
      setToast({ 
        type: 'success', 
        message: 'Password reset instructions sent! Check your email.' 
      });
    }, 1500);
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12 bg-gradient-to-br from-gray-50 to-primary-50">
      {/* Back to Login Link (Top) */}
      <Link 
        to="/login" 
        className="absolute top-8 left-8 flex items-center gap-2 text-gray-600 hover:text-primary-600 font-medium transition-colors duration-200"
      >
        <ChevronLeft className="w-5 h-5" />
        <span>Back to Login</span>
      </Link>

      {/* Card Container */}
      <div className="max-w-md w-full bg-white/70 backdrop-blur-xl border border-white/30 shadow-2xl rounded-2xl p-8 lg:p-10">
        {!emailSent ? (
          <>
            {/* Icon */}
            <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <Lock className="w-8 h-8 text-primary-600" />
            </div>

            {/* Header */}
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold font-heading text-gray-900 mb-3">
                Forgot Password?
              </h2>
              <p className="text-base text-gray-600 leading-relaxed max-w-sm mx-auto">
                No worries! Enter your email address and we'll send you a verification code to reset your password.
              </p>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit}>
              <Input
                label="Email Address"
                type="email"
                name="email"
                value={email}
                onChange={(e) => {
                  setEmail(e.target.value);
                  setError('');
                }}
                placeholder="your.email@example.com"
                icon={Mail}
                error={error}
                required
              />

              <Button
                type="submit"
                variant="primary"
                fullWidth
                loading={loading}
                icon={Send}
                iconPosition="right"
              >
                {loading ? 'Sending...' : 'Send Verification Code'}
              </Button>
            </form>

            {/* Back to Login Link (Bottom) */}
            <div className="mt-6 text-center">
              <Link
                to="/login"
                className="flex items-center justify-center gap-2 text-sm font-semibold text-primary-600 hover:text-primary-700"
              >
                <ChevronLeft className="w-4 h-4" />
                <span>Back to Login</span>
              </Link>
            </div>
          </>
        ) : (
          <>
            {/* Success State */}
            <div className="w-16 h-16 bg-success-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg className="w-8 h-8 text-success-600" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            </div>

            <div className="text-center">
              <h2 className="text-3xl font-bold font-heading text-gray-900 mb-3">
                Check Your Email
              </h2>
              <p className="text-base text-gray-600 leading-relaxed mb-6">
                We've sent password reset instructions to{' '}
                <span className="font-semibold text-gray-900">{email}</span>
              </p>
              <p className="text-sm text-gray-500 mb-8">
                Didn't receive the email? Check your spam folder or{' '}
                <button
                  onClick={() => setEmailSent(false)}
                  className="text-primary-600 hover:underline font-semibold"
                >
                  try again
                </button>
              </p>

              <Link to="/login">
                <Button variant="primary" fullWidth>
                  Return to Login
                </Button>
              </Link>
            </div>
          </>
        )}
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

export default ForgotPassword;
