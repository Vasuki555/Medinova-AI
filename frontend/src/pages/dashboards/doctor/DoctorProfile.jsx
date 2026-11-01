/**
 * Doctor Profile Edit Page
 * Doctor can edit their professional profile, availability, and fees
 */

import { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { apiService } from '@/services/api';
import {
  Stethoscope, Save, Loader2, CheckCircle, AlertCircle,
  QrCode, Download, Clock, DollarSign, Languages,
  Edit2
} from 'lucide-react';
import { API_BASE_URL } from '@/utils/constants';

const SPECIALIZATIONS = [
  'General Practitioner', 'Cardiologist', 'Dermatologist', 'Neurologist',
  'Orthopedic', 'Pediatrician', 'Psychiatrist', 'Gynecologist',
  'Ophthalmologist', 'ENT Specialist', 'Diabetologist', 'Radiologist',
  'Oncologist', 'Gastroenterologist', 'Urologist', 'Endocrinologist',
  'Pulmonologist', 'Rheumatologist', 'Nephrologist', 'Hematologist'
];

const DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

const inputCls = "w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white transition-colors disabled:opacity-60 disabled:cursor-not-allowed";

const FormField = ({ label, required, children }) => (
  <div>
    <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">
      {label} {required && <span className="text-red-500">*</span>}
    </label>
    {children}
  </div>
);

const SectionCard = ({ title, icon: Icon, iconColor = 'text-primary-500 bg-primary-50 dark:bg-primary-900/30', children }) => (
  <div className="bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 shadow-sm overflow-hidden">
    <div className="flex items-center gap-3 px-6 py-4 border-b border-neutral-100 dark:border-neutral-700">
      <div className={`w-8 h-8 rounded-xl flex items-center justify-center ${iconColor}`}>
        <Icon className="w-4 h-4" />
      </div>
      <h2 className="font-bold text-neutral-900 dark:text-white">{title}</h2>
    </div>
    <div className="p-6">{children}</div>
  </div>
);

const DoctorProfile = () => {
  const { user } = useAuth();

  const [profile, setProfile] = useState({
    specialization: 'General Practitioner',
    bio: '',
    years_of_experience: '',
    consultation_fee: '',
    consultation_duration: 30,
    languages_spoken: ['English'],
    availability: [],
    license_number: '',
    license_state: '',
    qualifications: '',
    accepts_insurance: true,
    is_accepting_patients: true,
  });

  const [loading, setLoading] = useState(true);
  const [editingProfessional, setEditingProfessional] = useState(false);
  const [editingConsultation, setEditingConsultation] = useState(false);
  const [editingAvailability, setEditingAvailability] = useState(false);
  const [editingLanguages, setEditingLanguages] = useState(false);
  
  const [savingProfessional, setSavingProfessional] = useState(false);
  const [savingConsultation, setSavingConsultation] = useState(false);
  const [savingAvailability, setSavingAvailability] = useState(false);
  const [savingLanguages, setSavingLanguages] = useState(false);
  
  const [professionalSuccess, setProfessionalSuccess] = useState('');
  const [professionalError, setProfessionalError] = useState('');
  const [consultationSuccess, setConsultationSuccess] = useState('');
  const [consultationError, setConsultationError] = useState('');
  const [availabilitySuccess, setAvailabilitySuccess] = useState('');
  const [availabilityError, setAvailabilityError] = useState('');
  const [languagesSuccess, setLanguagesSuccess] = useState('');
  const [languagesError, setLanguagesError] = useState('');
  
  const [langInput, setLangInput] = useState('');

  // QR download
  const [qrSrc, setQrSrc] = useState('');
  const [qrLoading, setQrLoading] = useState(true);
  const [qrError, setQrError] = useState('');

  useEffect(() => {
    const loadProfile = async () => {
      try {
        const data = await apiService.get('/doctors/profile');
        setProfile({
          specialization: data.specialization || 'General Practitioner',
          bio: data.bio || '',
          years_of_experience: data.years_of_experience ?? '',
          consultation_fee: data.consultation_fee ?? '',
          consultation_duration: data.consultation_duration || 30,
          languages_spoken: data.languages_spoken || ['English'],
          availability: data.availability || [],
          license_number: data.license_number || '',
          license_state: data.license_state || '',
          qualifications: Array.isArray(data.qualifications) ? data.qualifications.join(', ') : '',
          accepts_insurance: data.accepts_insurance ?? true,
          is_accepting_patients: data.is_accepting_patients ?? true,
        });
      } catch (err) {
        // Profile may not be set yet
      } finally {
        setLoading(false);
      }
    };
    loadProfile();
  }, []);

  // Load doctor QR
  useEffect(() => {
    if (!user?._id) {
      console.log('Doctor QR: No user ID available yet');
      return;
    }
    
    const loadQR = async () => {
      try {
        console.log('Doctor QR: Loading for user', user._id);
        const token = localStorage.getItem('accessToken');
        if (!token) {
          console.error('Doctor QR: No access token found');
          setQrError('Please log in again');
          setQrLoading(false);
          return;
        }
        
        const baseUrl = API_BASE_URL.replace('/api/v1', '');
        const url = `${baseUrl}/api/v1/qr/doctor/${user._id}`;
        console.log('Doctor QR: Fetching from', url);
        
        const response = await fetch(url, {
          headers: { 
            'Authorization': `Bearer ${token}`,
            'Accept': 'image/png'
          }
        });
        
        console.log('Doctor QR: Response status', response.status);
        
        if (response.status === 401) {
          setQrError('Session expired. Please log out and log back in.');
          setQrLoading(false);
          return;
        }
        
        if (!response.ok) {
          const text = await response.text();
          console.error('Doctor QR: Error response', text);
          setQrError('Failed to load QR code');
          setQrLoading(false);
          return;
        }
        
        const blob = await response.blob();
        console.log('Doctor QR: Received blob', blob.size, 'bytes');
        setQrSrc(URL.createObjectURL(blob));
        setQrError('');
      } catch (err) {
        console.error('Doctor QR load error:', err);
        setQrError('Failed to load QR code');
      } finally {
        setQrLoading(false);
      }
    };
    
    // Add delay to ensure user is loaded
    const timer = setTimeout(loadQR, 500);
    return () => clearTimeout(timer);
  }, [user]);

  const toggleDay = (day) => {
    setProfile(p => {
      const existing = p.availability.find(a => a.day === day);
      if (existing) {
        return { ...p, availability: p.availability.filter(a => a.day !== day) };
      } else {
        return {
          ...p,
          availability: [...p.availability, { day, start_time: '09:00', end_time: '17:00' }]
        };
      }
    });
  };

  const addLanguage = () => {
    const lang = langInput.trim();
    if (lang && !profile.languages_spoken.includes(lang)) {
      setProfile(p => ({ ...p, languages_spoken: [...p.languages_spoken, lang] }));
    }
    setLangInput('');
  };

  const removeLanguage = (lang) => {
    setProfile(p => ({ ...p, languages_spoken: p.languages_spoken.filter(l => l !== lang) }));
  };

  const handleError = (err) => {
    const errorDetail = err.response?.data?.detail;
    if (Array.isArray(errorDetail)) {
      return errorDetail.map(e => e.msg || JSON.stringify(e)).join(', ');
    } else if (typeof errorDetail === 'string') {
      return errorDetail;
    }
    return 'Failed to update profile';
  };

  const saveProfessional = async (e) => {
    e.preventDefault();
    setSavingProfessional(true);
    setProfessionalError('');
    setProfessionalSuccess('');
    try {
      const payload = {
        ...profile,
        years_of_experience: profile.years_of_experience ? parseInt(profile.years_of_experience) : 0,
        consultation_fee: profile.consultation_fee ? parseFloat(profile.consultation_fee) : 0,
        qualifications: profile.qualifications
          ? profile.qualifications.split(',').map(s => s.trim()).filter(Boolean)
          : [],
      };
      await apiService.put('/doctors/profile', payload);
      setProfessionalSuccess('Professional details updated successfully!');
      setEditingProfessional(false);
      setTimeout(() => setProfessionalSuccess(''), 3000);
    } catch (err) {
      setProfessionalError(handleError(err));
    } finally {
      setSavingProfessional(false);
    }
  };

  const saveConsultation = async (e) => {
    e.preventDefault();
    setSavingConsultation(true);
    setConsultationError('');
    setConsultationSuccess('');
    try {
      const payload = {
        ...profile,
        years_of_experience: profile.years_of_experience ? parseInt(profile.years_of_experience) : 0,
        consultation_fee: profile.consultation_fee ? parseFloat(profile.consultation_fee) : 0,
        qualifications: profile.qualifications
          ? profile.qualifications.split(',').map(s => s.trim()).filter(Boolean)
          : [],
      };
      await apiService.put('/doctors/profile', payload);
      setConsultationSuccess('Consultation settings updated successfully!');
      setEditingConsultation(false);
      setTimeout(() => setConsultationSuccess(''), 3000);
    } catch (err) {
      setConsultationError(handleError(err));
    } finally {
      setSavingConsultation(false);
    }
  };

  const saveAvailability = async (e) => {
    e.preventDefault();
    setSavingAvailability(true);
    setAvailabilityError('');
    setAvailabilitySuccess('');
    try {
      const payload = {
        ...profile,
        years_of_experience: profile.years_of_experience ? parseInt(profile.years_of_experience) : 0,
        consultation_fee: profile.consultation_fee ? parseFloat(profile.consultation_fee) : 0,
        qualifications: profile.qualifications
          ? profile.qualifications.split(',').map(s => s.trim()).filter(Boolean)
          : [],
      };
      await apiService.put('/doctors/profile', payload);
      setAvailabilitySuccess('Availability updated successfully!');
      setEditingAvailability(false);
      setTimeout(() => setAvailabilitySuccess(''), 3000);
    } catch (err) {
      setAvailabilityError(handleError(err));
    } finally {
      setSavingAvailability(false);
    }
  };

  const saveLanguages = async (e) => {
    e.preventDefault();
    setSavingLanguages(true);
    setLanguagesError('');
    setLanguagesSuccess('');
    try {
      const payload = {
        ...profile,
        years_of_experience: profile.years_of_experience ? parseInt(profile.years_of_experience) : 0,
        consultation_fee: profile.consultation_fee ? parseFloat(profile.consultation_fee) : 0,
        qualifications: profile.qualifications
          ? profile.qualifications.split(',').map(s => s.trim()).filter(Boolean)
          : [],
      };
      await apiService.put('/doctors/profile', payload);
      setLanguagesSuccess('Languages updated successfully!');
      setEditingLanguages(false);
      setTimeout(() => setLanguagesSuccess(''), 3000);
    } catch (err) {
      setLanguagesError(handleError(err));
    } finally {
      setSavingLanguages(false);
    }
  };

  const downloadQR = async () => {
    try {
      const token = localStorage.getItem('accessToken');
      const baseUrl = API_BASE_URL.replace('/api/v1', '');
      const res = await fetch(`${baseUrl}/api/v1/qr/doctor/${user._id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!res.ok) throw new Error('Failed to download QR');
      const blob = await res.blob();
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `MediNova_Doctor_QR_${user.first_name}.png`;
      link.click();
    } catch (err) { 
      alert('Could not download QR code. Please try logging out and back in.');
    }
  };

  const refreshQR = () => {
    setQrLoading(true);
    setQrError('');
    setQrSrc('');
    
    const loadQR = async () => {
      try {
        const token = localStorage.getItem('accessToken');
        if (!token) {
          setQrError('Please log out and log back in');
          setQrLoading(false);
          return;
        }
        
        const baseUrl = API_BASE_URL.replace('/api/v1', '');
        const url = `${baseUrl}/api/v1/qr/doctor/${user._id}`;
        
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

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 text-primary-400 animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center gap-4">
        <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-500 flex items-center justify-center text-white text-2xl font-bold shadow-lg">
          Dr
        </div>
        <div>
          <h1 className="text-2xl font-bold text-neutral-900 dark:text-white">
            Dr. {user?.first_name} {user?.last_name}
          </h1>
          <p className="text-emerald-500 font-medium text-sm">{profile.specialization}</p>
          <p className="text-neutral-400 text-xs">{user?.email}</p>
        </div>
      </div>

      {/* Professional Details */}
      <SectionCard title="Professional Details" icon={Stethoscope}>
        {!editingProfessional ? (
          <div className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <div>
                <label className="block text-xs font-medium text-neutral-500 dark:text-neutral-400 mb-1">Specialization</label>
                <p className="text-sm font-medium text-neutral-900 dark:text-white">{profile.specialization}</p>
              </div>
              <div>
                <label className="block text-xs font-medium text-neutral-500 dark:text-neutral-400 mb-1">Years of Experience</label>
                <p className="text-sm font-medium text-neutral-900 dark:text-white">{profile.years_of_experience || '—'}</p>
              </div>
              <div>
                <label className="block text-xs font-medium text-neutral-500 dark:text-neutral-400 mb-1">License Number</label>
                <p className="text-sm font-medium text-neutral-900 dark:text-white">{profile.license_number || '—'}</p>
              </div>
              <div>
                <label className="block text-xs font-medium text-neutral-500 dark:text-neutral-400 mb-1">License State/Country</label>
                <p className="text-sm font-medium text-neutral-900 dark:text-white">{profile.license_state || '—'}</p>
              </div>
              <div className="col-span-2">
                <label className="block text-xs font-medium text-neutral-500 dark:text-neutral-400 mb-1">Qualifications</label>
                <p className="text-sm text-neutral-900 dark:text-white">{profile.qualifications || '—'}</p>
              </div>
              <div className="col-span-2">
                <label className="block text-xs font-medium text-neutral-500 dark:text-neutral-400 mb-1">Professional Bio</label>
                <p className="text-sm text-neutral-900 dark:text-white whitespace-pre-wrap">{profile.bio || '—'}</p>
              </div>
            </div>

            {professionalSuccess && (
              <div className="flex items-center gap-2 p-3 bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-xl text-sm text-emerald-600 dark:text-emerald-400">
                <CheckCircle className="w-4 h-4 flex-shrink-0" /> {professionalSuccess}
              </div>
            )}

            <button
              onClick={() => setEditingProfessional(true)}
              className="flex items-center gap-2 bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold px-5 py-2.5 rounded-xl transition-colors"
            >
              <Edit2 className="w-4 h-4" />
              Edit Professional Details
            </button>
          </div>
        ) : (
          <form onSubmit={saveProfessional} className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <FormField label="Specialization" required>
                <select
                  value={profile.specialization}
                  onChange={e => setProfile(p => ({ ...p, specialization: e.target.value }))}
                  className={inputCls}
                >
                  {SPECIALIZATIONS.map(s => <option key={s} value={s}>{s}</option>)}
                </select>
              </FormField>
              <FormField label="Years of Experience">
                <input
                  type="number"
                  value={profile.years_of_experience}
                  onChange={e => setProfile(p => ({ ...p, years_of_experience: e.target.value }))}
                  placeholder="5"
                  min="0" max="60"
                  className={inputCls}
                />
              </FormField>
              <FormField label="License Number">
                <input
                  type="text"
                  value={profile.license_number}
                  onChange={e => setProfile(p => ({ ...p, license_number: e.target.value }))}
                  placeholder="MED-1234567"
                  className={inputCls}
                />
              </FormField>
              <FormField label="License State/Country">
                <input
                  type="text"
                  value={profile.license_state}
                  onChange={e => setProfile(p => ({ ...p, license_state: e.target.value }))}
                  placeholder="e.g., California, India"
                  className={inputCls}
                />
              </FormField>
              <div className="col-span-2">
                <FormField label="Qualifications (comma-separated)">
                  <input
                    type="text"
                    value={profile.qualifications}
                    onChange={e => setProfile(p => ({ ...p, qualifications: e.target.value }))}
                    placeholder="MBBS, MD, FRCS..."
                    className={inputCls}
                  />
                </FormField>
              </div>
              <div className="col-span-2">
                <FormField label="Professional Bio">
                  <textarea
                    value={profile.bio}
                    onChange={e => setProfile(p => ({ ...p, bio: e.target.value }))}
                    placeholder="Tell patients about your expertise, approach to care..."
                    rows={4}
                    className={`${inputCls} resize-none`}
                  />
                </FormField>
              </div>
            </div>

            {professionalError && (
              <div className="flex items-center gap-2 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl text-sm text-red-600 dark:text-red-400">
                <AlertCircle className="w-4 h-4 flex-shrink-0" /> {professionalError}
              </div>
            )}

            <div className="flex gap-3">
              <button
                type="submit"
                disabled={savingProfessional}
                className="flex items-center gap-2 bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold px-5 py-2.5 rounded-xl transition-colors disabled:opacity-50"
              >
                {savingProfessional ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
                Save Changes
              </button>
              <button
                type="button"
                onClick={() => {
                  setEditingProfessional(false);
                  setProfessionalError('');
                }}
                className="px-5 py-2.5 border border-neutral-300 dark:border-neutral-600 text-neutral-700 dark:text-neutral-300 text-sm font-semibold rounded-xl hover:bg-neutral-50 dark:hover:bg-neutral-700 transition-colors"
              >
                Cancel
              </button>
            </div>
          </form>
        )}
      </SectionCard>

      {/* Consultation Settings */}
      <SectionCard title="Consultation Settings" icon={DollarSign} iconColor="text-emerald-500 bg-emerald-50 dark:bg-emerald-900/30">
        {!editingConsultation ? (
          <div className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
              <div>
                <label className="block text-xs font-medium text-neutral-500 dark:text-neutral-400 mb-1">Consultation Fee</label>
                <p className="text-sm font-medium text-neutral-900 dark:text-white">${profile.consultation_fee || 0}</p>
              </div>
              <div>
                <label className="block text-xs font-medium text-neutral-500 dark:text-neutral-400 mb-1">Duration</label>
                <p className="text-sm font-medium text-neutral-900 dark:text-white">{profile.consultation_duration} minutes</p>
              </div>
              <div>
                <label className="block text-xs font-medium text-neutral-500 dark:text-neutral-400 mb-1">Status</label>
                <div className="flex flex-col gap-1">
                  <p className="text-sm text-neutral-900 dark:text-white">
                    Insurance: {profile.accepts_insurance ? '✓ Accepted' : '✗ Not Accepted'}
                  </p>
                  <p className="text-sm text-neutral-900 dark:text-white">
                    New Patients: {profile.is_accepting_patients ? '✓ Accepting' : '✗ Not Accepting'}
                  </p>
                </div>
              </div>
            </div>

            {consultationSuccess && (
              <div className="flex items-center gap-2 p-3 bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-xl text-sm text-emerald-600 dark:text-emerald-400">
                <CheckCircle className="w-4 h-4 flex-shrink-0" /> {consultationSuccess}
              </div>
            )}

            <button
              onClick={() => setEditingConsultation(true)}
              className="flex items-center gap-2 bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold px-5 py-2.5 rounded-xl transition-colors"
            >
              <Edit2 className="w-4 h-4" />
              Edit Consultation Settings
            </button>
          </div>
        ) : (
          <form onSubmit={saveConsultation} className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <FormField label="Consultation Fee ($)">
                <input
                  type="number"
                  value={profile.consultation_fee}
                  onChange={e => setProfile(p => ({ ...p, consultation_fee: e.target.value }))}
                  placeholder="50"
                  min="0"
                  className={inputCls}
                />
              </FormField>
              <FormField label="Duration (minutes)">
                <select
                  value={profile.consultation_duration}
                  onChange={e => setProfile(p => ({ ...p, consultation_duration: parseInt(e.target.value) }))}
                  className={inputCls}
                >
                  {[15, 20, 30, 45, 60, 90].map(d => (
                    <option key={d} value={d}>{d} min</option>
                  ))}
                </select>
              </FormField>
              <div className="flex flex-col gap-3 pt-6">
                <label className="flex items-center gap-3 cursor-pointer">
                  <div
                    onClick={() => setProfile(p => ({ ...p, accepts_insurance: !p.accepts_insurance }))}
                    className={`w-11 h-6 rounded-full transition-colors relative ${profile.accepts_insurance ? 'bg-primary-500' : 'bg-neutral-300 dark:bg-neutral-600'}`}
                  >
                    <div className={`w-5 h-5 bg-white rounded-full shadow absolute top-0.5 transition-transform ${profile.accepts_insurance ? 'translate-x-5' : 'translate-x-0.5'}`} />
                  </div>
                  <span className="text-sm text-neutral-700 dark:text-neutral-300">Accepts Insurance</span>
                </label>
                <label className="flex items-center gap-3 cursor-pointer">
                  <div
                    onClick={() => setProfile(p => ({ ...p, is_accepting_patients: !p.is_accepting_patients }))}
                    className={`w-11 h-6 rounded-full transition-colors relative ${profile.is_accepting_patients ? 'bg-emerald-500' : 'bg-neutral-300 dark:bg-neutral-600'}`}
                  >
                    <div className={`w-5 h-5 bg-white rounded-full shadow absolute top-0.5 transition-transform ${profile.is_accepting_patients ? 'translate-x-5' : 'translate-x-0.5'}`} />
                  </div>
                  <span className="text-sm text-neutral-700 dark:text-neutral-300">Accepting New Patients</span>
                </label>
              </div>
            </div>

            {consultationError && (
              <div className="flex items-center gap-2 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl text-sm text-red-600 dark:text-red-400">
                <AlertCircle className="w-4 h-4 flex-shrink-0" /> {consultationError}
              </div>
            )}

            <div className="flex gap-3">
              <button
                type="submit"
                disabled={savingConsultation}
                className="flex items-center gap-2 bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold px-5 py-2.5 rounded-xl transition-colors disabled:opacity-50"
              >
                {savingConsultation ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
                Save Changes
              </button>
              <button
                type="button"
                onClick={() => {
                  setEditingConsultation(false);
                  setConsultationError('');
                }}
                className="px-5 py-2.5 border border-neutral-300 dark:border-neutral-600 text-neutral-700 dark:text-neutral-300 text-sm font-semibold rounded-xl hover:bg-neutral-50 dark:hover:bg-neutral-700 transition-colors"
              >
                Cancel
              </button>
            </div>
          </form>
        )}
      </SectionCard>

      {/* Availability */}
      <SectionCard title="Weekly Availability" icon={Clock} iconColor="text-blue-500 bg-blue-50 dark:bg-blue-900/30">
        {!editingAvailability ? (
          <div className="space-y-4">
            {profile.availability.length > 0 ? (
              <div className="space-y-2">
                {profile.availability.map((slot) => (
                  <div key={slot.day} className="flex items-center justify-between p-3 bg-neutral-50 dark:bg-neutral-700/40 rounded-xl">
                    <span className="text-sm font-medium text-neutral-700 dark:text-neutral-300">{slot.day}</span>
                    <span className="text-sm text-neutral-600 dark:text-neutral-400">
                      {slot.start_time} - {slot.end_time}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-neutral-500 italic">No availability set</p>
            )}

            {availabilitySuccess && (
              <div className="flex items-center gap-2 p-3 bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-xl text-sm text-emerald-600 dark:text-emerald-400">
                <CheckCircle className="w-4 h-4 flex-shrink-0" /> {availabilitySuccess}
              </div>
            )}

            <button
              onClick={() => setEditingAvailability(true)}
              className="flex items-center gap-2 bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold px-5 py-2.5 rounded-xl transition-colors"
            >
              <Edit2 className="w-4 h-4" />
              Edit Availability
            </button>
          </div>
        ) : (
          <form onSubmit={saveAvailability} className="space-y-4">
            <div className="flex flex-wrap gap-2 mb-4">
              {DAYS.map(day => {
                const isSelected = profile.availability.some(a => a.day === day);
                return (
                  <button
                    key={day}
                    type="button"
                    onClick={() => toggleDay(day)}
                    className={`px-3 py-1.5 rounded-xl text-sm font-medium transition-colors ${
                      isSelected
                        ? 'bg-primary-500 text-white'
                        : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'
                    }`}
                  >
                    {day.slice(0, 3)}
                  </button>
                );
              })}
            </div>
            {profile.availability.length > 0 && (
              <div className="space-y-2">
                {profile.availability.map((slot, i) => (
                  <div key={slot.day} className="flex items-center gap-3 p-2 bg-neutral-50 dark:bg-neutral-700/40 rounded-xl">
                    <span className="text-sm font-medium text-neutral-700 dark:text-neutral-300 w-24">{slot.day}</span>
                    <input
                      type="time"
                      value={slot.start_time}
                      onChange={e => {
                        const updated = [...profile.availability];
                        updated[i] = { ...updated[i], start_time: e.target.value };
                        setProfile(p => ({ ...p, availability: updated }));
                      }}
                      className="text-sm border border-neutral-300 dark:border-neutral-600 rounded-lg px-2 py-1 dark:bg-neutral-700 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                    />
                    <span className="text-xs text-neutral-400">to</span>
                    <input
                      type="time"
                      value={slot.end_time}
                      onChange={e => {
                        const updated = [...profile.availability];
                        updated[i] = { ...updated[i], end_time: e.target.value };
                        setProfile(p => ({ ...p, availability: updated }));
                      }}
                      className="text-sm border border-neutral-300 dark:border-neutral-600 rounded-lg px-2 py-1 dark:bg-neutral-700 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                    />
                  </div>
                ))}
              </div>
            )}

            {availabilityError && (
              <div className="flex items-center gap-2 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl text-sm text-red-600 dark:text-red-400">
                <AlertCircle className="w-4 h-4 flex-shrink-0" /> {availabilityError}
              </div>
            )}

            <div className="flex gap-3">
              <button
                type="submit"
                disabled={savingAvailability}
                className="flex items-center gap-2 bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold px-5 py-2.5 rounded-xl transition-colors disabled:opacity-50"
              >
                {savingAvailability ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
                Save Changes
              </button>
              <button
                type="button"
                onClick={() => {
                  setEditingAvailability(false);
                  setAvailabilityError('');
                }}
                className="px-5 py-2.5 border border-neutral-300 dark:border-neutral-600 text-neutral-700 dark:text-neutral-300 text-sm font-semibold rounded-xl hover:bg-neutral-50 dark:hover:bg-neutral-700 transition-colors"
              >
                Cancel
              </button>
            </div>
          </form>
        )}
      </SectionCard>

      {/* Languages */}
      <SectionCard title="Languages Spoken" icon={Languages} iconColor="text-violet-500 bg-violet-50 dark:bg-violet-900/30">
        {!editingLanguages ? (
          <div className="space-y-4">
            <div className="flex flex-wrap gap-2">
              {profile.languages_spoken.map(lang => (
                <span key={lang} className="text-sm bg-violet-100 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300 px-3 py-1 rounded-xl">
                  {lang}
                </span>
              ))}
            </div>

            {languagesSuccess && (
              <div className="flex items-center gap-2 p-3 bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-xl text-sm text-emerald-600 dark:text-emerald-400">
                <CheckCircle className="w-4 h-4 flex-shrink-0" /> {languagesSuccess}
              </div>
            )}

            <button
              onClick={() => setEditingLanguages(true)}
              className="flex items-center gap-2 bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold px-5 py-2.5 rounded-xl transition-colors"
            >
              <Edit2 className="w-4 h-4" />
              Edit Languages
            </button>
          </div>
        ) : (
          <form onSubmit={saveLanguages} className="space-y-4">
            <div className="flex flex-wrap gap-2 mb-3">
              {profile.languages_spoken.map(lang => (
                <span key={lang} className="flex items-center gap-1.5 text-sm bg-violet-100 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300 px-3 py-1 rounded-xl">
                  {lang}
                  {lang !== 'English' && (
                    <button type="button" onClick={() => removeLanguage(lang)} className="hover:text-red-500 transition-colors text-xs">×</button>
                  )}
                </span>
              ))}
            </div>
            <div className="flex gap-2">
              <input
                type="text"
                value={langInput}
                onChange={e => setLangInput(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && (e.preventDefault(), addLanguage())}
                placeholder="Add a language..."
                className={`${inputCls} flex-1`}
              />
              <button
                type="button"
                onClick={addLanguage}
                className="px-4 py-2 bg-violet-500 hover:bg-violet-600 text-white text-sm font-medium rounded-xl transition-colors"
              >
                Add
              </button>
            </div>

            {languagesError && (
              <div className="flex items-center gap-2 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl text-sm text-red-600 dark:text-red-400">
                <AlertCircle className="w-4 h-4 flex-shrink-0" /> {languagesError}
              </div>
            )}

            <div className="flex gap-3">
              <button
                type="submit"
                disabled={savingLanguages}
                className="flex items-center gap-2 bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold px-5 py-2.5 rounded-xl transition-colors disabled:opacity-50"
              >
                {savingLanguages ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
                Save Changes
              </button>
              <button
                type="button"
                onClick={() => {
                  setEditingLanguages(false);
                  setLanguagesError('');
                }}
                className="px-5 py-2.5 border border-neutral-300 dark:border-neutral-600 text-neutral-700 dark:text-neutral-300 text-sm font-semibold rounded-xl hover:bg-neutral-50 dark:hover:bg-neutral-700 transition-colors"
              >
                Cancel
              </button>
            </div>
          </form>
        )}
      </SectionCard>

      {/* Doctor QR Code */}
      <SectionCard title="Your Doctor QR Code" icon={QrCode} iconColor="text-cyan-500 bg-cyan-50 dark:bg-cyan-900/30">
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
              <img src={qrSrc} alt="Doctor QR" className="w-full h-full object-contain p-2" />
            ) : (
              <div className="text-center p-2">
                <QrCode className="w-10 h-10 text-neutral-300 mx-auto mb-2" />
                <p className="text-xs text-neutral-500">QR not loaded</p>
              </div>
            )}
          </div>
          <div className="flex-1">
            <p className="font-semibold text-neutral-900 dark:text-white mb-1">Share Your QR Code</p>
            <p className="text-sm text-neutral-500 dark:text-neutral-400 mb-3">
              Print or display this QR code at your clinic. Patients can scan it to instantly open your booking page.
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
                  className="flex items-center gap-2 bg-cyan-500 hover:bg-cyan-600 text-white text-sm font-semibold px-4 py-2 rounded-xl transition-colors"
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

export default DoctorProfile;
