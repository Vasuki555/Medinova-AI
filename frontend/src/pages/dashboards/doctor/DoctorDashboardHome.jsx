/**
 * Doctor Dashboard Home
 * Main overview for doctor users
 */

import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { apiService } from '@/services/api';
import {
  Users, Calendar, Clock, CheckCircle, TrendingUp,
  Star, ArrowRight, Stethoscope, Bell, AlertCircle,
  Video, UserCheck
} from 'lucide-react';

const StatCard = ({ icon: Icon, label, value, color, sub }) => (
  <div className="bg-white dark:bg-neutral-800 rounded-2xl p-5 border border-neutral-200 dark:border-neutral-700 shadow-sm">
    <div className="flex items-center justify-between mb-3">
      <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${color}`}>
        <Icon className="w-5 h-5 text-white" />
      </div>
    </div>
    <p className="text-2xl font-bold text-neutral-900 dark:text-white">{value}</p>
    <p className="text-sm text-neutral-500 dark:text-neutral-400 mt-1">{label}</p>
    {sub && <p className="text-xs text-emerald-500 mt-0.5">{sub}</p>}
  </div>
);

const AppointmentRow = ({ apt }) => {
  const statusColors = {
    scheduled: 'bg-blue-100 text-blue-700',
    confirmed: 'bg-emerald-100 text-emerald-700',
    in_progress: 'bg-amber-100 text-amber-700',
    completed: 'bg-gray-100 text-gray-600',
    cancelled: 'bg-red-100 text-red-600',
  };
  const date = new Date(apt.appointment_date);

  return (
    <div className="flex items-center gap-4 p-3 hover:bg-neutral-50 dark:hover:bg-neutral-700/40 rounded-xl transition-colors">
      <div className="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-900/30 flex flex-col items-center justify-center flex-shrink-0">
        <span className="text-xs font-bold text-emerald-600 leading-none">{date.toLocaleDateString('en', { month: 'short' })}</span>
        <span className="text-base font-black text-emerald-600 leading-none">{date.getDate()}</span>
      </div>
      <div className="flex-grow min-w-0">
        <p className="font-semibold text-sm text-neutral-900 dark:text-white truncate">{apt.patient_name || 'Patient'}</p>
        <p className="text-xs text-neutral-400">
          {date.toLocaleTimeString('en', { hour: '2-digit', minute: '2-digit' })}
          {' · '}{apt.reason || 'Consultation'}
        </p>
      </div>
      <div className="flex items-center gap-2 flex-shrink-0">
        <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${statusColors[apt.status] || 'bg-gray-100 text-gray-600'}`}>
          {apt.status}
        </span>
        {apt.type === 'video' && <Video className="w-3.5 h-3.5 text-neutral-400" />}
      </div>
    </div>
  );
};

