/**
 * Book Appointment Page
 * Patients can search for doctors and book appointments
 */

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiService } from '@/services/api';
import {
  Search, Star, Clock, MapPin, Video, Calendar,
  Filter, ChevronRight, User, Stethoscope, X
} from 'lucide-react';

const SPECIALIZATIONS = [
  'All', 'General Practitioner', 'Cardiologist', 'Dermatologist',
  'Neurologist', 'Orthopedic', 'Pediatrician', 'Psychiatrist',
  'Gynecologist', 'Ophthalmologist', 'ENT Specialist', 'Diabetologist'
];

const DoctorCard = ({ doctor, onBook }) => (
  <div className="bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 p-5 hover:shadow-lg transition-shadow">
    <div className="flex items-start gap-4">
      <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center text-white font-bold text-xl flex-shrink-0">
        {(doctor.first_name || 'D')[0]}
      </div>
      <div className="flex-grow min-w-0">
        <h3 className="font-bold text-neutral-900 dark:text-white">
          Dr. {doctor.first_name} {doctor.last_name}
        </h3>
        <p className="text-sm text-primary-500 font-medium">{doctor.specialization || 'General Practitioner'}</p>
        <div className="flex items-center gap-3 mt-2 flex-wrap">
          <span className="flex items-center gap-1 text-xs text-neutral-500">
            <Star className="w-3.5 h-3.5 text-amber-400 fill-amber-400" />
            {doctor.rating?.toFixed(1) || '4.8'} ({doctor.total_consultations || 0} reviews)
          </span>
          <span className="flex items-center gap-1 text-xs text-neutral-500">
            <Clock className="w-3.5 h-3.5" />
            {doctor.years_of_experience || 0} yrs exp
          </span>
          {doctor.hospital_name && (
            <span className="flex items-center gap-1 text-xs text-neutral-500">
              <MapPin className="w-3.5 h-3.5" />
              {doctor.hospital_name}
            </span>
          )}
        </div>
        <div className="flex items-center gap-2 mt-3 flex-wrap">
          {(doctor.languages_spoken || ['English']).map(lang => (
            <span key={lang} className="text-xs bg-neutral-100 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-300 px-2 py-0.5 rounded-md">
              {lang}
            </span>
          ))}
        </div>
      </div>
    </div>
    <div className="flex items-center justify-between mt-4 pt-4 border-t border-neutral-100 dark:border-neutral-700">
      <div>
        <span className="text-lg font-bold text-neutral-900 dark:text-white">
          ${doctor.consultation_fee || 50}
        </span>
        <span className="text-sm text-neutral-400"> / session</span>
      </div>
      <div className="flex gap-2">
        <span className="flex items-center gap-1 text-xs bg-emerald-50 text-emerald-600 px-2 py-1 rounded-lg font-medium">
          <Video className="w-3 h-3" /> Video
        </span>
        <button
          onClick={() => onBook(doctor)}
          className="bg-primary-500 text-white text-sm font-semibold px-4 py-2 rounded-xl hover:bg-primary-600 transition-colors flex items-center gap-1"
        >
          Book <ChevronRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  </div>
);

