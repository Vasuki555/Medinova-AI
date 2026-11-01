/**
 * Patient Dashboard Home
 * Main overview page for patients with stats, upcoming appointments, and health summary
 */

import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { apiService } from '@/services/api';
import {
  Calendar, HeartPulse, Pill, Bell, Activity,
  ArrowRight, Clock, CheckCircle, AlertCircle,
  TrendingUp, User, Stethoscope, FileText
} from 'lucide-react';

const StatCard = ({ icon: Icon, label, value, color, trend, onClick }) => (
  <div 
    onClick={onClick}
    className={`bg-white dark:bg-neutral-800 rounded-2xl p-5 border border-neutral-200 dark:border-neutral-700 shadow-sm hover:shadow-md transition-all ${onClick ? 'cursor-pointer hover:scale-105 hover:border-primary-400' : ''}`}
  >
    <div className="flex items-center justify-between mb-3">
      <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${color}`}>
        <Icon className="w-5 h-5 text-white" />
      </div>
      {trend && (
        <span className="text-xs font-medium text-emerald-600 bg-emerald-50 px-2 py-1 rounded-lg">
          {trend}
        </span>
      )}
    </div>
    <p className="text-2xl font-bold text-neutral-900 dark:text-white">{value}</p>
    <p className="text-sm text-neutral-500 dark:text-neutral-400 mt-1">{label}</p>
  </div>
);

const AppointmentCard = ({ appointment }) => {
  const statusColors = {
    scheduled: 'bg-blue-100 text-blue-700',
    confirmed: 'bg-emerald-100 text-emerald-700',
    completed: 'bg-gray-100 text-gray-600',
    cancelled: 'bg-red-100 text-red-600',
  };

  const date = new Date(appointment.appointment_date);

  return (
    <div className="flex items-center gap-4 p-4 bg-neutral-50 dark:bg-neutral-700/40 rounded-xl border border-neutral-100 dark:border-neutral-700">
      <div className="w-12 h-12 bg-primary-100 rounded-xl flex flex-col items-center justify-center flex-shrink-0">
        <span className="text-xs font-bold text-primary-700">{date.toLocaleDateString('en', { month: 'short' })}</span>
        <span className="text-lg font-black text-primary-600">{date.getDate()}</span>
      </div>
      <div className="flex-grow min-w-0">
        <p className="font-semibold text-neutral-900 dark:text-white text-sm truncate">
          {appointment.doctor_name || 'Doctor'}
        </p>
        <p className="text-xs text-neutral-500 dark:text-neutral-400">
          {appointment.doctor_specialization || 'General Practitioner'}
        </p>
        <p className="text-xs text-neutral-400 mt-0.5">
          {date.toLocaleTimeString('en', { hour: '2-digit', minute: '2-digit' })}
          {' · '}{appointment.type === 'video' ? 'Video Call' : 'In-Person'}
        </p>
      </div>
      <span className={`text-xs font-medium px-2 py-1 rounded-lg flex-shrink-0 ${statusColors[appointment.status] || 'bg-gray-100 text-gray-600'}`}>
        {appointment.status}
      </span>
    </div>
  );
};

const PatientDashboardHome = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [appointments, setAppointments] = useState([]);
  const [medications, setMedications] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [healthRecords, setHealthRecords] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [apts, meds, notifs, records] = await Promise.allSettled([
          apiService.get('/appointments'),
          apiService.get('/medications'),
          apiService.get('/notifications'),
          apiService.get('/health-records'),
        ]);
        if (apts.status === 'fulfilled') setAppointments(apts.value || []);
        if (meds.status === 'fulfilled') setMedications(meds.value || []);
        if (notifs.status === 'fulfilled') setNotifications(notifs.value || []);
        if (records.status === 'fulfilled') setHealthRecords(records.value || []);
      } catch (err) {
        // Silent fail - show empty states
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  const upcomingAppointments = appointments
    .filter(a => ['scheduled', 'confirmed'].includes(a.status))
    .slice(0, 3);

  const activeMeds = medications.filter(m => m.is_active !== false);
  const unreadNotifs = notifications.filter(n => !n.is_read).length;
  const latestRecord = healthRecords[0];

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Welcome Banner */}
      <div className="relative bg-gradient-to-r from-primary-600 via-primary-500 to-cyan-500 rounded-2xl p-6 text-white overflow-hidden">
        <div className="absolute top-0 right-0 w-48 h-48 bg-white/10 rounded-full -translate-y-12 translate-x-12" />
        <div className="absolute bottom-0 left-1/2 w-32 h-32 bg-white/5 rounded-full translate-y-8" />
        <div className="relative z-10">
          <p className="text-primary-100 text-sm font-medium mb-1">Good morning,</p>
          <h1 className="text-2xl font-bold mb-1">{user?.first_name} {user?.last_name} 👋</h1>
          <p className="text-primary-100 text-sm">Here's your health summary for today.</p>
          <div className="flex gap-3 mt-4">
            <Link to="/patient/booking" className="bg-white text-primary-600 text-sm font-semibold px-4 py-2 rounded-xl hover:bg-primary-50 transition-colors flex items-center gap-2">
              <Calendar className="w-4 h-4" /> Book Appointment
            </Link>
            <Link to="/patient/phr" className="bg-white/20 text-white text-sm font-semibold px-4 py-2 rounded-xl hover:bg-white/30 transition-colors flex items-center gap-2">
              <HeartPulse className="w-4 h-4" /> Health Record
            </Link>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          icon={Calendar}
          label="Upcoming Appointments"
          value={upcomingAppointments.length}
          color="bg-blue-500"
          trend={upcomingAppointments.length > 0 ? 'Active' : null}
          onClick={() => navigate('/patient/appointments')}
        />
        <StatCard
          icon={Pill}
          label="Active Medications"
          value={activeMeds.length}
          color="bg-violet-500"
          onClick={() => navigate('/patient/medications')}
        />
        <StatCard
          icon={Bell}
          label="Unread Notifications"
          value={unreadNotifs}
          color="bg-amber-500"
          trend={unreadNotifs > 0 ? 'New' : null}
          onClick={() => navigate('/patient/notifications')}
        />
        <StatCard
          icon={FileText}
          label="Health Records"
          value={healthRecords.length}
          color="bg-emerald-500"
          trend="Tracked"
          onClick={() => navigate('/patient/phr')}
        />
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Upcoming Appointments */}
        <div className="lg:col-span-2 bg-white dark:bg-neutral-800 rounded-2xl p-6 border border-neutral-200 dark:border-neutral-700 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-neutral-900 dark:text-white">Upcoming Appointments</h2>
            <Link to="/patient/appointments" className="text-primary-500 text-sm font-medium flex items-center gap-1 hover:gap-2 transition-all">
              View All <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
          {loading ? (
            <div className="space-y-3">
              {[1, 2, 3].map(i => (
                <div key={i} className="h-16 bg-neutral-100 dark:bg-neutral-700 rounded-xl animate-pulse" />
              ))}
            </div>
          ) : upcomingAppointments.length > 0 ? (
            <div className="space-y-3">
              {upcomingAppointments.map(apt => (
                <AppointmentCard key={apt.id} appointment={apt} />
              ))}
            </div>
          ) : (
            <div className="text-center py-10">
              <Calendar className="w-12 h-12 text-neutral-300 mx-auto mb-3" />
              <p className="text-neutral-500 font-medium">No upcoming appointments</p>
              <p className="text-neutral-400 text-sm mt-1">Book a consultation with a doctor</p>
              <Link to="/patient/booking" className="mt-4 inline-flex items-center gap-2 bg-primary-500 text-white px-4 py-2 rounded-xl text-sm font-medium hover:bg-primary-600 transition-colors">
                <Calendar className="w-4 h-4" /> Book Now
              </Link>
            </div>
          )}
        </div>

        {/* Right Panel */}
        <div className="space-y-4">
          {/* Latest Vitals */}
          <div className="bg-white dark:bg-neutral-800 rounded-2xl p-5 border border-neutral-200 dark:border-neutral-700 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-neutral-900 dark:text-white">Latest Vitals</h3>
              <Link to="/patient/phr" className="text-primary-500 text-xs font-medium">View All</Link>
            </div>
            {latestRecord?.vitals ? (
              <div className="space-y-3">
                {latestRecord.vitals.heart_rate && (
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Activity className="w-4 h-4 text-rose-500" />
                      <span className="text-sm text-neutral-600 dark:text-neutral-400">Heart Rate</span>
                    </div>
                    <span className="font-bold text-neutral-900 dark:text-white text-sm">{latestRecord.vitals.heart_rate} <span className="font-normal text-neutral-400">bpm</span></span>
                  </div>
                )}
                {(latestRecord.vitals.blood_pressure_systolic) && (
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <TrendingUp className="w-4 h-4 text-blue-500" />
                      <span className="text-sm text-neutral-600 dark:text-neutral-400">Blood Pressure</span>
                    </div>
                    <span className="font-bold text-neutral-900 dark:text-white text-sm">
                      {latestRecord.vitals.blood_pressure_systolic}/{latestRecord.vitals.blood_pressure_diastolic} <span className="font-normal text-neutral-400">mmHg</span>
                    </span>
                  </div>
                )}
                {latestRecord.vitals.temperature && (
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <HeartPulse className="w-4 h-4 text-orange-500" />
                      <span className="text-sm text-neutral-600 dark:text-neutral-400">Temperature</span>
                    </div>
                    <span className="font-bold text-neutral-900 dark:text-white text-sm">{latestRecord.vitals.temperature} <span className="font-normal text-neutral-400">°F</span></span>
                  </div>
                )}
              </div>
            ) : (
              <div className="text-center py-4">
                <HeartPulse className="w-8 h-8 text-neutral-300 mx-auto mb-2" />
                <p className="text-sm text-neutral-400">No vitals recorded yet</p>
                <Link to="/patient/phr" className="text-primary-500 text-xs mt-1 block">Add record →</Link>
              </div>
            )}
          </div>

          {/* Medications Today */}
          <div className="bg-white dark:bg-neutral-800 rounded-2xl p-5 border border-neutral-200 dark:border-neutral-700 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-neutral-900 dark:text-white">Today's Medications</h3>
              <Link to="/patient/medications" className="text-primary-500 text-xs font-medium">Manage</Link>
            </div>
            {activeMeds.length > 0 ? (
              <div className="space-y-2">
                {activeMeds.slice(0, 4).map(med => (
                  <div key={med.id} className="flex items-center gap-3 p-2 rounded-lg bg-neutral-50 dark:bg-neutral-700/40">
                    <div className="w-7 h-7 rounded-lg bg-violet-100 flex items-center justify-center flex-shrink-0">
                      <Pill className="w-3.5 h-3.5 text-violet-600" />
                    </div>
                    <div className="flex-grow min-w-0">
                      <p className="text-sm font-medium text-neutral-900 dark:text-white truncate">{med.name}</p>
                      <p className="text-xs text-neutral-400">{med.dosage} · {(med.schedule_times || []).join(', ')}</p>
                    </div>
                  </div>
                ))}
                {activeMeds.length > 4 && (
                  <p className="text-xs text-neutral-400 text-center mt-2">+{activeMeds.length - 4} more</p>
                )}
              </div>
            ) : (
              <div className="text-center py-4">
                <Pill className="w-8 h-8 text-neutral-300 mx-auto mb-2" />
                <p className="text-sm text-neutral-400">No medications tracked</p>
                <Link to="/patient/medications" className="text-primary-500 text-xs mt-1 block">Add medication →</Link>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Quick Links */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {[
          { icon: Stethoscope, label: 'Find Doctor', path: '/patient/booking', color: 'from-blue-500 to-cyan-500' },
          { icon: HeartPulse, label: 'PHR', path: '/patient/phr', color: 'from-rose-500 to-pink-500' },
          { icon: Pill, label: 'Medications', path: '/patient/medications', color: 'from-violet-500 to-purple-500' },
          { icon: Activity, label: 'Hospitals', path: '/patient/hospitals', color: 'from-emerald-500 to-teal-500' },
        ].map(item => (
          <Link
            key={item.path}
            to={item.path}
            className={`bg-gradient-to-br ${item.color} rounded-2xl p-5 text-white flex flex-col items-center justify-center gap-2 hover:scale-[1.02] transition-transform shadow-sm`}
          >
            <item.icon className="w-7 h-7" />
            <span className="text-sm font-semibold">{item.label}</span>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default PatientDashboardHome;
