/**
 * Register Page
 * Allows new users to create accounts
 */

import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Mail, Lock, User, Phone, Heart, ChevronLeft, ArrowRight, Stethoscope, Check, X } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { useGoogleAuth } from '@/hooks/useGoogleAuth';
import Input from '@/components/common/Input';
import Button from '@/components/common/Button';
import Toast from '@/components/common/Toast';
import { validatePassword } from '@/utils/validation';

const Register = () => {
  const { register } = useAuth();
  const { initiateGoogleLogin, loading: googleLoading } = useGoogleAuth();

  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: '',
    role: 'patient',
    acceptedTerms: false,
  });

  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState(null);
  const [passwordChecks, setPasswordChecks] = useState({
    minLength: false,
    hasUppercase: false,
    hasLowercase: false,
    hasNumber: false,
    hasSpecialChar: false,
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    const newValue = type === 'checkbox' ? checked : value;
    
    setFormData((prev) => ({
      ...prev,
      [name]: newValue,
    }));

    // Real-time password validation
    if (name === 'password') {
      const validation = validatePassword(value);
      setPasswordChecks(validation.checks);
    }

    // Clear error for this field
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate form
    const newErrors = {};

    if (!formData.first_name.trim()) {
      newErrors.first_name = 'First name is required';
    }

    if (!formData.last_name.trim()) {
      newErrors.last_name = 'Last name is required';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    const passwordValidation = validatePassword(formData.password);
    if (!passwordValidation.isValid) {
      newErrors.password = 'Password does not meet all requirements';
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    if (!formData.acceptedTerms) {
      newErrors.acceptedTerms = 'You must accept the terms and conditions';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setLoading(true);
    setErrors({});

    // Prepare data for API
    const registrationData = {
      email: formData.email,
      password: formData.password,
      first_name: formData.first_name,
      last_name: formData.last_name,
      role: formData.role,
    };

    // Add phone if provided
    if (formData.phone.trim()) {
      registrationData.phone = formData.phone;
    }

    // Attempt registration
    const result = await register(registrationData);

    setLoading(false);

    if (result.success) {
      setToast({ type: 'success', message: 'Registration successful! Redirecting...' });
      // AuthContext.register() already navigates to the role-specific dashboard.
      // No additional navigate() needed here.
    } else {
      setToast({ type: 'error', message: result.error });
    }
  };

  const PasswordRequirement = ({ met, text }) => (
    <div className="flex items-center gap-2 text-xs">
      {met ? (
        <Check className="w-4 h-4 text-success-600" />
      ) : (
        <X className="w-4 h-4 text-gray-400" />
      )}
      <span className={met ? 'text-success-600' : 'text-gray-400'}>{text}</span>
    </div>
  );

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
          <h1 className="text-4xl font-bold mb-6">Start Your Health Journey Today</h1>
          
          <div className="space-y-4">
            {[
              'Free account forever',
              'No credit card required',
              'Set up in under 2 minutes',
              'AI-powered health insights',
              'Connect with verified doctors'
            ].map((text, index) => (
              <div key={index} className="flex items-start space-x-3">
                <svg className="w-6 h-6 text-success-400 flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                <p className="text-white/90 text-lg">{text}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Right Panel - Registration Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center px-8 py-12 bg-white overflow-y-auto">
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
              Join MediNova AI
            </h2>
            <p className="text-base text-gray-600">
              Create your account to get started
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Account Type Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                I am a <span className="text-danger-500">*</span>
              </label>
              <div className="flex gap-4">
                <label
                  className={`
                    flex-1 p-4 rounded-xl border-2 cursor-pointer transition-all duration-200
                    ${formData.role === 'patient' 
                      ? 'border-primary-600 bg-primary-50' 
                      : 'border-gray-300 hover:border-primary-300 hover:bg-primary-50'
                    }
                  `}
                >
                  <input
                    type="radio"
                    name="role"
                    value="patient"
                    checked={formData.role === 'patient'}
                    onChange={handleChange}
                    className="sr-only"
                  />
                  <div className="flex items-center gap-3">
                    <User className={`w-6 h-6 ${formData.role === 'patient' ? 'text-primary-600' : 'text-gray-400'}`} />
                    <div>
                      <div className={`font-semibold ${formData.role === 'patient' ? 'text-primary-600' : 'text-gray-700'}`}>
                        Patient
                      </div>
                      <div className="text-xs text-gray-500">Personal account</div>
                    </div>
                  </div>
                </label>

                <label
                  className={`
                    flex-1 p-4 rounded-xl border-2 cursor-pointer transition-all duration-200
                    ${formData.role === 'doctor' 
                      ? 'border-primary-600 bg-primary-50' 
                      : 'border-gray-300 hover:border-primary-300 hover:bg-primary-50'
                    }
                  `}
                >
                  <input
                    type="radio"
                    name="role"
                    value="doctor"
                    checked={formData.role === 'doctor'}
                    onChange={handleChange}
                    className="sr-only"
                  />
                  <div className="flex items-center gap-3">
                    <Stethoscope className={`w-6 h-6 ${formData.role === 'doctor' ? 'text-primary-600' : 'text-gray-400'}`} />
                    <div>
                      <div className={`font-semibold ${formData.role === 'doctor' ? 'text-primary-600' : 'text-gray-700'}`}>
                        Doctor
                      </div>
                      <div className="text-xs text-gray-500">Professional account</div>
                    </div>
                  </div>
                </label>
              </div>
            </div>

            {/* Name Fields */}
            <div className="grid grid-cols-2 gap-4">
              <Input
                label="First Name"
                type="text"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
                placeholder="John"
                error={errors.first_name}
                required
                className="mb-0"
              />

              <Input
                label="Last Name"
                type="text"
                name="last_name"
                value={formData.last_name}
                onChange={handleChange}
                placeholder="Doe"
                error={errors.last_name}
                required
                className="mb-0"
              />
            </div>

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
              label="Phone Number"
              type="tel"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              placeholder="+1 (555) 000-0000"
              icon={Phone}
              error={errors.phone}
              helperText="Optional - E.164 format (e.g., +14155552671)"
            />

            <div>
              <Input
                label="Password"
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="Create a strong password"
                icon={Lock}
                error={errors.password}
                required
                className="mb-2"
              />
              
              {/* Password Requirements */}
              <div className="space-y-1 mt-2">
                <PasswordRequirement met={passwordChecks.minLength} text="At least 8 characters" />
                <PasswordRequirement met={passwordChecks.hasUppercase} text="Contains uppercase letter" />
                <PasswordRequirement met={passwordChecks.hasLowercase} text="Contains lowercase letter" />
                <PasswordRequirement met={passwordChecks.hasNumber} text="Contains number" />
                <PasswordRequirement met={passwordChecks.hasSpecialChar} text="Contains special character" />
              </div>
            </div>

            <Input
              label="Confirm Password"
              type="password"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              placeholder="Re-enter your password"
              icon={Lock}
              error={errors.confirmPassword}
              required
            />

            {/* Terms & Conditions */}
            <div>
              <label className="flex items-start gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  name="acceptedTerms"
                  checked={formData.acceptedTerms}
                  onChange={handleChange}
                  className="w-5 h-5 rounded text-primary-600 focus:ring-4 focus:ring-primary-200 border-gray-300 cursor-pointer mt-0.5"
                />
                <span className="text-sm text-gray-700">
                  I agree to the{' '}
                  <Link to="/terms" className="text-primary-600 hover:underline font-semibold">
                    Terms of Service
                  </Link>
                  {' '}and{' '}
                  <Link to="/privacy" className="text-primary-600 hover:underline font-semibold">
                    Privacy Policy
                  </Link>
                </span>
              </label>
              {errors.acceptedTerms && (
                <p className="text-xs text-danger-600 mt-1">{errors.acceptedTerms}</p>
              )}
            </div>

            {/* Create Account Button */}
            <Button
              type="submit"
              variant="primary"
              fullWidth
              loading={loading}
              icon={ArrowRight}
              iconPosition="right"
            >
              {loading ? 'Creating your account...' : 'Create Account'}
            </Button>
          </form>

          {/* Divider */}
          <div className="relative my-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="bg-white px-4 text-gray-500">or sign up with</span>
            </div>
          </div>

          {/* Google Sign Up */}
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
            {googleLoading ? 'Connecting to Google...' : 'Sign up with Google'}
          </Button>

          {/* Sign In Link */}
          <div className="mt-8 text-center">
            <p className="text-sm text-gray-600">
              Already have an account?{' '}
              <Link
                to="/login"
                className="font-semibold text-primary-600 hover:text-primary-700 hover:underline"
              >
                Sign In
              </Link>
            </p>
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

export default Register;
