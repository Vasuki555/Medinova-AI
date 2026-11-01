/**
 * Doctor QR Code Page
 * Doctors can view, download, and share their professional QR code
 * Patients scan this QR to instantly book appointments
 */

import { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { API_BASE_URL } from '@/utils/constants';
import {
  QrCode, Download, Share2, User, Calendar,
  CheckCircle, AlertCircle, Loader2, Copy,
  Stethoscope, Clock, MapPin, ShieldCheck, Users
} from 'lucide-react';

const DoctorQRCode = () => {
  const { user } = useAuth();
  const [qrLoading, setQrLoading] = useState(true);
  const [qrError, setQrError] = useState('');
  const [copied, setCopied] = useState(false);
  const [stats, setStats] = useState({ scans: 0, bookings: 0 });

  useEffect(() => {
    // Simulate loading QR
    setTimeout(() => setQrLoading(false), 500);
  }, []);

  const downloadQR = async () => {
    try {
      const token = sessionStorage.getItem('accessToken') || localStorage.getItem('accessToken');
      const response = await fetch(`${API_BASE_URL}/qr/doctor/${user._id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!response.ok) throw new Error('Download failed');
      const blob = await response.blob();
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `MediNova_Doctor_QR_${user.first_name}_${user.last_name}.png`;
      link.click();
      URL.revokeObjectURL(link.href);
    } catch (err) {
      alert('Failed to download QR code. ' + err.message);
    }
  };

  const copyDoctorId = async () => {
    try {
      await navigator.clipboard.writeText(user._id);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      alert('Could not copy to clipboard');
    }
  };

  const shareQR = async () => {
    const shareData = {
      title: `Dr. ${user.first_name} ${user.last_name} - MediNova`,
      text: `Book an appointment with Dr. ${user.first_name} ${user.last_name}`,
      url: `${window.location.origin}/patient/booking?doctor_id=${user._id}`
    };

    if (navigator.share && navigator.canShare(shareData)) {
      try {
        await navigator.share(shareData);
      } catch (err) {
        if (err.name !== 'AbortError') {
          copyDoctorId();
        }
      }
    } else {
      copyDoctorId();
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-neutral-900 dark:text-white flex items-center gap-2">
          <QrCode className="w-6 h-6 text-primary-500" />
          Your Professional QR Code
        </h1>
        <p className="text-neutral-500 dark:text-neutral-400 mt-1">
          Share your QR code with patients for instant appointment booking
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* QR Code Card */}
        <div className="bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 shadow-sm overflow-hidden">
          <div className="bg-gradient-to-r from-violet-500 to-purple-500 p-6 text-white">
            <div className="flex items-center gap-3">
              <ShieldCheck className="w-6 h-6" />
              <div>
                <h2 className="font-bold text-lg">Doctor QR Code</h2>
                <p className="text-violet-100 text-sm">For patient appointment booking</p>
              </div>
            </div>
          </div>

          <div className="p-6 flex flex-col items-center">
            {/* QR Image */}
            <div className="relative">
              <div className="w-56 h-56 bg-neutral-50 dark:bg-neutral-700 rounded-2xl border-2 border-dashed border-neutral-200 dark:border-neutral-600 flex items-center justify-center overflow-hidden">
                <QRImageDisplay userId={user?._id} type="doctor" />
              </div>
              {/* Corner decorators */}
              {['top-2 left-2', 'top-2 right-2', 'bottom-2 left-2', 'bottom-2 right-2'].map(pos => (
                <div key={pos} className={`absolute ${pos} w-4 h-4 border-2 border-violet-500 rounded-sm`} />
              ))}
            </div>

            {/* Doctor Info */}
            <div className="mt-4 text-center">
              <p className="font-bold text-neutral-900 dark:text-white text-lg">
                Dr. {user?.first_name} {user?.last_name}
              </p>
              <p className="text-sm text-violet-500 font-medium">Medical Professional</p>
              <div className="flex items-center gap-2 mt-2 justify-center">
                <code className="text-xs text-neutral-400 bg-neutral-100 dark:bg-neutral-700 px-2 py-1 rounded-lg">
                  {user?._id?.slice(0, 16)}...
                </code>
                <button
                  onClick={copyDoctorId}
                  className="p-1 hover:bg-neutral-100 dark:hover:bg-neutral-700 rounded-lg transition-colors"
                  title="Copy Doctor ID"
                >
                  {copied
                    ? <CheckCircle className="w-4 h-4 text-emerald-500" />
                    : <Copy className="w-4 h-4 text-neutral-400" />
                  }
                </button>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3 mt-5 w-full">
              <button
                onClick={downloadQR}
                className="flex-1 flex items-center justify-center gap-2 bg-violet-500 hover:bg-violet-600 text-white text-sm font-semibold py-2.5 rounded-xl transition-colors"
              >
                <Download className="w-4 h-4" />
                Download
              </button>
              <button
                onClick={shareQR}
                className="flex-1 flex items-center justify-center gap-2 bg-neutral-100 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 text-sm font-semibold py-2.5 rounded-xl hover:bg-neutral-200 dark:hover:bg-neutral-600 transition-colors"
              >
                <Share2 className="w-4 h-4" />
                Share
              </button>
            </div>

            {/* Print Button */}
            <button
              onClick={() => window.print()}
              className="mt-2 w-full flex items-center justify-center gap-2 bg-neutral-50 dark:bg-neutral-700/50 text-neutral-600 dark:text-neutral-300 text-sm font-medium py-2 rounded-xl hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors border border-neutral-200 dark:border-neutral-600"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
              </svg>
              Print QR Code
            </button>
          </div>
        </div>

        {/* Right Panel */}
        <div className="space-y-4">
          {/* How it works */}
          <div className="bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 p-5 shadow-sm">
            <h3 className="font-bold text-neutral-900 dark:text-white mb-4 flex items-center gap-2">
              <Stethoscope className="w-4 h-4 text-violet-500" />
              How Patients Use Your QR
            </h3>
            <div className="space-y-3">
              {[
                { icon: QrCode, title: 'Patient Scans QR', desc: 'Patient scans your QR code using their phone camera or MediNova app', color: 'text-blue-500 bg-blue-50 dark:bg-blue-900/20' },
                { icon: User, title: 'Opens Your Profile', desc: 'Automatically opens your doctor profile with specialization and availability', color: 'text-violet-500 bg-violet-50 dark:bg-violet-900/20' },
                { icon: Calendar, title: 'Books Appointment', desc: 'Patient can instantly book an appointment with you', color: 'text-emerald-500 bg-emerald-50 dark:bg-emerald-900/20' },
              ].map(step => (
                <div key={step.title} className="flex items-start gap-3">
                  <div className={`w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0 ${step.color}`}>
                    <step.icon className="w-4 h-4" />
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-neutral-900 dark:text-white">{step.title}</p>
                    <p className="text-xs text-neutral-500 dark:text-neutral-400">{step.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Stats Card */}
          <div className="bg-gradient-to-br from-violet-50 to-purple-50 dark:from-violet-900/20 dark:to-purple-900/20 rounded-2xl border border-violet-200 dark:border-violet-800 p-5">
            <h3 className="font-bold text-neutral-900 dark:text-white mb-3 flex items-center gap-2">
              <Users className="w-4 h-4 text-violet-500" />
              QR Code Analytics
            </h3>
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-white/50 dark:bg-neutral-800/50 rounded-xl p-3">
                <p className="text-2xl font-bold text-violet-600 dark:text-violet-400">{stats.scans}</p>
                <p className="text-xs text-neutral-600 dark:text-neutral-400 mt-1">Total Scans</p>
              </div>
              <div className="bg-white/50 dark:bg-neutral-800/50 rounded-xl p-3">
                <p className="text-2xl font-bold text-emerald-600 dark:text-emerald-400">{stats.bookings}</p>
                <p className="text-xs text-neutral-600 dark:text-neutral-400 mt-1">Bookings via QR</p>
              </div>
            </div>
          </div>

          {/* Usage Tips */}
          <div className="bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 p-5 shadow-sm">
            <h3 className="font-bold text-neutral-900 dark:text-white mb-3 flex items-center gap-2">
              <MapPin className="w-4 h-4 text-violet-500" />
              Where to Display Your QR
            </h3>
            <ul className="space-y-2 text-sm text-neutral-600 dark:text-neutral-400">
              <li className="flex items-start gap-2">
                <CheckCircle className="w-4 h-4 text-emerald-500 mt-0.5 flex-shrink-0" />
                <span>Print and display in your clinic waiting room</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle className="w-4 h-4 text-emerald-500 mt-0.5 flex-shrink-0" />
                <span>Add to your business cards and letterhead</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle className="w-4 h-4 text-emerald-500 mt-0.5 flex-shrink-0" />
                <span>Share via email or messaging apps with patients</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle className="w-4 h-4 text-emerald-500 mt-0.5 flex-shrink-0" />
                <span>Include in your hospital/clinic directory</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

// Subcomponent: Fetches and displays QR image with auth token
const QRImageDisplay = ({ userId, type = 'doctor' }) => {
  const [src, setSrc] = useState('');
  const [error, setError] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!userId) return;
    const token = sessionStorage.getItem('accessToken') || localStorage.getItem('accessToken');
    fetch(`${API_BASE_URL}/qr/${type}/${userId}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => {
        if (!res.ok) throw new Error('QR fetch failed');
        return res.blob();
      })
      .then(blob => {
        setSrc(URL.createObjectURL(blob));
        setLoading(false);
      })
      .catch(err => {
        console.error('QR load error:', err);
        setError(true);
        setLoading(false);
      });
  }, [userId, type]);

  if (loading) return <Loader2 className="w-8 h-8 text-violet-400 animate-spin" />;

  if (error) return (
    <div className="text-center p-4">
      <AlertCircle className="w-8 h-8 text-amber-400 mx-auto mb-2" />
      <p className="text-xs text-neutral-500">QR generation failed</p>
      <p className="text-xs text-neutral-400 mt-1">Check backend connection</p>
    </div>
  );

  return <img src={src} alt="Doctor QR Code" className="w-full h-full object-contain p-2" />;
};

export default DoctorQRCode;
