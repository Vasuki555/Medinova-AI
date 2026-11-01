/**
 * My Appointments Page
 * View all patient appointments with status tracking
 */

import { useState, useEffect } from 'react';
import { apiService } from '@/services/api';
import { Link } from 'react-router-dom';
import {
  Calendar, Clock, Video, User, CheckCircle,
  XCircle, AlertCircle, ChevronDown, ChevronUp,
  MapPin, Phone, RefreshCw
} from 'lucide-react';

const statusConfig = {
  scheduled: { color: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400', icon: Clock, label: 'Scheduled' },
  confirmed: { color: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400', icon: CheckCircle, label: 'Confirmed' },
  in_progress: { color: 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400', icon: AlertCircle, label: 'In Progress' },
  completed: { color: 'bg-gray-100 text-gray-600 dark:bg-neutral-700 dark:text-neutral-400', icon: CheckCircle, label: 'Completed' },
  cancelled: { color: 'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400', icon: XCircle, label: 'Cancelled' },
  no_show: { color: 'bg-orange-100 text-orange-600 dark:bg-orange-900/30 dark:text-orange-400', icon: AlertCircle, label: 'No Show' },
};

const AppointmentDetail = ({ apt, onCancel }) => {
  const [expanded, setExpanded] = useState(false);
  const [cancelling, setCancelling] = useState(false);
  const config = statusConfig[apt.status] || statusConfig.scheduled;
  const Icon = config.icon;
  const date = new Date(apt.appointment_date);

  const handleCancel = async () => {
    if (!window.confirm('Are you sure you want to cancel this appointment?')) return;
    setCancelling(true);
    try {
      await apiService.patch(`/appointments/${apt.id}/status`, {
        status: 'cancelled',
        cancellation_reason: 'Cancelled by patient',
      });
      onCancel(apt.id);
    } catch {
      alert('Cancellation failed. Please try again.');
    } finally {
      setCancelling(false);
    }
  };

  return (
    <div className="bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 shadow-sm overflow-hidden">
      <div
        className="flex items-center gap-4 p-5 cursor-pointer"
        onClick={() => setExpanded(e => !e)}
      >
        {/* Date Block */}
        <div className="w-14 h-14 rounded-2xl bg-primary-50 dark:bg-primary-900/30 flex flex-col items-center justify-center flex-shrink-0">
          <span className="text-xs font-bold text-primary-500 uppercase">
            {date.toLocaleDateString('en', { month: 'short' })}
          </span>
          <span className="text-xl font-black text-primary-600">{date.getDate()}</span>
        </div>

        {/* Info */}
        <div className="flex-grow min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <h3 className="font-bold text-neutral-900 dark:text-white truncate">
              {apt.doctor_name || 'Doctor'}
            </h3>
            <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${config.color}`}>
              <Icon className="w-3 h-3 inline mr-1" />
              {config.label}
            </span>
          </div>
          <p className="text-sm text-neutral-500 dark:text-neutral-400">
            {apt.doctor_specialization || 'General Practitioner'}
          </p>
          <div className="flex items-center gap-4 mt-1 flex-wrap">
            <span className="text-xs text-neutral-400 flex items-center gap-1">
              <Clock className="w-3 h-3" />
              {date.toLocaleTimeString('en', { hour: '2-digit', minute: '2-digit' })}
              {' · '}{apt.duration_minutes}min
            </span>
            <span className="text-xs text-neutral-400 flex items-center gap-1">
              <Video className="w-3 h-3" />
              {apt.type === 'video' ? 'Video Call' : apt.type === 'in_person' ? 'In-Person' : 'Chat'}
            </span>
          </div>
        </div>

        {/* Expand */}
        <div className="flex-shrink-0">
          {expanded ? <ChevronUp className="w-5 h-5 text-neutral-400" /> : <ChevronDown className="w-5 h-5 text-neutral-400" />}
        </div>
      </div>

      {expanded && (
        <div className="border-t border-neutral-100 dark:border-neutral-700 p-5 space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-xs text-neutral-400 uppercase tracking-wide mb-1">Reason</p>
              <p className="text-sm font-medium text-neutral-800 dark:text-white">{apt.reason || 'Not specified'}</p>
            </div>
            <div>
              <p className="text-xs text-neutral-400 uppercase tracking-wide mb-1">Appointment #</p>
              <p className="text-sm font-medium text-neutral-800 dark:text-white font-mono">{apt.appointment_number}</p>
            </div>
            {apt.symptoms?.length > 0 && (
              <div className="col-span-2">
                <p className="text-xs text-neutral-400 uppercase tracking-wide mb-2">Reported Symptoms</p>
                <div className="flex flex-wrap gap-2">
                  {apt.symptoms.map(s => (
                    <span key={s} className="text-xs bg-neutral-100 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-300 px-2 py-1 rounded-lg">
                      {s}
                    </span>
                  ))}
                </div>
              </div>
            )}
            {apt.payment && (
              <div>
                <p className="text-xs text-neutral-400 uppercase tracking-wide mb-1">Fee</p>
                <p className="text-sm font-medium text-neutral-800 dark:text-white">
                  ${apt.payment.amount} · <span className={apt.payment.status === 'paid' ? 'text-emerald-600' : 'text-amber-600'}>{apt.payment.status}</span>
                </p>
              </div>
            )}
          </div>

          {apt.consultation && (
            <div className="bg-neutral-50 dark:bg-neutral-700/40 rounded-xl p-4">
              <p className="text-xs font-bold text-neutral-500 uppercase tracking-wide mb-2">Consultation Notes</p>
              {apt.consultation.diagnosis && (
                <p className="text-sm text-neutral-700 dark:text-neutral-300 mb-2">
                  <strong>Diagnosis:</strong> {apt.consultation.diagnosis}
                </p>
              )}
              {apt.consultation.notes && (
                <p className="text-sm text-neutral-700 dark:text-neutral-300">
                  <strong>Notes:</strong> {apt.consultation.notes}
                </p>
              )}
              {apt.consultation.follow_up_required && (
                <p className="text-sm text-blue-600 dark:text-blue-400 mt-2">
                  ℹ️ Follow-up required in {apt.consultation.follow_up_days} days
                </p>
              )}
            </div>
          )}

          {['scheduled', 'confirmed'].includes(apt.status) && (
            <div className="flex gap-3">
              {apt.type === 'video' && apt.video_call?.join_url_patient && (
                <a
                  href={apt.video_call.join_url_patient}
                  className="flex-1 bg-primary-500 text-white text-sm font-semibold py-2.5 rounded-xl hover:bg-primary-600 transition-colors text-center flex items-center justify-center gap-2"
                >
                  <Video className="w-4 h-4" /> Join Call
                </a>
              )}
              <button
                onClick={handleCancel}
                disabled={cancelling}
                className="flex-1 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 text-sm font-semibold py-2.5 rounded-xl hover:bg-red-100 dark:hover:bg-red-900/30 transition-colors disabled:opacity-50"
              >
                {cancelling ? 'Cancelling...' : 'Cancel Appointment'}
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

const MyAppointments = () => {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  const loadAppointments = async () => {
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

  useEffect(() => { loadAppointments(); }, []);

  const handleCancel = (id) => {
    setAppointments(prev => prev.map(a => a.id === id ? { ...a, status: 'cancelled' } : a));
  };

  const filtered = appointments.filter(a => {
    if (filter === 'all') return true;
    if (filter === 'upcoming') return ['scheduled', 'confirmed'].includes(a.status);
    if (filter === 'completed') return a.status === 'completed';
    if (filter === 'cancelled') return a.status === 'cancelled';
    return true;
  });

  const tabs = [
    { key: 'all', label: 'All', count: appointments.length },
    { key: 'upcoming', label: 'Upcoming', count: appointments.filter(a => ['scheduled', 'confirmed'].includes(a.status)).length },
    { key: 'completed', label: 'Completed', count: appointments.filter(a => a.status === 'completed').length },
    { key: 'cancelled', label: 'Cancelled', count: appointments.filter(a => a.status === 'cancelled').length },
  ];

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-neutral-900 dark:text-white">My Appointments</h1>
          <p className="text-neutral-500 dark:text-neutral-400 mt-1">Track and manage your consultations</p>
        </div>
        <div className="flex gap-2">
          <button onClick={loadAppointments} className="p-2 rounded-xl border border-neutral-200 dark:border-neutral-700 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors">
            <RefreshCw className={`w-4 h-4 text-neutral-500 ${loading ? 'animate-spin' : ''}`} />
          </button>
          <Link to="/patient/booking" className="bg-primary-500 text-white text-sm font-semibold px-4 py-2 rounded-xl hover:bg-primary-600 transition-colors flex items-center gap-2">
            <Calendar className="w-4 h-4" /> Book New
          </Link>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-neutral-200 dark:border-neutral-700">
        {tabs.map(tab => (
          <button
            key={tab.key}
            onClick={() => setFilter(tab.key)}
            className={`pb-3 px-4 text-sm font-medium border-b-2 transition-colors ${
              filter === tab.key
                ? 'text-primary-500 border-primary-500'
                : 'text-neutral-500 border-transparent hover:text-neutral-700 dark:hover:text-neutral-300'
            }`}
          >
            {tab.label}
            {tab.count > 0 && (
              <span className={`ml-1.5 text-xs px-1.5 py-0.5 rounded-full ${
                filter === tab.key ? 'bg-primary-100 text-primary-600' : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-500'
              }`}>
                {tab.count}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Content */}
      {loading ? (
        <div className="space-y-4">
          {[1, 2, 3].map(i => (
            <div key={i} className="h-24 bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 animate-pulse" />
          ))}
        </div>
      ) : filtered.length > 0 ? (
        <div className="space-y-4">
          {filtered.map(apt => (
            <AppointmentDetail key={apt.id} apt={apt} onCancel={handleCancel} />
          ))}
        </div>
      ) : (
        <div className="text-center py-16">
          <Calendar className="w-12 h-12 text-neutral-300 mx-auto mb-3" />
          <p className="text-neutral-500 font-medium">No appointments found</p>
          <p className="text-neutral-400 text-sm mt-1">
            {filter === 'all' ? 'Book a consultation to get started' : `No ${filter} appointments`}
          </p>
          {filter === 'all' && (
            <Link to="/patient/booking" className="mt-4 inline-flex items-center gap-2 bg-primary-500 text-white px-4 py-2 rounded-xl text-sm font-medium hover:bg-primary-600 transition-colors">
              <Calendar className="w-4 h-4" /> Book Now
            </Link>
          )}
        </div>
      )}
    </div>
  );
};

export default MyAppointments;
