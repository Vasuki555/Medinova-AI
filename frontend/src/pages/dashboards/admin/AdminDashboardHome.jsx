/**
 * Admin Dashboard Home
 * Platform-wide overview for administrators
 */

import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { apiService } from '@/services/api';
import {
  Users, Calendar, Shield, TrendingUp,
  ArrowRight, Bell, AlertTriangle, Pill, Stethoscope, UserPlus, X
} from 'lucide-react';

const MetricCard = ({ icon: Icon, label, value, color, sub, link }) => (
  <div className="bg-white dark:bg-neutral-800 rounded-2xl p-5 border border-neutral-200 dark:border-neutral-700 shadow-sm hover:shadow-md transition-shadow">
    <div className="flex items-center justify-between mb-3">
      <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${color}`}>
        <Icon className="w-5 h-5 text-white" />
      </div>
      {link && (
        <Link to={link} className="text-primary-500 hover:text-primary-600">
          <ArrowRight className="w-4 h-4" />
        </Link>
      )}
    </div>
    <p className="text-2xl font-bold text-neutral-900 dark:text-white">{value ?? '—'}</p>
    <p className="text-sm text-neutral-500 dark:text-neutral-400 mt-1">{label}</p>
    {sub && <p className="text-xs text-emerald-500 mt-0.5">{sub}</p>}
  </div>
);

const AdminDashboardHome = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showAddDoctor, setShowAddDoctor] = useState(false);
  const [doctorForm, setDoctorForm] = useState({
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    phone: '',
    date_of_birth: '',
    gender: '',
    specialization: '',
    years_of_experience: ''
  });
  const [formError, setFormError] = useState('');
  const [formSuccess, setFormSuccess] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    const loadStats = async () => {
      try {
        const data = await apiService.get('/admin/stats');
        setStats(data);
      } catch {
        setStats(null);
      } finally {
        setLoading(false);
      }
    };
    loadStats();
  }, []);

  const handleAddDoctor = async (e) => {
    e.preventDefault();
    setFormError('');
    setFormSuccess('');
    setSubmitting(true);

    try {
      const registerData = {
        email: doctorForm.email,
        password: doctorForm.password,
        first_name: doctorForm.first_name,
        last_name: doctorForm.last_name,
        phone: doctorForm.phone,
        date_of_birth: doctorForm.date_of_birth,
        gender: doctorForm.gender,
        role: 'doctor'
      };

      const response = await apiService.post('/auth/register', registerData);
      
      // If doctor was created, update their profile with specialization and experience
      if (doctorForm.specialization || doctorForm.years_of_experience) {
        try {
          // Get the user ID from the registration response
          const loginResponse = await apiService.post('/auth/login', {
            email: doctorForm.email,
            password: doctorForm.password
          });
          
          // Update doctor profile
          await apiService.put('/doctors/profile', {
            specialization: doctorForm.specialization || 'General Practitioner',
            years_of_experience: parseInt(doctorForm.years_of_experience) || 0
          }, {
            headers: {
              Authorization: `Bearer ${loginResponse.access_token}`
            }
          });
        } catch (profileError) {
          console.error('Error updating doctor profile:', profileError);
          // Continue anyway since doctor account was created
        }
      }
      
      setFormSuccess('Doctor account created successfully!');
      setDoctorForm({
        email: '',
        password: '',
        first_name: '',
        last_name: '',
        phone: '',
        date_of_birth: '',
        gender: '',
        specialization: '',
        years_of_experience: ''
      });
      
      // Reload stats
      const data = await apiService.get('/admin/stats');
      setStats(data);
      
      setTimeout(() => {
        setShowAddDoctor(false);
        setFormSuccess('');
      }, 2000);
    } catch (error) {
      setFormError(error.response?.data?.detail || 'Failed to create doctor account');
    } finally {
      setSubmitting(false);
    }
  };

  const metrics = stats?.metrics;

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Banner */}
      <div className="relative bg-gradient-to-r from-slate-700 via-slate-600 to-slate-700 rounded-2xl p-6 text-white overflow-hidden">
        <div className="absolute top-0 right-0 w-48 h-48 bg-white/5 rounded-full -translate-y-12 translate-x-12" />
        <div className="relative z-10">
          <p className="text-slate-300 text-sm font-medium mb-1">Administrator Console</p>
          <h1 className="text-2xl font-bold mb-1">MediNova AI Platform</h1>
          <p className="text-slate-300 text-sm">Platform overview and management center</p>
          <div className="flex gap-3 mt-4">
            <Link to="/admin/users" className="bg-white text-slate-700 text-sm font-semibold px-4 py-2 rounded-xl hover:bg-slate-50 transition-colors flex items-center gap-2">
              <Users className="w-4 h-4" /> Manage Users
            </Link>
            <button
              onClick={() => setShowAddDoctor(true)}
              className="bg-emerald-500 text-white text-sm font-semibold px-4 py-2 rounded-xl hover:bg-emerald-600 transition-colors flex items-center gap-2"
            >
              <UserPlus className="w-4 h-4" /> Add Doctor
            </button>
            <Link to="/admin/verify" className="bg-white/20 text-white text-sm font-semibold px-4 py-2 rounded-xl hover:bg-white/30 transition-colors flex items-center gap-2">
              <Shield className="w-4 h-4" /> Verify Doctors
            </Link>
          </div>
        </div>
      </div>

      {/* Core Metrics */}
      <div>
        <h2 className="text-sm font-bold text-neutral-400 uppercase tracking-wider mb-3">Platform Metrics</h2>
        {loading ? (
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {[1, 2, 3, 4].map(i => (
              <div key={i} className="h-28 bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 animate-pulse" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <MetricCard icon={Users} label="Total Users" value={metrics?.total_users} color="bg-blue-500" link="/admin/users" />
            <MetricCard icon={Stethoscope} label="Total Doctors" value={metrics?.total_doctors} color="bg-violet-500" sub={`${metrics?.verified_doctors || 0} verified`} link="/admin/verify" />
            <MetricCard icon={Calendar} label="Total Appointments" value={metrics?.total_appointments} color="bg-emerald-500" sub={`${metrics?.completed_appointments || 0} completed`} />
            <MetricCard icon={Pill} label="Active Medications" value={metrics?.active_medications} color="bg-amber-500" />
          </div>
        )}
      </div>

      {/* Secondary Metrics */}
      {!loading && metrics && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="bg-white dark:bg-neutral-800 rounded-2xl p-4 border border-neutral-200 dark:border-neutral-700 text-center">
            <p className="text-xl font-black text-blue-500">{metrics.total_patients}</p>
            <p className="text-xs text-neutral-500 mt-1">Patients</p>
          </div>
          <div className="bg-white dark:bg-neutral-800 rounded-2xl p-4 border border-neutral-200 dark:border-neutral-700 text-center">
            <p className="text-xl font-black text-emerald-500">{metrics.verified_doctors}</p>
            <p className="text-xs text-neutral-500 mt-1">Verified Doctors</p>
          </div>
          <div className="bg-white dark:bg-neutral-800 rounded-2xl p-4 border border-neutral-200 dark:border-neutral-700 text-center">
            <p className={`text-xl font-black ${metrics.unverified_doctors > 0 ? 'text-amber-500' : 'text-neutral-400'}`}>
              {metrics.unverified_doctors}
            </p>
            <p className="text-xs text-neutral-500 mt-1">Pending Verification</p>
          </div>
          <div className="bg-white dark:bg-neutral-800 rounded-2xl p-4 border border-neutral-200 dark:border-neutral-700 text-center">
            <p className="text-xl font-black text-violet-500">{metrics.completed_appointments}</p>
            <p className="text-xs text-neutral-500 mt-1">Completed Consults</p>
          </div>
        </div>
      )}

      {/* Pending Verification Alert */}
      {!loading && metrics?.unverified_doctors > 0 && (
        <div className="p-4 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-2xl flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-amber-600 dark:text-amber-400 flex-shrink-0 mt-0.5" />
          <div className="flex-grow">
            <p className="font-semibold text-amber-800 dark:text-amber-300 text-sm">Doctors Pending Verification</p>
            <p className="text-amber-700 dark:text-amber-400 text-sm mt-0.5">
              {metrics.unverified_doctors} doctor{metrics.unverified_doctors > 1 ? 's' : ''} waiting for credential verification.
            </p>
          </div>
          <Link to="/admin/verify" className="bg-amber-500 text-white text-sm font-semibold px-4 py-2 rounded-xl hover:bg-amber-600 transition-colors flex-shrink-0">
            Review
          </Link>
        </div>
      )}

      {/* Recent Signups */}
      {!loading && stats?.recent_signups?.length > 0 && (
        <div className="bg-white dark:bg-neutral-800 rounded-2xl p-6 border border-neutral-200 dark:border-neutral-700 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-neutral-900 dark:text-white">Recent Signups</h2>
            <Link to="/admin/users" className="text-primary-500 text-sm font-medium">View All →</Link>
          </div>
          <div className="space-y-3">
            {stats.recent_signups.map(user => (
              <div key={user.id} className="flex items-center gap-3 p-3 hover:bg-neutral-50 dark:hover:bg-neutral-700/40 rounded-xl transition-colors">
                <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center text-white font-bold text-sm flex-shrink-0">
                  {(user.first_name || 'U')[0]}
                </div>
                <div className="flex-grow min-w-0">
                  <p className="font-semibold text-sm text-neutral-900 dark:text-white">
                    {user.first_name} {user.last_name}
                  </p>
                  <p className="text-xs text-neutral-400 truncate">{user.email}</p>
                </div>
                <span className={`text-xs font-medium px-2 py-1 rounded-full flex-shrink-0 ${
                  user.role === 'doctor'
                    ? 'bg-violet-100 text-violet-600 dark:bg-violet-900/30 dark:text-violet-400'
                    : user.role === 'admin'
                    ? 'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400'
                    : 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400'
                }`}>
                  {user.role}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="grid grid-cols-3 gap-4">
        {[
          { icon: Users, label: 'User Management', path: '/admin/users', color: 'from-blue-500 to-blue-600' },
          { icon: Shield, label: 'Verify Doctors', path: '/admin/verify', color: 'from-violet-500 to-violet-600' },
          { icon: Bell, label: 'Notifications', path: '/admin/notifications', color: 'from-amber-500 to-amber-600' },
        ].map(item => (
          <Link
            key={item.path}
            to={item.path}
            className={`bg-gradient-to-br ${item.color} rounded-2xl p-5 text-white flex flex-col items-center justify-center gap-2 hover:scale-[1.02] transition-transform shadow-sm`}
          >
            <item.icon className="w-7 h-7" />
            <span className="text-sm font-semibold text-center">{item.label}</span>
          </Link>
        ))}
      </div>

      {/* Add Doctor Modal */}
      {showAddDoctor && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white dark:bg-neutral-800 rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            {/* Header */}
            <div className="flex items-center justify-between p-6 border-b border-neutral-200 dark:border-neutral-700">
              <div>
                <h2 className="text-xl font-bold text-neutral-900 dark:text-white">Add New Doctor</h2>
                <p className="text-sm text-neutral-500 mt-1">Create a doctor account</p>
              </div>
              <button
                onClick={() => setShowAddDoctor(false)}
                className="text-neutral-400 hover:text-neutral-600 dark:hover:text-neutral-300"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Form */}
            <form onSubmit={handleAddDoctor} className="p-6 space-y-4">
              {formError && (
                <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl text-red-700 dark:text-red-400 text-sm">
                  {formError}
                </div>
              )}

              {formSuccess && (
                <div className="p-3 bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-xl text-emerald-700 dark:text-emerald-400 text-sm">
                  {formSuccess}
                </div>
              )}

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
                    First Name <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    value={doctorForm.first_name}
                    onChange={(e) => setDoctorForm({ ...doctorForm, first_name: e.target.value })}
                    required
                    className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
                    Last Name <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    value={doctorForm.last_name}
                    onChange={(e) => setDoctorForm({ ...doctorForm, last_name: e.target.value })}
                    required
                    className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
                  Email <span className="text-red-500">*</span>
                </label>
                <input
                  type="email"
                  value={doctorForm.email}
                  onChange={(e) => setDoctorForm({ ...doctorForm, email: e.target.value })}
                  required
                  className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
                  Password <span className="text-red-500">*</span>
                </label>
                <input
                  type="password"
                  value={doctorForm.password}
                  onChange={(e) => setDoctorForm({ ...doctorForm, password: e.target.value })}
                  required
                  minLength={8}
                  className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white"
                  placeholder="Min. 8 characters"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
                  Phone
                </label>
                <input
                  type="tel"
                  value={doctorForm.phone}
                  onChange={(e) => setDoctorForm({ ...doctorForm, phone: e.target.value })}
                  className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white"
                  placeholder="+1234567890"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
                    Date of Birth
                  </label>
                  <input
                    type="date"
                    value={doctorForm.date_of_birth}
                    onChange={(e) => setDoctorForm({ ...doctorForm, date_of_birth: e.target.value })}
                    className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
                    Gender
                  </label>
                  <select
                    value={doctorForm.gender}
                    onChange={(e) => setDoctorForm({ ...doctorForm, gender: e.target.value })}
                    className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white"
                  >
                    <option value="">Select Gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                  </select>
                </div>
              </div>

              {/* Specialization and Experience */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
                    Specialization <span className="text-red-500">*</span>
                  </label>
                  <select
                    value={doctorForm.specialization}
                    onChange={(e) => setDoctorForm({ ...doctorForm, specialization: e.target.value })}
                    required
                    className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white"
                  >
                    <option value="">Select Specialization</option>
                    <option value="General Practitioner">General Practitioner</option>
                    <option value="Cardiologist">Cardiologist</option>
                    <option value="Dermatologist">Dermatologist</option>
                    <option value="Neurologist">Neurologist</option>
                    <option value="Orthopedic">Orthopedic</option>
                    <option value="Pediatrician">Pediatrician</option>
                    <option value="Psychiatrist">Psychiatrist</option>
                    <option value="Gynecologist">Gynecologist</option>
                    <option value="Ophthalmologist">Ophthalmologist</option>
                    <option value="ENT Specialist">ENT Specialist</option>
                    <option value="Diabetologist">Diabetologist</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">
                    Years of Experience <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="number"
                    value={doctorForm.years_of_experience}
                    onChange={(e) => setDoctorForm({ ...doctorForm, years_of_experience: e.target.value })}
                    required
                    min="0"
                    max="50"
                    className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white"
                    placeholder="e.g., 10"
                  />
                </div>
              </div>

              {/* Actions */}
              <div className="flex gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowAddDoctor(false)}
                  className="flex-1 px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 text-neutral-700 dark:text-neutral-300 rounded-xl hover:bg-neutral-50 dark:hover:bg-neutral-700 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="flex-1 px-4 py-2.5 bg-emerald-500 text-white rounded-xl hover:bg-emerald-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-semibold"
                >
                  {submitting ? 'Creating...' : 'Create Doctor Account'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminDashboardHome;
