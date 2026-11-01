/**
 * Patient Profile Page
 * Edit personal info, medical profile, emergency contact, and password
 */

import { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { apiService } from '@/services/api';
import {
  User, Save, Loader2, CheckCircle, AlertCircle,
  Lock, Phone, Calendar, Heart, Shield, Edit2,
  Activity, Droplets, Weight, Ruler, QrCode, Download
} from 'lucide-react';
import { API_BASE_URL } from '@/utils/constants';

const BLOOD_GROUPS = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'];
const GENDERS = ['male', 'female', 'other', 'prefer_not_to_say'];

const SectionCard = ({ title, icon: Icon, children }) => (
  <div className="bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 shadow-sm overflow-hidden">
    <div className="flex items-center gap-3 px-6 py-4 border-b border-neutral-100 dark:border-neutral-700">
      <div className="w-8 h-8 rounded-xl bg-primary-50 dark:bg-primary-900/30 flex items-center justify-center">
        <Icon className="w-4 h-4 text-primary-500" />
      </div>
      <h2 className="font-bold text-neutral-900 dark:text-white">{title}</h2>
    </div>
    <div className="p-6">{children}</div>
  </div>
);

const FormField = ({ label, required, children }) => (
  <div>
    <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">
      {label} {required && <span className="text-red-500">*</span>}
    </label>
    {children}
  </div>
);

const inputCls = "w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white transition-colors";

const PatientProfile = () => {
  const { user, updateUser } = useAuth();

  // Edit mode toggles
  const [editingPersonal, setEditingPersonal] = useState(false);
  const [editingMedical, setEditingMedical] = useState(false);
  const [editingPassword, setEditingPassword] = useState(false);

  // Personal info state
  const [personal, setPersonal] = useState({
    first_name: '',
    last_name: '',
    phone: '',
    date_of_birth: '',
    gender: '',
  });

  // Medical profile state
  const [medical, setMedical] = useState({
    blood_group: '',
    height_cm: '',
    weight_kg: '',
    allergies: '',
    chronic_conditions: '',
    emergency_contact_name: '',
    emergency_contact_phone: '',
    emergency_contact_relation: '',
  });

  // Password change state
  const [pwForm, setPwForm] = useState({
    current_password: '',
    new_password: '',
    confirm_password: '',
  });

  const [loadingPersonal, setLoadingPersonal] = useState(false);
  const [loadingMedical, setLoadingMedical] = useState(false);
  const [loadingPw, setLoadingPw] = useState(false);
  const [loadingProfile, setLoadingProfile] = useState(true);

  const [personalSuccess, setPersonalSuccess] = useState('');
  const [personalError, setPersonalError] = useState('');
  const [medicalSuccess, setMedicalSuccess] = useState('');
  const [medicalError, setMedicalError] = useState('');
  const [pwSuccess, setPwSuccess] = useState('');
  const [pwError, setPwError] = useState('');

  // QR code
  const [qrSrc, setQrSrc] = useState('');
  const [qrLoading, setQrLoading] = useState(true);
  const [qrError, setQrError] = useState('');

  // Pre-fill personal form from auth context
  useEffect(() => {
    if (user) {
      setPersonal({
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        phone: user.phone || '',
        date_of_birth: user.date_of_birth ? user.date_of_birth.slice(0, 10) : '',
        gender: user.gender || '',
      });
    }
  }, [user]);

  // Load medical profile
  useEffect(() => {
    const loadProfile = async () => {
      try {
        const data = await apiService.get('/patients/profile');
        if (data) {
          setMedical({
            blood_group: data.blood_group || '',
            height_cm: data.height_cm || '',
            weight_kg: data.weight_kg || '',
            allergies: Array.isArray(data.allergies) ? data.allergies.join(', ') : '',
            chronic_conditions: Array.isArray(data.chronic_conditions) ? data.chronic_conditions.join(', ') : '',
            emergency_contact_name: data.emergency_contact?.name || '',
            emergency_contact_phone: data.emergency_contact?.phone || '',
            emergency_contact_relation: data.emergency_contact?.relationship || '',
          });
        }
      } catch (err) {
        // Profile may not exist yet — that's fine
      } finally {
        setLoadingProfile(false);
      }
    };
    loadProfile();
  }, []);

  // Load patient QR
  useEffect(() => {
    if (!user?._id) {
      console.log('QR: No user ID available yet');
      return;
    }
    
    const loadQR = async () => {
      try {
        console.log('QR: Loading for user', user._id);
        
        // Use direct fetch with the current token from apiService
        const token = localStorage.getItem('accessToken');
        if (!token) {
          console.error('QR: No access token found');
          setQrLoading(false);
          return;
        }
        
        // Construct full URL including base
        const baseUrl = API_BASE_URL.replace('/api/v1', ''); // Remove /api/v1 if present
        const url = `${baseUrl}/api/v1/qr/patient/${user._id}`;
        console.log('QR: Fetching from', url);
        
        const response = await fetch(url, {
          method: 'GET',
          headers: { 
            'Authorization': `Bearer ${token}`,
            'Accept': 'image/png'
          },
          credentials: 'include'
        });
        
        console.log('QR: Response status', response.status, response.statusText);
        
        if (response.status === 401) {
          console.error('QR: Token expired or invalid, please refresh the page');
          setQrLoading(false);
          return;
        }
        
        if (!response.ok) {
          const text = await response.text();
          console.error('QR: Error response', text);
          throw new Error(`Failed to load QR code: ${response.status}`);
        }
        
        const blob = await response.blob();
        console.log('QR: Received blob', blob.size, 'bytes, type:', blob.type);
        
        const objectUrl = URL.createObjectURL(blob);
        console.log('QR: Created object URL', objectUrl);
        setQrSrc(objectUrl);
      } catch (err) {
        console.error('QR load error:', err);
      } finally {
        setQrLoading(false);
      }
    };
    
    // Add a small delay to ensure user is fully loaded
    const timer = setTimeout(loadQR, 500);
    return () => clearTimeout(timer);
  }, [user]);

  const savePersonal = async (e) => {
    e.preventDefault();
    if (!personal.first_name || !personal.last_name) {
      setPersonalError('First name and last name are required');
      return;
    }
    setLoadingPersonal(true);
    setPersonalError('');
    setPersonalSuccess('');
    try {
      // Convert empty strings to null for optional fields
      const payload = {
        first_name: personal.first_name,
        last_name: personal.last_name,
        phone: personal.phone.trim() || null,
        date_of_birth: personal.date_of_birth || null,
        gender: personal.gender || null,
      };
      const updated = await apiService.put('/patients/profile/basic', payload);
      updateUser({ first_name: personal.first_name, last_name: personal.last_name });
      setPersonalSuccess('Personal information updated successfully!');
      setEditingPersonal(false); // Exit edit mode
      setTimeout(() => setPersonalSuccess(''), 3000);
    } catch (err) {
      // Handle validation errors (array) or simple error message (string)
      const errorDetail = err.response?.data?.detail;
      if (Array.isArray(errorDetail)) {
        // Pydantic validation errors - extract messages
        const messages = errorDetail.map(e => e.msg || JSON.stringify(e)).join(', ');
        setPersonalError(messages);
      } else if (typeof errorDetail === 'string') {
        setPersonalError(errorDetail);
      } else {
        setPersonalError('Failed to update profile');
      }
    } finally {
      setLoadingPersonal(false);
    }
  };

  const saveMedical = async (e) => {
    e.preventDefault();
    setLoadingMedical(true);
    setMedicalError('');
    setMedicalSuccess('');
    try {
      const payload = {
        blood_group: medical.blood_group || null,
        height_cm: medical.height_cm ? parseFloat(medical.height_cm) : null,
        weight_kg: medical.weight_kg ? parseFloat(medical.weight_kg) : null,
        allergies: medical.allergies ? medical.allergies.split(',').map(s => s.trim()).filter(Boolean) : [],
        chronic_conditions: medical.chronic_conditions ? medical.chronic_conditions.split(',').map(s => s.trim()).filter(Boolean) : [],
        emergency_contact: medical.emergency_contact_name ? {
          name: medical.emergency_contact_name,
          phone: medical.emergency_contact_phone,
          relationship: medical.emergency_contact_relation,
        } : null,
      };
      await apiService.put('/patients/profile', payload);
      setMedicalSuccess('Medical profile updated successfully!');
      setEditingMedical(false); // Exit edit mode
      setTimeout(() => setMedicalSuccess(''), 3000);
    } catch (err) {
      // Handle validation errors (array) or simple error message (string)
      const errorDetail = err.response?.data?.detail;
      if (Array.isArray(errorDetail)) {
        const messages = errorDetail.map(e => e.msg || JSON.stringify(e)).join(', ');
        setMedicalError(messages);
      } else if (typeof errorDetail === 'string') {
        setMedicalError(errorDetail);
      } else {
        setMedicalError('Failed to update medical profile');
      }
    } finally {
      setLoadingMedical(false);
    }
  };

  const changePassword = async (e) => {
    e.preventDefault();
    if (pwForm.new_password !== pwForm.confirm_password) {
      setPwError('New passwords do not match');
      return;
    }
    if (pwForm.new_password.length < 8) {
      setPwError('Password must be at least 8 characters');
      return;
    }
    setLoadingPw(true);
    setPwError('');
    setPwSuccess('');
    try {
      await apiService.post('/auth/change-password', {
        current_password: pwForm.current_password,
        new_password: pwForm.new_password,
      });
      setPwSuccess('Password changed successfully!');
      setPwForm({ current_password: '', new_password: '', confirm_password: '' });
      setEditingPassword(false); // Exit edit mode
      setTimeout(() => setPwSuccess(''), 3000);
    } catch (err) {
      // Handle validation errors (array) or simple error message (string)
      const errorDetail = err.response?.data?.detail;
      if (Array.isArray(errorDetail)) {
        const messages = errorDetail.map(e => e.msg || JSON.stringify(e)).join(', ');
        setPwError(messages);
      } else if (typeof errorDetail === 'string') {
        setPwError(errorDetail);
      } else {
        setPwError('Failed to change password');
      }
    } finally {
      setLoadingPw(false);
    }
  };

  const downloadQR = async () => {
    try {
      const token = localStorage.getItem('accessToken');
      const baseUrl = API_BASE_URL.replace('/api/v1', '');
      const res = await fetch(`${baseUrl}/api/v1/qr/patient/${user._id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!res.ok) throw new Error('Failed to download QR');
      const blob = await res.blob();
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `MediNova_Patient_QR_${user.first_name}.png`;
      link.click();
    } catch (err) { 
      alert('Could not download QR code. Please try logging out and back in.');
    }
  };

  const refreshQR = () => {
    setQrLoading(true);
    setQrError('');
    setQrSrc('');
    // Trigger useEffect by creating a tiny state change
    const loadQR = async () => {
      try {
        const token = localStorage.getItem('accessToken');
        if (!token) {
          setQrError('Please log out and log back in');
          setQrLoading(false);
          return;
        }
        
        const baseUrl = API_BASE_URL.replace('/api/v1', '');
        const url = `${baseUrl}/api/v1/qr/patient/${user._id}`;
        
        const response = await fetch(url, {
          method: 'GET',
          headers: { 
            'Authorization': `Bearer ${token}`,
            'Accept': 'image/png'
          }
        });
        
        if (response.status === 401) {
          setQrError('Session expired. Please log out and log back in.');
          setQrLoading(false);
          return;
        }
        
        if (!response.ok) {
          throw new Error(`Failed: ${response.status}`);
        }
        
        const blob = await response.blob();
        const objectUrl = URL.createObjectURL(blob);
        setQrSrc(objectUrl);
        setQrError('');
      } catch (err) {
        setQrError('Failed to load QR code');
        console.error('QR error:', err);
      } finally {
        setQrLoading(false);
      }
    };
    loadQR();
  };

  // Computed BMI
  const bmi = medical.height_cm && medical.weight_kg
    ? (parseFloat(medical.weight_kg) / Math.pow(parseFloat(medical.height_cm) / 100, 2)).toFixed(1)
    : null;

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center gap-4">
        <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary-500 to-cyan-500 flex items-center justify-center text-white text-2xl font-bold shadow-lg">
          {user?.first_name?.[0]}{user?.last_name?.[0]}
        </div>
        <div>
          <h1 className="text-2xl font-bold text-neutral-900 dark:text-white">
            {user?.first_name} {user?.last_name}
          </h1>
          <p className="text-neutral-500 dark:text-neutral-400">{user?.email}</p>
          <span className="text-xs bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 px-2 py-0.5 rounded-lg font-medium">Patient</span>
        </div>
      </div>

      {/* Personal Information */}
      <SectionCard title="Personal Information" icon={User}>
        {!editingPersonal ? (
          /* READ MODE */
          <div className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div>
                <label className="block text-xs font-medium text-neutral-500 dark:text-neutral-400 mb-1">First Name</label>
                <p className="text-sm font-medium text-neutral-900 dark:text-white">{personal.first_name || '—'}</p>
              </div>
              <div>
                <label className="block text-xs font-medium text-neutral-500 dark:text-neutral-400 mb-1">Last Name</label>
                <p className="text-sm font-medium text-neutral-900 dark:text-white">{personal.last_name || '—'}</p>
              </div>
              <div>
                <label className="block text-xs font-medium text-neutral-500 dark:text-neutral-400 mb-1">Phone Number</label>
                <p className="text-sm font-medium text-neutral-900 dark:text-white">{personal.phone || '—'}</p>
              </div>
              <div>
                <label className="block text-xs font-medium text-neutral-500 dark:text-neutral-400 mb-1">Date of Birth</label>
                <p className="text-sm font-medium text-neutral-900 dark:text-white">{personal.date_of_birth || '—'}</p>
              </div>
              <div>
                <label className="block text-xs font-medium text-neutral-500 dark:text-neutral-400 mb-1">Gender</label>
                <p className="text-sm font-medium text-neutral-900 dark:text-white capitalize">
                  {personal.gender ? personal.gender.replace(/_/g, ' ') : '—'}
                </p>
              </div>
            </div>

            {personalSuccess && (
              <div className="flex items-center gap-2 p-3 bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-xl text-sm text-emerald-600 dark:text-emerald-400">
                <CheckCircle className="w-4 h-4 flex-shrink-0" /> {personalSuccess}
              </div>
            )}

            <button
              onClick={() => setEditingPersonal(true)}
              className="flex items-center gap-2 bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold px-5 py-2.5 rounded-xl transition-colors"
            >
              <Edit2 className="w-4 h-4" />
              Edit Personal Info
            </button>
          </div>
        ) : (
          /* EDIT MODE */
          <form onSubmit={savePersonal} className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <FormField label="First Name" required>
                <input
                  type="text"
                  value={personal.first_name}
                  onChange={e => setPersonal(p => ({ ...p, first_name: e.target.value }))}
                  className={inputCls}
                  required
                />
              </FormField>
              <FormField label="Last Name" required>
                <input
                  type="text"
                  value={personal.last_name}
                  onChange={e => setPersonal(p => ({ ...p, last_name: e.target.value }))}
                  className={inputCls}
                  required
                />
              </FormField>
              <FormField label="Phone Number">
                <input
                  type="tel"
                  value={personal.phone}
                  onChange={e => setPersonal(p => ({ ...p, phone: e.target.value }))}
                  placeholder="+1234567890 or 1234567890"
                  className={inputCls}
                />
              </FormField>
              <FormField label="Date of Birth">
                <input
                  type="date"
                  value={personal.date_of_birth}
                  onChange={e => setPersonal(p => ({ ...p, date_of_birth: e.target.value }))}
                  className={inputCls}
                />
              </FormField>
              <FormField label="Gender">
                <select
                  value={personal.gender}
                  onChange={e => setPersonal(p => ({ ...p, gender: e.target.value }))}
                  className={inputCls}
                >
                  <option value="">Select gender</option>
                  {GENDERS.map(g => (
                    <option key={g} value={g}>{g.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}</option>
                  ))}
                </select>
              </FormField>
            </div>

            {personalError && (
              <div className="flex items-center gap-2 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl text-sm text-red-600 dark:text-red-400">
                <AlertCircle className="w-4 h-4 flex-shrink-0" /> {personalError}
              </div>
            )}

            <div className="flex gap-3">
              <button
                type="submit"
                disabled={loadingPersonal}
                className="flex items-center gap-2 bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold px-5 py-2.5 rounded-xl transition-colors disabled:opacity-50"
              >
                {loadingPersonal ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
                Save Changes
              </button>
              <button
                type="button"
                onClick={() => {
                  setEditingPersonal(false);
                  setPersonalError('');
                }}
                className="px-5 py-2.5 border border-neutral-300 dark:border-neutral-600 text-neutral-700 dark:text-neutral-300 text-sm font-semibold rounded-xl hover:bg-neutral-50 dark:hover:bg-neutral-700 transition-colors"
              >
                Cancel
              </button>
            </div>
          </form>
        )}
      </SectionCard>

      {/* Medical Profile */}
      <SectionCard title="Medical Profile" icon={Heart}>
        {loadingProfile ? (
          <div className="flex items-center justify-center py-8">
            <Loader2 className="w-6 h-6 text-primary-400 animate-spin" />
          </div>
        ) : !editingMedical ? (
          /* READ MODE */
          <div className="space-y-4">
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-6">
              <div>
                <label className="block text-xs font-medium text-neutral-500 dark:text-neutral-400 mb-1">Blood Group</label>
                <p className="text-sm font-medium text-neutral-900 dark:text-white">{medical.blood_group || '—'}</p>
              </div>
              <div>
                <label className="block text-xs font-medium text-neutral-500 dark:text-neutral-400 mb-1">Height</label>
                <p className="text-sm font-medium text-neutral-900 dark:text-white">{medical.height_cm ? `${medical.height_cm} cm` : '—'}</p>
              </div>
              <div>
                <label className="block text-xs font-medium text-neutral-500 dark:text-neutral-400 mb-1">Weight</label>
                <p className="text-sm font-medium text-neutral-900 dark:text-white">{medical.weight_kg ? `${medical.weight_kg} kg` : '—'}</p>
              </div>
              <div>
                <label className="block text-xs font-medium text-neutral-500 dark:text-neutral-400 mb-1">BMI</label>
                <p className={`text-sm font-medium ${
                  bmi ? (
                    parseFloat(bmi) < 18.5 ? 'text-blue-500' :
                    parseFloat(bmi) < 25 ? 'text-emerald-500' :
                    parseFloat(bmi) < 30 ? 'text-amber-500' : 'text-red-500'
                  ) : 'text-neutral-900 dark:text-white'
                }`}>
                  {bmi || '—'}
                </p>
              </div>
            </div>

            <div className="border-t border-neutral-100 dark:border-neutral-700 pt-4">
              <div className="space-y-3">
                <div>
                  <label className="block text-xs font-medium text-neutral-500 dark:text-neutral-400 mb-1">Allergies</label>
                  <p className="text-sm text-neutral-900 dark:text-white">{medical.allergies || 'None reported'}</p>
                </div>
                <div>
                  <label className="block text-xs font-medium text-neutral-500 dark:text-neutral-400 mb-1">Chronic Conditions</label>
                  <p className="text-sm text-neutral-900 dark:text-white">{medical.chronic_conditions || 'None reported'}</p>
                </div>
              </div>
            </div>

            {/* Emergency Contact */}
            <div className="border-t border-neutral-100 dark:border-neutral-700 pt-4">
              <p className="text-sm font-semibold text-neutral-700 dark:text-neutral-300 mb-3 flex items-center gap-2">
                <Shield className="w-4 h-4 text-rose-500" />
                Emergency Contact
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div>
                  <label className="block text-xs font-medium text-neutral-500 dark:text-neutral-400 mb-1">Name</label>
                  <p className="text-sm text-neutral-900 dark:text-white">{medical.emergency_contact_name || '—'}</p>
                </div>
                <div>
                  <label className="block text-xs font-medium text-neutral-500 dark:text-neutral-400 mb-1">Phone</label>
                  <p className="text-sm text-neutral-900 dark:text-white">{medical.emergency_contact_phone || '—'}</p>
                </div>
                <div>
                  <label className="block text-xs font-medium text-neutral-500 dark:text-neutral-400 mb-1">Relationship</label>
                  <p className="text-sm text-neutral-900 dark:text-white">{medical.emergency_contact_relation || '—'}</p>
                </div>
              </div>
            </div>

            {medicalSuccess && (
              <div className="flex items-center gap-2 p-3 bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-xl text-sm text-emerald-600 dark:text-emerald-400">
                <CheckCircle className="w-4 h-4 flex-shrink-0" /> {medicalSuccess}
              </div>
            )}

            <button
              onClick={() => setEditingMedical(true)}
              className="flex items-center gap-2 bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold px-5 py-2.5 rounded-xl transition-colors"
            >
              <Edit2 className="w-4 h-4" />
              Edit Medical Profile
            </button>
          </div>
        ) : (
          /* EDIT MODE */
          <form onSubmit={saveMedical} className="space-y-4">
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <FormField label="Blood Group">
                <select
                  value={medical.blood_group}
                  onChange={e => setMedical(m => ({ ...m, blood_group: e.target.value }))}
                  className={inputCls}
                >
                  <option value="">Select</option>
                  {BLOOD_GROUPS.map(b => <option key={b} value={b}>{b}</option>)}
                </select>
              </FormField>
              <FormField label="Height (cm)">
                <input
                  type="number"
                  value={medical.height_cm}
                  onChange={e => setMedical(m => ({ ...m, height_cm: e.target.value }))}
                  placeholder="170"
                  className={inputCls}
                  min="50" max="300"
                />
              </FormField>
              <FormField label="Weight (kg)">
                <input
                  type="number"
                  value={medical.weight_kg}
                  onChange={e => setMedical(m => ({ ...m, weight_kg: e.target.value }))}
                  placeholder="70"
                  className={inputCls}
                  min="10" max="500"
                />
              </FormField>
              <div>
                <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">BMI</label>
                <div className={`${inputCls} bg-neutral-50 dark:bg-neutral-600 text-neutral-500`}>
                  {bmi ? (
                    <span className={
                      parseFloat(bmi) < 18.5 ? 'text-blue-500' :
                      parseFloat(bmi) < 25 ? 'text-emerald-500' :
                      parseFloat(bmi) < 30 ? 'text-amber-500' : 'text-red-500'
                    }>
                      {bmi}
                    </span>
                  ) : '—'}
                </div>
              </div>
            </div>

            <FormField label="Allergies (comma-separated)">
              <input
                type="text"
                value={medical.allergies}
                onChange={e => setMedical(m => ({ ...m, allergies: e.target.value }))}
                placeholder="Penicillin, Peanuts, Dust..."
                className={inputCls}
              />
            </FormField>

            <FormField label="Chronic Conditions (comma-separated)">
              <input
                type="text"
                value={medical.chronic_conditions}
                onChange={e => setMedical(m => ({ ...m, chronic_conditions: e.target.value }))}
                placeholder="Diabetes, Hypertension..."
                className={inputCls}
              />
            </FormField>

            {/* Emergency Contact */}
            <div className="border-t border-neutral-100 dark:border-neutral-700 pt-4">
              <p className="text-sm font-semibold text-neutral-700 dark:text-neutral-300 mb-3 flex items-center gap-2">
                <Shield className="w-4 h-4 text-rose-500" />
                Emergency Contact
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <FormField label="Name">
                  <input
                    type="text"
                    value={medical.emergency_contact_name}
                    onChange={e => setMedical(m => ({ ...m, emergency_contact_name: e.target.value }))}
                    placeholder="Full name"
                    className={inputCls}
                  />
                </FormField>
                <FormField label="Phone">
                  <input
                    type="tel"
                    value={medical.emergency_contact_phone}
                    onChange={e => setMedical(m => ({ ...m, emergency_contact_phone: e.target.value }))}
                    placeholder="+1 234 567 8900"
                    className={inputCls}
                  />
                </FormField>
                <FormField label="Relationship">
                  <input
                    type="text"
                    value={medical.emergency_contact_relation}
                    onChange={e => setMedical(m => ({ ...m, emergency_contact_relation: e.target.value }))}
                    placeholder="Spouse, Parent..."
                    className={inputCls}
                  />
                </FormField>
              </div>
            </div>

            {medicalError && (
              <div className="flex items-center gap-2 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl text-sm text-red-600 dark:text-red-400">
                <AlertCircle className="w-4 h-4 flex-shrink-0" /> {medicalError}
              </div>
            )}

            <div className="flex gap-3">
              <button
                type="submit"
                disabled={loadingMedical}
                className="flex items-center gap-2 bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold px-5 py-2.5 rounded-xl transition-colors disabled:opacity-50"
              >
                {loadingMedical ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
                Save Changes
              </button>
              <button
                type="button"
                onClick={() => {
                  setEditingMedical(false);
                  setMedicalError('');
                }}
                className="px-5 py-2.5 border border-neutral-300 dark:border-neutral-600 text-neutral-700 dark:text-neutral-300 text-sm font-semibold rounded-xl hover:bg-neutral-50 dark:hover:bg-neutral-700 transition-colors"
              >
                Cancel
              </button>
            </div>
          </form>
        )}
      </SectionCard>

      {/* Change Password */}
      <SectionCard title="Change Password" icon={Lock}>
        {!editingPassword ? (
          /* READ MODE - Hidden */
          <div className="space-y-3">
            <p className="text-sm text-neutral-600 dark:text-neutral-400">
              Keep your account secure by regularly updating your password.
            </p>

            {pwSuccess && (
              <div className="flex items-center gap-2 p-3 bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-xl text-sm text-emerald-600 dark:text-emerald-400">
                <CheckCircle className="w-4 h-4 flex-shrink-0" /> {pwSuccess}
              </div>
            )}

            <button
              onClick={() => setEditingPassword(true)}
              className="flex items-center gap-2 bg-rose-500 hover:bg-rose-600 text-white text-sm font-semibold px-5 py-2.5 rounded-xl transition-colors"
            >
              <Lock className="w-4 h-4" />
              Change Password
            </button>
          </div>
        ) : (
          /* EDIT MODE - Form visible */
          <form onSubmit={changePassword} className="space-y-4 max-w-md">
            <FormField label="Current Password" required>
              <input
                type="password"
                value={pwForm.current_password}
                onChange={e => setPwForm(p => ({ ...p, current_password: e.target.value }))}
                className={inputCls}
                required
                autoComplete="current-password"
              />
            </FormField>
            <FormField label="New Password" required>
              <input
                type="password"
                value={pwForm.new_password}
                onChange={e => setPwForm(p => ({ ...p, new_password: e.target.value }))}
                className={inputCls}
                required
                autoComplete="new-password"
                minLength={8}
              />
            </FormField>
            <FormField label="Confirm New Password" required>
              <input
                type="password"
                value={pwForm.confirm_password}
                onChange={e => setPwForm(p => ({ ...p, confirm_password: e.target.value }))}
                className={inputCls}
                required
                autoComplete="new-password"
              />
            </FormField>

            {pwError && (
              <div className="flex items-center gap-2 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl text-sm text-red-600 dark:text-red-400">
                <AlertCircle className="w-4 h-4 flex-shrink-0" /> {pwError}
              </div>
            )}

            <div className="flex gap-3">
              <button
                type="submit"
                disabled={loadingPw}
                className="flex items-center gap-2 bg-rose-500 hover:bg-rose-600 text-white text-sm font-semibold px-5 py-2.5 rounded-xl transition-colors disabled:opacity-50"
              >
                {loadingPw ? <Loader2 className="w-4 h-4 animate-spin" /> : <Lock className="w-4 h-4" />}
                Update Password
              </button>
              <button
                type="button"
                onClick={() => {
                  setEditingPassword(false);
                  setPwError('');
                  setPwForm({ current_password: '', new_password: '', confirm_password: '' });
                }}
                className="px-5 py-2.5 border border-neutral-300 dark:border-neutral-600 text-neutral-700 dark:text-neutral-300 text-sm font-semibold rounded-xl hover:bg-neutral-50 dark:hover:bg-neutral-700 transition-colors"
              >
                Cancel
              </button>
            </div>
          </form>
        )}
      </SectionCard>

      {/* Patient QR Code */}
      <SectionCard title="Your Patient QR Code" icon={QrCode}>
        <div className="flex flex-col sm:flex-row items-center gap-6">
          <div className="w-40 h-40 bg-neutral-50 dark:bg-neutral-700 rounded-2xl border-2 border-dashed border-neutral-200 dark:border-neutral-600 flex items-center justify-center flex-shrink-0">
            {qrLoading ? (
              <Loader2 className="w-6 h-6 text-primary-400 animate-spin" />
            ) : qrError ? (
              <div className="text-center p-2">
                <AlertCircle className="w-8 h-8 text-red-400 mx-auto mb-2" />
                <p className="text-xs text-red-600 dark:text-red-400">{qrError}</p>
              </div>
            ) : qrSrc ? (
              <img src={qrSrc} alt="Patient QR" className="w-full h-full object-contain p-2" />
            ) : (
              <div className="text-center p-2">
                <QrCode className="w-10 h-10 text-neutral-300 mx-auto mb-2" />
                <p className="text-xs text-neutral-500">QR not loaded</p>
              </div>
            )}
          </div>
          <div className="flex-1">
            <p className="font-semibold text-neutral-900 dark:text-white mb-1">Share Your Medical QR Code</p>
            <p className="text-sm text-neutral-500 dark:text-neutral-400 mb-3">
              Use this QR code to quickly share your medical information with healthcare providers. 
              They can scan it to access your health records securely.
            </p>
            <div className="flex gap-2">
              {!qrSrc && !qrLoading && (
                <button
                  onClick={refreshQR}
                  className="flex items-center gap-2 bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold px-4 py-2 rounded-xl transition-colors"
                >
                  <Loader2 className="w-4 h-4" />
                  Load QR Code
                </button>
              )}
              {qrSrc && (
                <button
                  onClick={downloadQR}
                  className="flex items-center gap-2 bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold px-4 py-2 rounded-xl transition-colors"
                >
                  <Download className="w-4 h-4" />
                  Download QR PNG
                </button>
              )}
              {qrError && (
                <button
                  onClick={refreshQR}
                  className="flex items-center gap-2 bg-neutral-500 hover:bg-neutral-600 text-white text-sm font-semibold px-4 py-2 rounded-xl transition-colors"
                >
                  <Loader2 className="w-4 h-4" />
                  Retry
                </button>
              )}
            </div>
            {qrError && (
              <p className="text-xs text-amber-600 dark:text-amber-400 mt-2">
                💡 Tip: Try logging out and logging back in to refresh your session
              </p>
            )}
          </div>
        </div>
      </SectionCard>
    </div>
  );
};

export default PatientProfile;
