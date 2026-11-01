/**
 * Doctor Schedule / Profile Management
 * Edit professional profile and manage availability
 */

import { useState, useEffect } from 'react';
import { apiService } from '@/services/api';
import {
  Award, Globe, Save, CheckCircle, AlertCircle, Calendar
} from 'lucide-react';

const SPECIALIZATIONS = [
  'General Practitioner', 'Cardiologist', 'Dermatologist', 'Neurologist',
  'Orthopedic', 'Pediatrician', 'Psychiatrist', 'Gynecologist',
  'Ophthalmologist', 'ENT Specialist', 'Diabetologist', 'Oncologist',
  'Nephrologist', 'Gastroenterologist', 'Pulmonologist'
];

const DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
const LANGUAGES = ['English', 'Hindi', 'Tamil', 'Telugu', 'Kannada', 'Malayalam', 'Marathi', 'Bengali'];

const DoctorSchedule = () => {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState('');
  const [error, setError] = useState('');

  const [form, setForm] = useState({
    specialization: 'General Practitioner',
    years_of_experience: 0,
    license_number: '',
    consultation_fee: 50,
    bio: '',
    is_accepting_patients: true,
    available_days: ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'],
    languages_spoken: ['English'],
    consultation_duration: 30,
    accepts_insurance: true,
  });

  useEffect(() => {
    const load = async () => {
      try {
        const data = await apiService.get('/doctors/profile');
        setProfile(data);
        setForm({
          specialization: data.specialization || 'General Practitioner',
          years_of_experience: data.years_of_experience || 0,
          license_number: data.license_number || '',
          consultation_fee: data.consultation_fee || 50,
          bio: data.bio || '',
          is_accepting_patients: data.is_accepting_patients !== false,
          available_days: data.availability?.filter(a => a.is_available).map(a => a.day) || ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'],
          languages_spoken: data.languages_spoken || ['English'],
          consultation_duration: data.consultation_duration || 30,
          accepts_insurance: data.accepts_insurance !== false,
        });
      } catch {
        // New doctor - use defaults
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const toggleDay = (day) => {
    setForm(f => ({
      ...f,
      available_days: f.available_days.includes(day)
        ? f.available_days.filter(d => d !== day)
        : [...f.available_days, day]
    }));
  };

  const toggleLanguage = (lang) => {
    setForm(f => ({
      ...f,
      languages_spoken: f.languages_spoken.includes(lang)
        ? f.languages_spoken.filter(l => l !== lang)
        : [...f.languages_spoken, lang]
    }));
  };

  const handleSave = async () => {
    setSaving(true);
    setError('');
    setSuccess('');
    try {
      // Build availability array from selected days
      const availability = DAYS.map(day => ({
        day,
        is_available: form.available_days.includes(day),
        time_slots: form.available_days.includes(day)
          ? [
              { start_time: '09:00', end_time: '12:00', slot_duration: form.consultation_duration },
              { start_time: '14:00', end_time: '17:00', slot_duration: form.consultation_duration },
            ]
          : [],
      }));

      await apiService.put('/doctors/profile', {
        specialization: form.specialization,
        years_of_experience: form.years_of_experience,
        consultation_fee: form.consultation_fee,
        bio: form.bio,
        is_accepting_patients: form.is_accepting_patients,
        languages_spoken: form.languages_spoken,
        consultation_duration: form.consultation_duration,
        accepts_insurance: form.accepts_insurance,
        availability,
      });
      setSuccess('Profile updated successfully!');
      setTimeout(() => setSuccess(''), 4000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update profile');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="space-y-4 animate-pulse">
        {[1, 2, 3].map(i => (
          <div key={i} className="h-32 bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700" />
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fade-in max-w-3xl">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-neutral-900 dark:text-white">My Schedule & Profile</h1>
          <p className="text-neutral-500 dark:text-neutral-400 mt-1">Update your professional details and availability</p>
        </div>
        <button
          onClick={handleSave}
          disabled={saving}
          className="bg-emerald-500 text-white text-sm font-semibold px-5 py-2.5 rounded-xl hover:bg-emerald-600 transition-colors disabled:opacity-50 flex items-center gap-2"
        >
          <Save className="w-4 h-4" />
          {saving ? 'Saving...' : 'Save Changes'}
        </button>
      </div>

      {success && (
        <div className="p-4 bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-2xl flex items-center gap-3">
          <CheckCircle className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
          <span className="text-emerald-700 dark:text-emerald-300 text-sm font-medium">{success}</span>
        </div>
      )}
      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-2xl flex items-center gap-3">
          <AlertCircle className="w-5 h-5 text-red-600" />
          <span className="text-red-700 text-sm font-medium">{error}</span>
        </div>
      )}

      {/* Availability Toggle */}
      <div className="bg-white dark:bg-neutral-800 rounded-2xl p-5 border border-neutral-200 dark:border-neutral-700 shadow-sm">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="font-bold text-neutral-900 dark:text-white">Accepting Patients</h2>
            <p className="text-sm text-neutral-500 dark:text-neutral-400 mt-0.5">Toggle to accept or pause new appointments</p>
          </div>
          <button
            onClick={() => setForm(f => ({ ...f, is_accepting_patients: !f.is_accepting_patients }))}
            className={`relative w-14 h-7 rounded-full transition-colors ${form.is_accepting_patients ? 'bg-emerald-500' : 'bg-neutral-300 dark:bg-neutral-600'}`}
          >
            <span className={`absolute top-1 w-5 h-5 bg-white rounded-full shadow transition-transform ${form.is_accepting_patients ? 'translate-x-8' : 'translate-x-1'}`} />
          </button>
        </div>
      </div>

      {/* Professional Info */}
      <div className="bg-white dark:bg-neutral-800 rounded-2xl p-6 border border-neutral-200 dark:border-neutral-700 shadow-sm space-y-4">
        <h2 className="font-bold text-neutral-900 dark:text-white flex items-center gap-2">
          <Award className="w-5 h-5 text-emerald-500" /> Professional Information
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">Specialization</label>
            <select
              value={form.specialization}
              onChange={e => setForm(f => ({ ...f, specialization: e.target.value }))}
              className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white"
            >
              {SPECIALIZATIONS.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">Experience (years)</label>
            <input
              type="number" min={0}
              value={form.years_of_experience}
              onChange={e => setForm(f => ({ ...f, years_of_experience: parseInt(e.target.value) || 0 }))}
              className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">Consultation Fee ($)</label>
            <input
              type="number" min={0}
              value={form.consultation_fee}
              onChange={e => setForm(f => ({ ...f, consultation_fee: parseFloat(e.target.value) || 0 }))}
              className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">Session Duration (min)</label>
            <select
              value={form.consultation_duration}
              onChange={e => setForm(f => ({ ...f, consultation_duration: parseInt(e.target.value) }))}
              className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white"
            >
              {[15, 20, 30, 45, 60].map(d => <option key={d} value={d}>{d} minutes</option>)}
            </select>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">Professional Bio</label>
          <textarea
            value={form.bio}
            onChange={e => setForm(f => ({ ...f, bio: e.target.value }))}
            placeholder="Brief professional biography..."
            rows={3}
            className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white resize-none"
          />
        </div>

        <div className="flex items-center gap-3">
          <input
            type="checkbox"
            id="insurance"
            checked={form.accepts_insurance}
            onChange={e => setForm(f => ({ ...f, accepts_insurance: e.target.checked }))}
            className="w-4 h-4 rounded accent-primary-500"
          />
          <label htmlFor="insurance" className="text-sm font-medium text-neutral-700 dark:text-neutral-300">Accepts Health Insurance</label>
        </div>
      </div>

      {/* Schedule */}
      <div className="bg-white dark:bg-neutral-800 rounded-2xl p-6 border border-neutral-200 dark:border-neutral-700 shadow-sm space-y-4">
        <h2 className="font-bold text-neutral-900 dark:text-white flex items-center gap-2">
          <Calendar className="w-5 h-5 text-blue-500" /> Working Days
        </h2>
        <div className="flex flex-wrap gap-2">
          {DAYS.map(day => (
            <button
              key={day}
              type="button"
              onClick={() => toggleDay(day)}
              className={`px-4 py-2 rounded-xl text-sm font-medium transition-colors capitalize ${
                form.available_days.includes(day)
                  ? 'bg-blue-500 text-white'
                  : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'
              }`}
            >
              {day.slice(0, 3)}
            </button>
          ))}
        </div>
      </div>

      {/* Languages */}
      <div className="bg-white dark:bg-neutral-800 rounded-2xl p-6 border border-neutral-200 dark:border-neutral-700 shadow-sm">
        <h2 className="font-bold text-neutral-900 dark:text-white flex items-center gap-2 mb-4">
          <Globe className="w-5 h-5 text-violet-500" /> Languages Spoken
        </h2>
        <div className="flex flex-wrap gap-2">
          {LANGUAGES.map(lang => (
            <button
              key={lang}
              type="button"
              onClick={() => toggleLanguage(lang)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                form.languages_spoken.includes(lang)
                  ? 'bg-violet-500 text-white'
                  : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'
              }`}
            >
              {lang}
            </button>
          ))}
        </div>
      </div>

      <button
        onClick={handleSave}
        disabled={saving}
        className="w-full bg-emerald-500 text-white font-semibold py-3 rounded-xl hover:bg-emerald-600 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
      >
        <Save className="w-5 h-5" />
        {saving ? 'Saving...' : 'Save All Changes'}
      </button>
    </div>
  );
};

export default DoctorSchedule;