const DoctorDashboardHome = () => {
  const { user } = useAuth();
  const [appointments, setAppointments] = useState([]);
  const [profile, setProfile] = useState(null);
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [apts, prof, notifs] = await Promise.allSettled([
          apiService.get('/appointments'),
          apiService.get('/doctors/profile'),
          apiService.get('/notifications'),
        ]);
        if (apts.status === 'fulfilled') setAppointments(apts.value || []);
        if (prof.status === 'fulfilled') setProfile(prof.value);
        if (notifs.status === 'fulfilled') setNotifications(notifs.value || []);
      } catch {
        // Silent fail
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  const today = new Date().toDateString();
  const todayApts = appointments.filter(a => new Date(a.appointment_date).toDateString() === today);
  const upcomingApts = appointments.filter(a => ['scheduled', 'confirmed'].includes(a.status));
  const completedApts = appointments.filter(a => a.status === 'completed');
  const unreadNotifs = notifications.filter(n => !n.is_read).length;

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Welcome Banner */}
      <div className="relative bg-gradient-to-r from-emerald-600 via-emerald-500 to-teal-500 rounded-2xl p-6 text-white overflow-hidden">
        <div className="absolute top-0 right-0 w-48 h-48 bg-white/10 rounded-full -translate-y-12 translate-x-12" />
        <div className="relative z-10">
          <p className="text-emerald-100 text-sm font-medium mb-1">Welcome back,</p>
          <h1 className="text-2xl font-bold mb-1">Dr. {user?.first_name} {user?.last_name} 👨‍⚕️</h1>
          <p className="text-emerald-100 text-sm">
            {profile?.specialization || 'General Practitioner'} · {profile?.total_consultations || 0} consultations completed
          </p>
          <div className="flex gap-3 mt-4">
            <Link to="/doctor/appointments" className="bg-white text-emerald-600 text-sm font-semibold px-4 py-2 rounded-xl hover:bg-emerald-50 transition-colors flex items-center gap-2">
              <Calendar className="w-4 h-4" /> Patient Queue
            </Link>
            <Link to="/doctor/schedule" className="bg-white/20 text-white text-sm font-semibold px-4 py-2 rounded-xl hover:bg-white/30 transition-colors flex items-center gap-2">
              <Clock className="w-4 h-4" /> My Schedule
            </Link>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard icon={Calendar} label="Today's Appointments" value={todayApts.length} color="bg-blue-500" sub={todayApts.length > 0 ? `${todayApts.filter(a => a.status === 'scheduled').length} pending` : ''} />
        <StatCard icon={Users} label="Upcoming" value={upcomingApts.length} color="bg-violet-500" />
        <StatCard icon={CheckCircle} label="Completed" value={completedApts.length} color="bg-emerald-500" sub="All time" />
        <StatCard icon={Bell} label="Unread Alerts" value={unreadNotifs} color="bg-amber-500" />
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Today's Queue */}
        <div className="lg:col-span-2 bg-white dark:bg-neutral-800 rounded-2xl p-6 border border-neutral-200 dark:border-neutral-700 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-neutral-900 dark:text-white">Today's Queue</h2>
            <Link to="/doctor/appointments" className="text-primary-500 text-sm font-medium flex items-center gap-1 hover:gap-2 transition-all">
              View All <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
          {loading ? (
            <div className="space-y-2">
              {[1, 2, 3].map(i => <div key={i} className="h-14 bg-neutral-100 dark:bg-neutral-700 rounded-xl animate-pulse" />)}
            </div>
          ) : todayApts.length > 0 ? (
            <div>
              {todayApts.map(apt => <AppointmentRow key={apt.id} apt={apt} />)}
            </div>
          ) : (
            <div className="text-center py-10">
              <Calendar className="w-12 h-12 text-neutral-300 mx-auto mb-3" />
              <p className="text-neutral-500 font-medium">No appointments today</p>
              <p className="text-neutral-400 text-sm mt-1">Your schedule is clear for today</p>
            </div>
          )}
        </div>

        {/* Profile Card */}
        <div className="space-y-4">
          <div className="bg-white dark:bg-neutral-800 rounded-2xl p-5 border border-neutral-200 dark:border-neutral-700 shadow-sm">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-emerald-400 to-emerald-600 flex items-center justify-center text-white font-bold text-lg">
                {(user?.first_name || 'D')[0]}
              </div>
              <div>
                <p className="font-bold text-neutral-900 dark:text-white text-sm">Dr. {user?.first_name} {user?.last_name}</p>
                <p className="text-xs text-emerald-500">{profile?.specialization || 'General Practitioner'}</p>
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-neutral-500">Rating</span>
                <span className="font-bold text-amber-500 flex items-center gap-1">
                  <Star className="w-3.5 h-3.5 fill-amber-400" />
                  {profile?.rating?.toFixed(1) || '—'}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-neutral-500">Experience</span>
                <span className="font-medium text-neutral-800 dark:text-white">{profile?.years_of_experience || 0} years</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-neutral-500">Consultation Fee</span>
                <span className="font-medium text-neutral-800 dark:text-white">${profile?.consultation_fee || 50}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-neutral-500">Status</span>
                <span className={`font-medium ${profile?.is_available ? 'text-emerald-500' : 'text-red-500'}`}>
                  {profile?.is_available ? '✓ Available' : '✗ Unavailable'}
                </span>
              </div>
            </div>
            <Link to="/doctor/schedule" className="mt-4 w-full block text-center bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600 dark:text-emerald-400 text-sm font-semibold py-2 rounded-xl hover:bg-emerald-100 dark:hover:bg-emerald-900/30 transition-colors">
              Edit Profile & Schedule
            </Link>
          </div>

          {/* Quick actions */}
          <div className="bg-white dark:bg-neutral-800 rounded-2xl p-5 border border-neutral-200 dark:border-neutral-700 shadow-sm">
            <h3 className="font-bold text-neutral-900 dark:text-white mb-3 text-sm">Quick Stats</h3>
            <div className="space-y-2">
              {[
                { label: 'Consultations', value: profile?.total_consultations || 0, icon: Stethoscope, color: 'text-blue-500' },
                { label: 'Total Reviews', value: profile?.review_count || 0, icon: Star, color: 'text-amber-500' },
                { label: 'Upcoming', value: upcomingApts.length, icon: Calendar, color: 'text-violet-500' },
              ].map(item => (
                <div key={item.label} className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <item.icon className={`w-4 h-4 ${item.color}`} />
                    <span className="text-sm text-neutral-600 dark:text-neutral-400">{item.label}</span>
                  </div>
                  <span className="font-bold text-neutral-900 dark:text-white">{item.value}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Upcoming Appointments */}
      {upcomingApts.length > 0 && (
        <div className="bg-white dark:bg-neutral-800 rounded-2xl p-6 border border-neutral-200 dark:border-neutral-700 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-neutral-900 dark:text-white">Upcoming Appointments</h2>
            <Link to="/doctor/appointments" className="text-primary-500 text-sm font-medium">View All →</Link>
          </div>
          <div className="space-y-1">
            {upcomingApts.slice(0, 5).map(apt => <AppointmentRow key={apt.id} apt={apt} />)}
          </div>
        </div>
      )}
    </div>
  );
};

export default DoctorDashboardHome;
