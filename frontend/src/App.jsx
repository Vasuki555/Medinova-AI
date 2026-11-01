/**
 * App Component
 * Root component with full routing configuration for all roles
 */

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from '@/context/AuthContext';
import { ThemeProvider } from '@/context/ThemeContext';
import { ToastProvider } from '@/context/ToastContext';
import Layout from '@/components/layout/Layout';
import PrivateRoute from '@/components/auth/PrivateRoute';
import PublicRoute from '@/components/auth/PublicRoute';

// Public Pages
import Home from '@/pages/Home';
import Login from '@/pages/auth/Login';
import Register from '@/pages/auth/Register';
import ForgotPassword from '@/pages/auth/ForgotPassword';
import GoogleCallback from '@/pages/auth/GoogleCallback';
import Unauthorized from '@/pages/Unauthorized';
import NotFound from '@/pages/NotFound';

// Dashboard Wrappers (use DashboardLayout + Outlet)
import PatientDashboard from '@/pages/dashboards/PatientDashboard';
import DoctorDashboard from '@/pages/dashboards/DoctorDashboard';
import AdminDashboard from '@/pages/dashboards/AdminDashboard';

// Patient Sub-Pages
import PatientDashboardHome from '@/pages/dashboards/patient/PatientDashboardHome';
import BookAppointment from '@/pages/dashboards/patient/BookAppointment';
import MyAppointments from '@/pages/dashboards/patient/MyAppointments';
import HealthRecord from '@/pages/dashboards/patient/HealthRecord';
import Medications from '@/pages/dashboards/patient/Medications';
import NearbyHospitals from '@/pages/dashboards/patient/NearbyHospitals';
import PatientNotifications from '@/pages/dashboards/patient/PatientNotifications';
import AIAssistant from '@/pages/dashboards/patient/AIAssistant';
import QRHealthID from '@/pages/dashboards/patient/QRHealthID';
import PatientProfile from '@/pages/dashboards/patient/PatientProfile';
import SmartUpload from '@/pages/dashboards/patient/SmartUpload';

// Doctor Sub-Pages
import DoctorDashboardHome from '@/pages/dashboards/doctor/DoctorDashboardHome';
import DoctorAppointments from '@/pages/dashboards/doctor/DoctorAppointments';
import DoctorSchedule from '@/pages/dashboards/doctor/DoctorSchedule';
import DoctorProfile from '@/pages/dashboards/doctor/DoctorProfile';
import DoctorQRCode from '@/pages/dashboards/doctor/DoctorQRCode';
import SharedNotifications from '@/pages/dashboards/SharedNotifications';

// Admin Sub-Pages
import AdminDashboardHome from '@/pages/dashboards/admin/AdminDashboardHome';
import UserManagement from '@/pages/dashboards/admin/UserManagement';
import DoctorVerification from '@/pages/dashboards/admin/DoctorVerification';

function App() {
  return (
    <BrowserRouter>
      <ThemeProvider>
        <ToastProvider>
          <AuthProvider>
            <Routes>
              {/* Public Routes (Home - standalone, has its own nav/footer) */}
              <Route path="/" element={<Home />} />

              {/* Authentication Routes (redirect if already authenticated) */}
              <Route path="/login" element={<PublicRoute><Login /></PublicRoute>} />
              <Route path="/register" element={<PublicRoute><Register /></PublicRoute>} />
              <Route path="/forgot-password" element={<ForgotPassword />} />
              <Route path="/auth/google/callback" element={<GoogleCallback />} />

              {/* ─── PATIENT ROUTES ─── */}
              <Route
                path="/patient"
                element={
                  <PrivateRoute roles={['patient']}>
                    <PatientDashboard />
                  </PrivateRoute>
                }
              >
                <Route index element={<PatientDashboardHome />} />
                <Route path="dashboard" element={<PatientDashboardHome />} />
                <Route path="booking" element={<BookAppointment />} />
                <Route path="appointments" element={<MyAppointments />} />
                <Route path="phr" element={<HealthRecord />} />
                <Route path="medications" element={<Medications />} />
                <Route path="hospitals" element={<NearbyHospitals />} />
                <Route path="notifications" element={<PatientNotifications />} />
                <Route path="ai-assistant" element={<AIAssistant />} />
                <Route path="smart-upload" element={<SmartUpload />} />
                <Route path="qr-id" element={<QRHealthID />} />
                <Route path="profile" element={<PatientProfile />} />
              </Route>

              {/* ─── DOCTOR ROUTES ─── */}
              <Route
                path="/doctor"
                element={
                  <PrivateRoute roles={['doctor']}>
                    <DoctorDashboard />
                  </PrivateRoute>
                }
              >
                <Route index element={<DoctorDashboardHome />} />
                <Route path="dashboard" element={<DoctorDashboardHome />} />
                <Route path="appointments" element={<DoctorAppointments />} />
                <Route path="schedule" element={<DoctorSchedule />} />
                <Route path="qr-code" element={<DoctorQRCode />} />
                <Route path="profile" element={<DoctorProfile />} />
                <Route path="notifications" element={<SharedNotifications />} />
              </Route>

              {/* ─── ADMIN ROUTES ─── */}
              <Route
                path="/admin"
                element={
                  <PrivateRoute roles={['admin']}>
                    <AdminDashboard />
                  </PrivateRoute>
                }
              >
                <Route index element={<AdminDashboardHome />} />
                <Route path="dashboard" element={<AdminDashboardHome />} />
                <Route path="users" element={<UserManagement />} />
                <Route path="verify" element={<DoctorVerification />} />
                <Route path="notifications" element={<SharedNotifications />} />
              </Route>

              {/* Error Pages */}
              <Route path="/unauthorized" element={<Unauthorized />} />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </AuthProvider>
        </ToastProvider>
      </ThemeProvider>
    </BrowserRouter>
  );
}

export default App;
