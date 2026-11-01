/**
 * Notifications Page
 * View and manage system notifications
 */

import { useState, useEffect } from 'react';
import { apiService } from '@/services/api';
import {
  Bell, Calendar, Pill, HeartPulse, Shield,
  CheckCheck, Trash2, Info, AlertTriangle, CheckCircle,
  XCircle, BellOff, Loader2
} from 'lucide-react';

const typeIcons = {
  appointment: Calendar,
  medication: Pill,
  health: HeartPulse,
  security: Shield,
  system: Info,
};

const categoryColors = {
  info: 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400',
  success: 'bg-emerald-50 text-emerald-600 dark:bg-emerald-900/20 dark:text-emerald-400',
  warning: 'bg-amber-50 text-amber-600 dark:bg-amber-900/20 dark:text-amber-400',
  error: 'bg-red-50 text-red-600 dark:bg-red-900/20 dark:text-red-400',
};

const NotificationItem = ({ notif, onRead }) => {
  const [marking, setMarking] = useState(false);
  const Icon = typeIcons[notif.type] || Bell;

  const handleRead = async () => {
    if (notif.is_read) return;
    setMarking(true);
    try {
      await apiService.patch(`/notifications/${notif.id}/read`);
      onRead(notif.id);
    } catch {
      // Silent fail
    } finally {
      setMarking(false);
    }
  };

  const timeAgo = (dateStr) => {
    const diff = Date.now() - new Date(dateStr).getTime();
    const mins = Math.floor(diff / 60000);
    if (mins < 1) return 'Just now';
    if (mins < 60) return `${mins}m ago`;
    const hrs = Math.floor(mins / 60);
    if (hrs < 24) return `${hrs}h ago`;
    return new Date(dateStr).toLocaleDateString('en', { month: 'short', day: 'numeric' });
  };

  return (
    <div
      className={`flex items-start gap-4 p-4 rounded-2xl border transition-all cursor-pointer ${
        notif.is_read
          ? 'bg-white dark:bg-neutral-800 border-neutral-200 dark:border-neutral-700 opacity-75'
          : 'bg-primary-50 dark:bg-primary-900/10 border-primary-200 dark:border-primary-800'
      }`}
      onClick={handleRead}
    >
      <div className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 ${categoryColors[notif.category] || categoryColors.info}`}>
        <Icon className="w-5 h-5" />
      </div>
      <div className="flex-grow min-w-0">
        <div className="flex items-center gap-2">
          <h3 className={`font-semibold text-sm ${notif.is_read ? 'text-neutral-600 dark:text-neutral-400' : 'text-neutral-900 dark:text-white'}`}>
            {notif.title}
          </h3>
          {!notif.is_read && (
            <span className="w-2 h-2 rounded-full bg-primary-500 flex-shrink-0" />
          )}
        </div>
        <p className="text-sm text-neutral-500 dark:text-neutral-400 mt-0.5 leading-relaxed">
          {notif.message}
        </p>
        <div className="flex items-center gap-3 mt-2">
          <span className="text-xs text-neutral-400">{timeAgo(notif.created_at)}</span>
          {notif.action_url && notif.action_text && (
            <a
              href={notif.action_url}
              onClick={e => e.stopPropagation()}
              className="text-xs text-primary-500 font-medium hover:underline"
            >
              {notif.action_text} →
            </a>
          )}
        </div>
      </div>
      {marking && <Loader2 className="w-4 h-4 text-neutral-400 animate-spin flex-shrink-0" />}
    </div>
  );
};

const Notifications = () => {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [markingAll, setMarkingAll] = useState(false);
  const [filter, setFilter] = useState('all');

  const loadNotifications = async () => {
    setLoading(true);
    try {
      const data = await apiService.get('/notifications');
      setNotifications(data || []);
    } catch {
      setNotifications([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadNotifications(); }, []);

  const handleRead = (id) => {
    setNotifications(prev => prev.map(n => n.id === id ? { ...n, is_read: true } : n));
  };

  const handleMarkAll = async () => {
    setMarkingAll(true);
    try {
      await apiService.patch('/notifications/read-all');
      setNotifications(prev => prev.map(n => ({ ...n, is_read: true })));
    } catch {
      alert('Failed to mark all as read');
    } finally {
      setMarkingAll(false);
    }
  };

  const unreadCount = notifications.filter(n => !n.is_read).length;
  const filtered = filter === 'all' ? notifications : filter === 'unread' ? notifications.filter(n => !n.is_read) : notifications.filter(n => n.is_read);

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-neutral-900 dark:text-white">Notifications</h1>
          <p className="text-neutral-500 dark:text-neutral-400 mt-1">
            {unreadCount > 0 ? `${unreadCount} unread notification${unreadCount > 1 ? 's' : ''}` : 'All caught up!'}
          </p>
        </div>
        {unreadCount > 0 && (
          <button
            onClick={handleMarkAll}
            disabled={markingAll}
            className="flex items-center gap-2 bg-neutral-100 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 text-sm font-medium px-4 py-2 rounded-xl hover:bg-neutral-200 dark:hover:bg-neutral-600 transition-colors disabled:opacity-50"
          >
            <CheckCheck className="w-4 h-4" />
            {markingAll ? 'Marking...' : 'Mark All Read'}
          </button>
        )}
      </div>

      {/* Filter Tabs */}
      <div className="flex gap-2">
        {[
          { key: 'all', label: 'All', count: notifications.length },
          { key: 'unread', label: 'Unread', count: unreadCount },
          { key: 'read', label: 'Read', count: notifications.length - unreadCount },
        ].map(tab => (
          <button
            key={tab.key}
            onClick={() => setFilter(tab.key)}
            className={`flex items-center gap-1.5 px-4 py-2 rounded-xl text-sm font-medium transition-colors ${
              filter === tab.key
                ? 'bg-primary-500 text-white'
                : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'
            }`}
          >
            {tab.label}
            {tab.count > 0 && (
              <span className={`text-xs px-1.5 py-0.5 rounded-full ${
                filter === tab.key ? 'bg-white/20 text-white' : 'bg-neutral-200 dark:bg-neutral-600 text-neutral-600 dark:text-neutral-300'
              }`}>
                {tab.count}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Content */}
      {loading ? (
        <div className="space-y-3">
          {[1, 2, 3, 4].map(i => (
            <div key={i} className="h-20 bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 animate-pulse" />
          ))}
        </div>
      ) : filtered.length > 0 ? (
        <div className="space-y-3">
          {filtered.map(n => (
            <NotificationItem key={n.id || n._id} notif={n} onRead={handleRead} />
          ))}
        </div>
      ) : (
        <div className="text-center py-16">
          <BellOff className="w-12 h-12 text-neutral-300 mx-auto mb-3" />
          <p className="text-neutral-500 font-medium">
            {filter === 'unread' ? 'No unread notifications' : 'No notifications'}
          </p>
          <p className="text-neutral-400 text-sm mt-1">You're all caught up!</p>
        </div>
      )}
    </div>
  );
};

export default Notifications;
