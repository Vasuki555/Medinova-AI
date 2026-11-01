/**
 * Dashboard Layout Component
 * Private layout featuring a collapsible premium sidebar, unread badge, and dark mode toggles.
 */

import { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation, Outlet } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { useTheme } from '@/context/ThemeContext';
import { apiService } from '@/services/api';
import {
  LayoutDashboard,
  CalendarDays,
  CalendarRange,
  HeartPulse,
  Pill,
  MapPin,
  Bell,
  LogOut,
  Menu,
  X,
  Sun,
  Moon,
  Users,
  ShieldCheck,
  ClipboardList,
  Bot,
  QrCode,
  UserCircle2,
  Upload
} from 'lucide-react';

const DashboardLayout = () => {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const location = useLocation();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [unreadCount, setUnreadCount] = useState(0);

  // Poll unread notifications count
  useEffect(() => {
    const fetchUnread = async () => {
      try {
        const response = await apiService.get('/notifications/unread-count');
        setUnreadCount(response.unread_count || 0);
      } catch (err) {
        // Fallback or ignore on connection issues
      }
    };
    fetchUnread();
    const interval = setInterval(fetchUnread, 15000);
    return () => clearInterval(interval);
  }, []);

  const getNavigationLinks = () => {
    if (!user) return [];
    
    switch (user.role) {
      case 'patient':
        return [
          { name: 'Dashboard', path: '/patient/dashboard', icon: LayoutDashboard },
          { name: 'Book Appointment', path: '/patient/booking', icon: CalendarDays },
          { name: 'My Appointments', path: '/patient/appointments', icon: CalendarRange },
          { name: 'Health Record', path: '/patient/phr', icon: HeartPulse },
          { name: 'Medications', path: '/patient/medications', icon: Pill },
          { name: 'AI Assistant', path: '/patient/ai-assistant', icon: Bot },
          { name: 'Smart Upload', path: '/patient/smart-upload', icon: Upload },
          { name: 'QR Health ID', path: '/patient/qr-id', icon: QrCode },
          { name: 'Nearby Hospitals', path: '/patient/hospitals', icon: MapPin },
          { name: 'My Profile', path: '/patient/profile', icon: UserCircle2 },
          { name: 'Notifications', path: '/patient/notifications', icon: Bell, badge: unreadCount }
        ];
      case 'doctor':
        return [
          { name: 'Doctor Portal', path: '/doctor/dashboard', icon: LayoutDashboard },
          { name: 'Patient Queue', path: '/doctor/appointments', icon: ClipboardList },
          { name: 'My Schedule', path: '/doctor/schedule', icon: CalendarRange },
          { name: 'My QR Code', path: '/doctor/qr-code', icon: QrCode },
          { name: 'My Profile', path: '/doctor/profile', icon: UserCircle2 },
          { name: 'Notifications', path: '/doctor/notifications', icon: Bell, badge: unreadCount }
        ];
      case 'admin':
        return [
          { name: 'Admin Console', path: '/admin/dashboard', icon: LayoutDashboard },
          { name: 'Platform Users', path: '/admin/users', icon: Users },
          { name: 'Verify Credentials', path: '/admin/verify', icon: ShieldCheck },
          { name: 'Notifications', path: '/admin/notifications', icon: Bell, badge: unreadCount }
        ];
      default:
        return [];
    }
  };

  const links = getNavigationLinks();

  return (
    <div className="min-h-screen flex bg-neutral-50 dark:bg-neutral-900 transition-colors duration-300">
      {/* Sidebar for Desktop */}
      <aside className="hidden lg:flex flex-col w-64 bg-white/70 dark:bg-neutral-900/60 border-r border-neutral-200 dark:border-neutral-800 backdrop-blur-xl sticky top-0 h-screen py-6 px-4 z-40">
        {/* Brand */}
        <div className="flex items-center space-x-3 px-2 mb-8">
          <div className="w-9 h-9 bg-primary-500 rounded-xl flex items-center justify-center shadow-lg shadow-primary-500/20">
            <span className="text-white font-bold text-lg">M</span>
          </div>
          <span className="text-lg font-display font-bold text-neutral-900 dark:text-white">
            MediNova <span className="text-primary-500">AI</span>
          </span>
        </div>

        {/* Links */}
        <nav className="flex-grow space-y-1.5 overflow-y-auto pr-1">
          {links.map((link) => {
            const Icon = link.icon;
            const isActive = location.pathname === link.path;
            return (
              <Link
                key={link.name}
                to={link.path}
                className={`flex items-center justify-between px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200 ${
                  isActive
                    ? 'bg-primary-500 text-white shadow-lg shadow-primary-500/10'
                    : 'text-neutral-600 dark:text-neutral-400 hover:bg-neutral-100 dark:hover:bg-neutral-800 hover:text-neutral-900 dark:hover:text-white'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon className="w-5 h-5" />
                  <span>{link.name}</span>
                </div>
                {link.badge > 0 && (
                  <span className={`px-2 py-0.5 rounded-full text-xs font-bold ${
                    isActive ? 'bg-white text-primary-600' : 'bg-primary-500 text-white'
                  }`}>
                    {link.badge}
                  </span>
                )}
              </Link>
            );
          })}
        </nav>

        {/* Footer actions */}
        <div className="border-t border-neutral-200 dark:border-neutral-800 pt-4 mt-4 space-y-2">
          {/* Theme switcher */}
          <button
            onClick={toggleTheme}
            className="flex items-center gap-3 w-full px-3 py-2.5 rounded-xl text-sm font-medium text-neutral-600 dark:text-neutral-400 hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-colors"
          >
            {theme === 'dark' ? (
              <>
                <Sun className="w-5 h-5 text-amber-400" />
                <span>Light Mode</span>
              </>
            ) : (
              <>
                <Moon className="w-5 h-5 text-indigo-500" />
                <span>Dark Mode</span>
              </>
            )}
          </button>

          {/* Logout */}
          <button
            onClick={logout}
            className="flex items-center gap-3 w-full px-3 py-2.5 rounded-xl text-sm font-medium text-rose-500 hover:bg-rose-50 dark:hover:bg-rose-950/20 transition-colors"
          >
            <LogOut className="w-5 h-5" />
            <span>Logout</span>
          </button>
        </div>
      </aside>

      {/* Mobile Header Bar */}
      <div className="flex-grow flex flex-col min-w-0">
        <header className="lg:hidden flex items-center justify-between h-16 px-4 bg-white/80 dark:bg-neutral-900/80 border-b border-neutral-200 dark:border-neutral-800 backdrop-blur-xl sticky top-0 z-50">
          <button
            onClick={() => setIsSidebarOpen(true)}
            className="p-1 rounded-lg text-neutral-600 dark:text-neutral-400 hover:bg-neutral-100 dark:hover:bg-neutral-800"
          >
            <Menu className="w-6 h-6" />
          </button>
          
          <span className="text-md font-display font-bold text-neutral-900 dark:text-white">
            MediNova <span className="text-primary-500">AI</span>
          </span>

          <button
            onClick={toggleTheme}
            className="p-1.5 rounded-xl text-neutral-600 dark:text-neutral-400 hover:bg-neutral-100 dark:hover:bg-neutral-800"
          >
            {theme === 'dark' ? <Sun className="w-5 h-5 text-amber-400" /> : <Moon className="w-5 h-5 text-indigo-500" />}
          </button>
        </header>

        {/* Mobile Navigation Drawer Overlay */}
        {isSidebarOpen && (
          <div className="fixed inset-0 bg-neutral-950/60 backdrop-blur-sm z-[100] lg:hidden">
            <aside className="w-64 max-w-[80vw] h-full bg-white dark:bg-neutral-900 flex flex-col p-6 shadow-2xl animate-fade-in">
              <div className="flex items-center justify-between mb-8">
                <span className="text-md font-display font-bold text-neutral-900 dark:text-white">
                  MediNova <span className="text-primary-500">AI</span>
                </span>
                <button
                  onClick={() => setIsSidebarOpen(false)}
                  className="p-1 rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-800 text-neutral-500"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <nav className="flex-grow space-y-1 overflow-y-auto">
                {links.map((link) => {
                  const Icon = link.icon;
                  const isActive = location.pathname === link.path;
                  return (
                    <Link
                      key={link.name}
                      to={link.path}
                      onClick={() => setIsSidebarOpen(false)}
                      className={`flex items-center justify-between px-3 py-2.5 rounded-xl text-sm font-medium transition-colors ${
                        isActive
                          ? 'bg-primary-500 text-white'
                          : 'text-neutral-600 dark:text-neutral-400 hover:bg-neutral-100 dark:hover:bg-neutral-800'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <Icon className="w-5 h-5" />
                        <span>{link.name}</span>
                      </div>
                      {link.badge > 0 && (
                        <span className={`px-2 py-0.5 rounded-full text-xs font-bold ${
                          isActive ? 'bg-white text-primary-600' : 'bg-primary-500 text-white'
                        }`}>
                          {link.badge}
                        </span>
                      )}
                    </Link>
                  );
                })}
              </nav>

              <div className="border-t border-neutral-200 dark:border-neutral-800 pt-4 mt-4">
                <button
                  onClick={() => {
                    setIsSidebarOpen(false);
                    logout();
                  }}
                  className="flex items-center gap-3 w-full px-3 py-2.5 rounded-xl text-sm font-medium text-rose-500 hover:bg-rose-50 dark:hover:bg-rose-950/20 transition-colors"
                >
                  <LogOut className="w-5 h-5" />
                  <span>Logout</span>
                </button>
              </div>
            </aside>
          </div>
        )}

        {/* Dashboard Main Workspace */}
        <main className="flex-grow p-4 sm:p-6 lg:p-8 max-w-7xl w-full mx-auto overflow-x-hidden">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
