/**
 * Doctor - Patient Queue / Appointments
 * Doctor view of all appointments with consultation tools
 */

import { useState, useEffect } from 'react';
import { apiService } from '@/services/api';
import {
  Calendar, Clock, Video, User, CheckCircle, X,
  ChevronDown, ChevronUp, FileText, Stethoscope,
  RefreshCw, Activity
} from 'lucide-react';

const statusColors = {
  scheduled: 'bg-blue-100 text-blue-700',
  confirmed: 'bg-emerald-100 text-emerald-700',
  in_progress: 'bg-amber-100 text-amber-700',
  completed: 'bg-gray-100 text-gray-600',
  cancelled: 'bg-red-100 text-red-600',
};

const ConsultationForm = ({ appointment, onSave, onClose }) => {
  const [form, setForm] = useState({
    notes: '',
    diagnosis: '',
    icd10_codes: '',
    lab_tests_ordered: '',
    imaging_ordered: '',
    follow_up_required: false,
    follow_up_days: '',
    vitals_heart_rate: '',
    vitals_blood_pressure: '',
    vitals_temperature: '',
    vitals_oxygen_saturation: '',
    vitals_weight: '',
  });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  const handleSave = async () => {
    setSaving(true);
    setError('');
    try {
      const vitals = {};
      if (form.vitals_heart_rate) vitals.heart_rate = parseFloat(form.vitals_heart_rate);
      if (form.vitals_blood_pressure) vitals.blood_pressure = form.vitals_blood_pressure;
      if (form.vitals_temperature) vitals.temperature = parseFloat(form.vitals_temperature);
      if (form.vitals_oxygen_saturation) vitals.oxygen_saturation = parseFloat(form.vitals_oxygen_saturation);
      if (form.vitals_weight) vitals.weight = parseFloat(form.vitals_weight);

      const consultation = {
        notes: form.notes,
        diagnosis: form.diagnosis,
        icd10_codes: form.icd10_codes ? form.icd10_codes.split(',').map(c => c.trim()) : [],
        lab_tests_ordered: form.lab_tests_ordered ? form.lab_tests_ordered.split(',').map(t => t.trim()) : [],
        imaging_ordered: form.imaging_ordered ? form.imaging_ordered.split(',').map(t => t.trim()) : [],
        follow_up_required: form.follow_up_required,
        follow_up_days: form.follow_up_days ? parseInt(form.follow_up_days) : null,
        vitals: Object.keys(vitals).length > 0 ? vitals : null,
      };

      await apiService.patch(`/appointments/${appointment.id}/consultation`, { consultation });
      onSave();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save consultation');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white dark:bg-neutral-800 rounded-2xl w-full max-w-lg shadow-2xl animate-scale-in max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between p-6 border-b border-neutral-200 dark:border-neutral-700 sticky top-0 bg-white dark:bg-neutral-800">
          <div>
            <h2 className="font-bold text-neutral-900 dark:text-white">Write Consultation</h2>
            <p className="text-sm text-neutral-500">Patient: {appointment.patient_name}</p>
          </div>
          <button onClick={onClose} className="p-2 hover:bg-neutral-100 dark:hover:bg-neutral-700 rounded-xl">
            <X className="w-5 h-5 text-neutral-500" />
          </button>
        </div>
        <div className="p-6 space-y-4">
          {error && <div className="p-3 bg-red-50 border border-red-200 rounded-xl text-red-600 text-sm">{error}</div>}

          <div>
            <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">Diagnosis</label>
            <input type="text" value={form.diagnosis} onChange={e => setForm(f => ({ ...f, diagnosis: e.target.value }))} placeholder="Primary diagnosis" className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" />
          </div>

          <div>
            <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">Clinical Notes</label>
            <textarea value={form.notes} onChange={e => setForm(f => ({ ...f, notes: e.target.value }))} placeholder="Detailed consultation notes..." rows={4} className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white resize-none" />
          </div>

          <div>
            <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">ICD-10 Codes (comma separated)</label>
            <input type="text" value={form.icd10_codes} onChange={e => setForm(f => ({ ...f, icd10_codes: e.target.value }))} placeholder="e.g., J06.9, Z00.0" className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">Lab Tests Ordered</label>
              <input type="text" value={form.lab_tests_ordered} onChange={e => setForm(f => ({ ...f, lab_tests_ordered: e.target.value }))} placeholder="CBC, LFT, RFT" className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" />
            </div>
            <div>
              <label className="block text-xs font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">Imaging Ordered</label>
              <input type="text" value={form.imaging_ordered} onChange={e => setForm(f => ({ ...f, imaging_ordered: e.target.value }))} placeholder="X-Ray Chest, USG" className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" />
            </div>
          </div>

          {/* Vitals */}
          <div>
            <p className="text-sm font-semibold text-neutral-700 dark:text-neutral-300 mb-2 flex items-center gap-2">
              <Activity className="w-4 h-4 text-rose-500" /> Vitals
            </p>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
              <div>
                <label className="block text-xs text-neutral-500 mb-1">Heart Rate (bpm)</label>
                <input type="number" value={form.vitals_heart_rate} onChange={e => setForm(f => ({ ...f, vitals_heart_rate: e.target.value }))} placeholder="72" className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" />
              </div>
              <div>
                <label className="block text-xs text-neutral-500 mb-1">BP (sys/dia)</label>
                <input type="text" value={form.vitals_blood_pressure} onChange={e => setForm(f => ({ ...f, vitals_blood_pressure: e.target.value }))} placeholder="120/80" className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" />
              </div>
              <div>
                <label className="block text-xs text-neutral-500 mb-1">Temp (°F)</label>
                <input type="number" step="0.1" value={form.vitals_temperature} onChange={e => setForm(f => ({ ...f, vitals_temperature: e.target.value }))} placeholder="98.6" className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" />
              </div>
              <div>
                <label className="block text-xs text-neutral-500 mb-1">SpO₂ (%)</label>
                <input type="number" value={form.vitals_oxygen_saturation} onChange={e => setForm(f => ({ ...f, vitals_oxygen_saturation: e.target.value }))} placeholder="98" className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" />
              </div>
              <div>
                <label className="block text-xs text-neutral-500 mb-1">Weight (kg)</label>
                <input type="number" step="0.1" value={form.vitals_weight} onChange={e => setForm(f => ({ ...f, vitals_weight: e.target.value }))} placeholder="70" className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" />
              </div>
            </div>
          </div>

          {/* Follow up */}
          <div className="flex items-center gap-3">
            <input
              type="checkbox"
              id="followup"
              checked={form.follow_up_required}
              onChange={e => setForm(f => ({ ...f, follow_up_required: e.target.checked }))}
              className="w-4 h-4 rounded accent-primary-500"
            />
            <label htmlFor="followup" className="text-sm font-medium text-neutral-700 dark:text-neutral-300">Follow-up required</label>
            {form.follow_up_required && (
              <input type="number" value={form.follow_up_days} onChange={e => setForm(f => ({ ...f, follow_up_days: e.target.value }))} placeholder="Days" className="w-20 px-3 py-1.5 border border-neutral-300 dark:border-neutral-600 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" />
            )}
          </div>

          <div className="flex gap-3 pt-2">
            <button onClick={onClose} className="flex-1 py-2.5 rounded-xl border border-neutral-300 dark:border-neutral-600 text-neutral-600 dark:text-neutral-400 text-sm font-medium hover:bg-neutral-50 dark:hover:bg-neutral-700 transition-colors">Cancel</button>
            <button
              onClick={handleSave}
              disabled={saving}
              className="flex-1 bg-emerald-500 text-white py-2.5 rounded-xl text-sm font-semibold hover:bg-emerald-600 transition-colors disabled:opacity-50"
            >
              {saving ? 'Saving...' : 'Complete Consultation'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

const AppointmentDetail = ({ apt, onUpdate }) => {
  const [expanded, setExpanded] = useState(false);
  const [showConsultation, setShowConsultation] = useState(false);
  const [updating, setUpdating] = useState(false);
  const config = statusColors[apt.status] || statusColors.scheduled;
  const date = new Date(apt.appointment_date);

  const handleStatusUpdate = async (newStatus) => {
    setUpdating(true);
    try {
      await apiService.patch(`/appointments/${apt.id}/status`, { status: newStatus });
      onUpdate(apt.id, newStatus);
    } catch {
      alert('Status update failed');
    } finally {
      setUpdating(false);
    }
  };

  return (
    <div className="bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 shadow-sm overflow-hidden">
      <div className="flex items-center gap-4 p-5 cursor-pointer" onClick={() => setExpanded(e => !e)}>
        <div className="w-12 h-12 rounded-2xl bg-emerald-50 dark:bg-emerald-900/30 flex flex-col items-center justify-center flex-shrink-0">
          <span className="text-xs font-bold text-emerald-600 uppercase">{date.toLocaleDateString('en', { month: 'short' })}</span>
          <span className="text-lg font-black text-emerald-600">{date.getDate()}</span>
        </div>
        <div className="flex-grow min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <h3 className="font-bold text-neutral-900 dark:text-white">{apt.patient_name || 'Patient'}</h3>
            <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${config}`}>{apt.status}</span>
          </div>
          <p className="text-sm text-neutral-500 dark:text-neutral-400">
            {date.toLocaleTimeString('en', { hour: '2-digit', minute: '2-digit' })} · {apt.reason}
          </p>
          <p className="text-xs text-neutral-400">{apt.type === 'video' ? '📹 Video Call' : apt.type === 'in_person' ? '🏥 In-Person' : '💬 Chat'} · {apt.duration_minutes}min</p>
        </div>
        {expanded ? <ChevronUp className="w-5 h-5 text-neutral-400" /> : <ChevronDown className="w-5 h-5 text-neutral-400" />}
      </div>

      {expanded && (
        <div className="border-t border-neutral-100 dark:border-neutral-700 p-5 space-y-4">
          {apt.symptoms?.length > 0 && (
            <div>
              <p className="text-xs text-neutral-400 uppercase tracking-wide mb-2">Reported Symptoms</p>
              <div className="flex flex-wrap gap-2">
                {apt.symptoms.map(s => (
                  <span key={s} className="text-xs bg-rose-50 dark:bg-rose-900/20 text-rose-600 dark:text-rose-400 px-2 py-0.5 rounded-lg">{s}</span>
                ))}
              </div>
            </div>
          )}

          {apt.consultation && (
            <div className="bg-neutral-50 dark:bg-neutral-700/40 rounded-xl p-4">
              <p className="text-xs font-bold text-neutral-500 uppercase tracking-wide mb-2">Consultation Recorded</p>
              {apt.consultation.diagnosis && <p className="text-sm text-neutral-700 dark:text-neutral-300"><strong>Dx:</strong> {apt.consultation.diagnosis}</p>}
              {apt.consultation.notes && <p className="text-sm text-neutral-700 dark:text-neutral-300 mt-1"><strong>Notes:</strong> {apt.consultation.notes}</p>}
            </div>
          )}

          <div className="flex gap-2 flex-wrap">
            {apt.status === 'scheduled' && (
              <button onClick={() => handleStatusUpdate('confirmed')} disabled={updating} className="flex-1 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600 dark:text-emerald-400 text-sm font-medium py-2 rounded-xl hover:bg-emerald-100 transition-colors disabled:opacity-50 flex items-center justify-center gap-1.5">
                <CheckCircle className="w-4 h-4" /> Confirm
              </button>
            )}
            {['scheduled', 'confirmed'].includes(apt.status) && !apt.consultation && (
              <button onClick={() => setShowConsultation(true)} className="flex-1 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 text-sm font-medium py-2 rounded-xl hover:bg-blue-100 transition-colors flex items-center justify-center gap-1.5">
                <FileText className="w-4 h-4" /> Write Notes
              </button>
            )}
            {apt.type === 'video' && ['scheduled', 'confirmed'].includes(apt.status) && (
              <a href={apt.video_call?.join_url_doctor || '#'} className="flex-1 bg-violet-50 dark:bg-violet-900/20 text-violet-600 dark:text-violet-400 text-sm font-medium py-2 rounded-xl hover:bg-violet-100 transition-colors flex items-center justify-center gap-1.5">
                <Video className="w-4 h-4" /> Join Call
              </a>
            )}
            {['scheduled', 'confirmed'].includes(apt.status) && (
              <button onClick={() => handleStatusUpdate('cancelled')} disabled={updating} className="px-3 py-2 bg-red-50 dark:bg-red-900/20 text-red-500 dark:text-red-400 text-sm font-medium rounded-xl hover:bg-red-100 transition-colors disabled:opacity-50">
                <X className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>
      )}

      {showConsultation && (
        <ConsultationForm
          appointment={apt}
          onSave={() => { setShowConsultation(false); onUpdate(apt.id, 'completed'); }}
          onClose={() => setShowConsultation(false)}
        />
      )}
    </div>
  );
};

const DoctorAppointments = () => {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  const load = async () => {
    setLoading(true);
    try {
      const data = await apiService.get('/appointments');
      setAppointments(data || []);
    } catch {
      setAppointments([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleUpdate = (id, newStatus) => {
    setAppointments(prev => prev.map(a => a.id === id ? { ...a, status: newStatus } : a));
  };

  const tabs = [
    { key: 'all', label: 'All' },
    { key: 'today', label: 'Today' },
    { key: 'upcoming', label: 'Upcoming' },
    { key: 'completed', label: 'Completed' },
  ];

  const today = new Date().toDateString();
  const filtered = appointments.filter(a => {
    if (filter === 'today') return new Date(a.appointment_date).toDateString() === today;
    if (filter === 'upcoming') return ['scheduled', 'confirmed'].includes(a.status);
    if (filter === 'completed') return a.status === 'completed';
    return true;
  });

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-neutral-900 dark:text-white">Patient Queue</h1>
          <p className="text-neutral-500 dark:text-neutral-400 mt-1">Manage your appointments and consultations</p>
        </div>
        <button onClick={load} className="p-2 rounded-xl border border-neutral-200 dark:border-neutral-700 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors">
          <RefreshCw className={`w-4 h-4 text-neutral-500 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      <div className="flex gap-2 border-b border-neutral-200 dark:border-neutral-700">
        {tabs.map(tab => (
          <button key={tab.key} onClick={() => setFilter(tab.key)} className={`pb-3 px-4 text-sm font-medium border-b-2 transition-colors ${filter === tab.key ? 'text-primary-500 border-primary-500' : 'text-neutral-500 border-transparent hover:text-neutral-700 dark:hover:text-neutral-300'}`}>
            {tab.label}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="space-y-4">{[1, 2, 3].map(i => <div key={i} className="h-24 bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 animate-pulse" />)}</div>
      ) : filtered.length > 0 ? (
        <div className="space-y-4">{filtered.map(apt => <AppointmentDetail key={apt.id} apt={apt} onUpdate={handleUpdate} />)}</div>
      ) : (
        <div className="text-center py-16">
          <Calendar className="w-12 h-12 text-neutral-300 mx-auto mb-3" />
          <p className="text-neutral-500 font-medium">No appointments found</p>
        </div>
      )}
    </div>
  );
};

export default DoctorAppointments;