const BookingModal = ({ doctor, onClose, onBooked }) => {
  const [form, setForm] = useState({
    appointment_date: '',
    type: 'video',
    reason: '',
    symptoms: '',
    duration_minutes: 30,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.appointment_date || !form.reason) {
      setError('Please fill in all required fields');
      return;
    }
    setLoading(true);
    setError('');
    try {
      await apiService.post('/appointments', {
        doctor_id: doctor.user_id,
        appointment_date: new Date(form.appointment_date).toISOString(),
        type: form.type,
        reason: form.reason,
        symptoms: form.symptoms ? form.symptoms.split(',').map(s => s.trim()) : [],
        duration_minutes: form.duration_minutes,
      });
      onBooked();
    } catch (err) {
      setError(err.response?.data?.detail || 'Booking failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white dark:bg-neutral-800 rounded-2xl w-full max-w-md shadow-2xl animate-scale-in">
        <div className="flex items-center justify-between p-6 border-b border-neutral-200 dark:border-neutral-700">
          <div>
            <h2 className="font-bold text-neutral-900 dark:text-white">Book Appointment</h2>
            <p className="text-sm text-neutral-500">Dr. {doctor.first_name} {doctor.last_name}</p>
          </div>
          <button onClick={onClose} className="p-2 hover:bg-neutral-100 dark:hover:bg-neutral-700 rounded-xl transition-colors">
            <X className="w-5 h-5 text-neutral-500" />
          </button>
        </div>
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {error && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-xl text-red-600 text-sm">{error}</div>
          )}
          <div>
            <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">
              Date & Time <span className="text-red-500">*</span>
            </label>
            <input
              type="datetime-local"
              value={form.appointment_date}
              onChange={e => setForm(f => ({ ...f, appointment_date: e.target.value }))}
              min={new Date().toISOString().slice(0, 16)}
              className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">
              Consultation Type
            </label>
            <div className="flex gap-3">
              {['video', 'in_person', 'chat'].map(type => (
                <button
                  key={type}
                  type="button"
                  onClick={() => setForm(f => ({ ...f, type }))}
                  className={`flex-1 py-2 rounded-xl text-sm font-medium border transition-colors ${
                    form.type === type
                      ? 'bg-primary-500 text-white border-primary-500'
                      : 'bg-white dark:bg-neutral-700 text-neutral-600 dark:text-neutral-300 border-neutral-300 dark:border-neutral-600 hover:border-primary-400'
                  }`}
                >
                  {type === 'video' ? '📹 Video' : type === 'in_person' ? '🏥 In-Person' : '💬 Chat'}
                </button>
              ))}
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">
              Reason for Visit <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={form.reason}
              onChange={e => setForm(f => ({ ...f, reason: e.target.value }))}
              placeholder="e.g., Routine checkup, fever, back pain"
              className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">
              Symptoms (comma separated)
            </label>
            <input
              type="text"
              value={form.symptoms}
              onChange={e => setForm(f => ({ ...f, symptoms: e.target.value }))}
              placeholder="e.g., headache, fever, fatigue"
              className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">
              Duration
            </label>
            <select
              value={form.duration_minutes}
              onChange={e => setForm(f => ({ ...f, duration_minutes: Number(e.target.value) }))}
              className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white"
            >
              <option value={15}>15 minutes</option>
              <option value={30}>30 minutes</option>
              <option value={45}>45 minutes</option>
              <option value={60}>60 minutes</option>
            </select>
          </div>
          <div className="pt-2">
            <div className="flex items-center justify-between text-sm mb-3">
              <span className="text-neutral-500">Consultation Fee</span>
              <span className="font-bold text-neutral-900 dark:text-white">${doctor.consultation_fee || 50}</span>
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-primary-500 text-white font-semibold py-3 rounded-xl hover:bg-primary-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Booking...' : 'Confirm Booking'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

const BookAppointment = () => {
  const navigate = useNavigate();
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [specialization, setSpecialization] = useState('All');
  const [selectedDoctor, setSelectedDoctor] = useState(null);
  const [successMsg, setSuccessMsg] = useState('');

  useEffect(() => {
    loadDoctors();
  }, []);

  const loadDoctors = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (search) params.append('search', search);
      if (specialization !== 'All') params.append('specialization', specialization);
      const data = await apiService.get(`/doctors?${params.toString()}`);
      setDoctors(data || []);
    } catch {
      setDoctors([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const timer = setTimeout(loadDoctors, 400);
    return () => clearTimeout(timer);
  }, [search, specialization]);

  const handleBooked = () => {
    setSelectedDoctor(null);
    setSuccessMsg('Appointment booked successfully! Check your notifications.');
    setTimeout(() => setSuccessMsg(''), 5000);
    navigate('/patient/appointments');
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-neutral-900 dark:text-white">Book Appointment</h1>
        <p className="text-neutral-500 dark:text-neutral-400 mt-1">Find and book a consultation with our verified doctors</p>
      </div>

      {successMsg && (
        <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-2xl text-emerald-700 font-medium flex items-center gap-2">
          <span>✓</span> {successMsg}
        </div>
      )}

      {/* Search & Filters */}
      <div className="bg-white dark:bg-neutral-800 rounded-2xl p-5 border border-neutral-200 dark:border-neutral-700 shadow-sm">
        <div className="flex gap-3 mb-4">
          <div className="flex-grow relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-neutral-400" />
            <input
              type="text"
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="Search doctors by name..."
              className="w-full pl-10 pr-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white"
            />
          </div>
        </div>
        <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-hide">
          {SPECIALIZATIONS.map(spec => (
            <button
              key={spec}
              onClick={() => setSpecialization(spec)}
              className={`flex-shrink-0 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                specialization === spec
                  ? 'bg-primary-500 text-white'
                  : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'
              }`}
            >
              {spec}
            </button>
          ))}
        </div>
      </div>

      {/* Doctors Grid */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[1, 2, 3, 4].map(i => (
            <div key={i} className="h-48 bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 animate-pulse" />
          ))}
        </div>
      ) : doctors.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {doctors.map(doc => (
            <DoctorCard key={doc.user_id || doc.id} doctor={doc} onBook={setSelectedDoctor} />
          ))}
        </div>
      ) : (
        <div className="text-center py-16">
          <Stethoscope className="w-12 h-12 text-neutral-300 mx-auto mb-3" />
          <p className="text-neutral-500 font-medium">No doctors found</p>
          <p className="text-neutral-400 text-sm mt-1">Try adjusting your search or filters</p>
        </div>
      )}

      {selectedDoctor && (
        <BookingModal
          doctor={selectedDoctor}
          onClose={() => setSelectedDoctor(null)}
          onBooked={handleBooked}
        />
      )}
    </div>
  );
};

export default BookAppointment;
