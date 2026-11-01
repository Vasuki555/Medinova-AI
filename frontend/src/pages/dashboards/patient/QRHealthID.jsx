/**
 * Smart QR Health ID Page
 * Patient can view, download, and share their unique QR health ID
 * Also supports scanning a QR code to view doctor profile / book appointment
 */

import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { API_BASE_URL } from '@/utils/constants';
import QRScanner from '@/components/common/QRScanner';
import {
  QrCode, Download, Share2, Scan, User, Stethoscope,
  Calendar, CheckCircle, AlertCircle, Loader2, Camera,
  Copy, ExternalLink, ShieldCheck
} from 'lucide-react';

const QRHealthID = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [qrUrl, setQrUrl] = useState('');
  const [qrLoading, setQrLoading] = useState(true);
  const [qrError, setQrError] = useState('');

  // Scanner state
  const [scanInput, setScanInput] = useState('');
  const [scanResult, setScanResult] = useState(null);
  const [scanLoading, setScanLoading] = useState(false);
  const [scanError, setScanError] = useState('');
  const [showCameraScanner, setShowCameraScanner] = useState(false);

  const [copied, setCopied] = useState(false);

  // Build authenticated QR image URL
  useEffect(() => {
    if (!user?._id) return;
    const url = `${API_BASE_URL}/qr/patient/${user._id}`;
    setQrUrl(url);
    setQrLoading(false);
  }, [user]);

  const downloadQR = async () => {
    try {
      const token = sessionStorage.getItem('accessToken') || localStorage.getItem('accessToken');
      const response = await fetch(`${API_BASE_URL}/qr/patient/${user._id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!response.ok) throw new Error('Download failed');
      const blob = await response.blob();
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `MediNova_QR_${user.first_name}_${user.last_name}.png`;
      link.click();
      URL.revokeObjectURL(link.href);
    } catch (err) {
      alert('Failed to download QR code. ' + err.message);
    }
  };

  const copyPatientId = async () => {
    try {
      await navigator.clipboard.writeText(user._id);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      alert('Could not copy to clipboard');
    }
  };

  const handleScanQR = async () => {
    if (!scanInput.trim()) {
      setScanError('Please paste the QR code data to scan');
      return;
    }
    setScanLoading(true);
    setScanError('');
    setScanResult(null);

    try {
      const token = sessionStorage.getItem('accessToken') || localStorage.getItem('accessToken');
      const response = await fetch(`${API_BASE_URL}/qr/scan`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ qr_data: scanInput.trim() })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Scan failed');
      setScanResult(data);
    } catch (err) {
      setScanError(err.message || 'Invalid QR code. Please scan a valid MediNova QR.');
    } finally {
      setScanLoading(false);
    }
  };

  const handleScanAction = () => {
    if (!scanResult) return;
    if (scanResult.type === 'doctor') {
      navigate(`/patient/booking?doctor_id=${scanResult.doctor_id}`);
    }
  };

  const handleCameraScan = async (decodedText) => {
    setShowCameraScanner(false);
    setScanInput(decodedText);
    setScanLoading(true);
    setScanError('');
    setScanResult(null);

    try {
      const token = sessionStorage.getItem('accessToken') || localStorage.getItem('accessToken');
      const response = await fetch(`${API_BASE_URL}/qr/scan`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ qr_data: decodedText })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Scan failed');
      setScanResult(data);
    } catch (err) {
      setScanError(err.message || 'Invalid QR code. Please scan a valid MediNova QR.');
    } finally {
      setScanLoading(false);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-neutral-900 dark:text-white flex items-center gap-2">
          <QrCode className="w-6 h-6 text-primary-500" />
          Smart QR Health ID
        </h1>
        <p className="text-neutral-500 dark:text-neutral-400 mt-1">
          Your unique digital health identity — share with doctors for instant access to your profile.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* QR Code Card */}
        <div className="bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 shadow-sm overflow-hidden">
          <div className="bg-gradient-to-r from-primary-500 to-cyan-500 p-6 text-white">
            <div className="flex items-center gap-3">
              <ShieldCheck className="w-6 h-6" />
              <div>
                <h2 className="font-bold text-lg">Your Health QR Code</h2>
                <p className="text-primary-100 text-sm">Scan to open your patient profile</p>
              </div>
            </div>
          </div>

          <div className="p-6 flex flex-col items-center">
            {/* QR Image */}
            <div className="relative">
              <div className="w-56 h-56 bg-neutral-50 dark:bg-neutral-700 rounded-2xl border-2 border-dashed border-neutral-200 dark:border-neutral-600 flex items-center justify-center overflow-hidden">
                {qrLoading ? (
                  <Loader2 className="w-8 h-8 text-primary-400 animate-spin" />
                ) : qrError ? (
                  <div className="text-center p-4">
                    <AlertCircle className="w-8 h-8 text-red-400 mx-auto mb-2" />
                    <p className="text-xs text-neutral-500">{qrError}</p>
                  </div>
                ) : (
                  <QRImageDisplay userId={user?._id} />
                )}
              </div>
              {/* Corner decorators */}
              {['top-2 left-2', 'top-2 right-2', 'bottom-2 left-2', 'bottom-2 right-2'].map(pos => (
                <div key={pos} className={`absolute ${pos} w-4 h-4 border-2 border-primary-500 rounded-sm`} />
              ))}
            </div>

            {/* Patient Info */}
            <div className="mt-4 text-center">
              <p className="font-bold text-neutral-900 dark:text-white text-lg">
                {user?.first_name} {user?.last_name}
              </p>
              <p className="text-sm text-primary-500 font-medium">Patient</p>
              <div className="flex items-center gap-2 mt-2 justify-center">
                <code className="text-xs text-neutral-400 bg-neutral-100 dark:bg-neutral-700 px-2 py-1 rounded-lg">
                  {user?._id?.slice(0, 16)}...
                </code>
                <button
                  onClick={copyPatientId}
                  className="p-1 hover:bg-neutral-100 dark:hover:bg-neutral-700 rounded-lg transition-colors"
                  title="Copy Patient ID"
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
                className="flex-1 flex items-center justify-center gap-2 bg-primary-500 hover:bg-primary-600 text-white text-sm font-semibold py-2.5 rounded-xl transition-colors"
              >
                <Download className="w-4 h-4" />
                Download
              </button>
              <button
                onClick={async () => {
                  if (navigator.share) {
                    try {
                      await navigator.share({
                        title: 'MediNova Health ID',
                        text: `My MediNova Patient ID: ${user?._id}`,
                      });
                    } catch { /* user cancelled */ }
                  } else {
                    copyPatientId();
                  }
                }}
                className="flex-1 flex items-center justify-center gap-2 bg-neutral-100 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 text-sm font-semibold py-2.5 rounded-xl hover:bg-neutral-200 dark:hover:bg-neutral-600 transition-colors"
              >
                <Share2 className="w-4 h-4" />
                Share
              </button>
            </div>
          </div>
        </div>

        {/* Right Panel */}
        <div className="space-y-4">
          {/* How it works */}
          <div className="bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 p-5 shadow-sm">
            <h3 className="font-bold text-neutral-900 dark:text-white mb-4 flex items-center gap-2">
              <QrCode className="w-4 h-4 text-primary-500" />
              How It Works
            </h3>
            <div className="space-y-3">
              {[
                { icon: User, title: 'Show Your QR', desc: 'Present your QR code to any doctor at the clinic', color: 'text-blue-500 bg-blue-50 dark:bg-blue-900/20' },
                { icon: Stethoscope, title: 'Doctor Scans', desc: 'Doctor scans and instantly views your complete health profile', color: 'text-violet-500 bg-violet-50 dark:bg-violet-900/20' },
                { icon: Calendar, title: 'Scan Doctor QR', desc: 'Scan a doctor\'s QR code to instantly open their booking page', color: 'text-emerald-500 bg-emerald-50 dark:bg-emerald-900/20' },
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

          {/* QR Scanner / Paste */}
          <div className="bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 p-5 shadow-sm">
            <h3 className="font-bold text-neutral-900 dark:text-white mb-3 flex items-center gap-2">
              <Scan className="w-4 h-4 text-primary-500" />
              Scan a Doctor's QR Code
            </h3>
            
            {/* Camera Scan Button */}
            <button
              onClick={() => setShowCameraScanner(true)}
              className="w-full mb-3 flex items-center justify-center gap-2 bg-gradient-to-r from-primary-500 to-cyan-500 hover:from-primary-600 hover:to-cyan-600 text-white text-sm font-semibold py-3 rounded-xl transition-all shadow-lg shadow-primary-500/20"
            >
              <Camera className="w-5 h-5" />
              Scan with Camera
            </button>
            <p className="text-xs text-neutral-500 dark:text-neutral-400 mb-3">
              Paste the JSON data decoded from a MediNova doctor QR code to open their profile.
            </p>
            <textarea
              value={scanInput}
              onChange={e => setScanInput(e.target.value)}
              placeholder='Paste QR data here, e.g. {"type":"medinova_doctor","doctor_id":"..."}'
              rows={3}
              className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-xl text-xs focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white resize-none"
            />
            {scanError && (
              <p className="text-xs text-red-500 mt-1 flex items-center gap-1">
                <AlertCircle className="w-3 h-3" /> {scanError}
              </p>
            )}
            <button
              onClick={handleScanQR}
              disabled={scanLoading || !scanInput.trim()}
              className="mt-2 w-full flex items-center justify-center gap-2 bg-primary-500 hover:bg-primary-600 disabled:opacity-50 text-white text-sm font-semibold py-2.5 rounded-xl transition-colors"
            >
              {scanLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Scan className="w-4 h-4" />}
              {scanLoading ? 'Processing...' : 'Process QR Data'}
            </button>

            {/* Scan Result */}
            {scanResult && (
              <div className="mt-3 p-3 bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-xl">
                <div className="flex items-center gap-2 mb-2">
                  <CheckCircle className="w-4 h-4 text-emerald-500" />
                  <p className="text-sm font-semibold text-emerald-800 dark:text-emerald-300">QR Decoded Successfully</p>
                </div>
                <p className="text-xs text-neutral-600 dark:text-neutral-400">
                  <strong>Type:</strong> {scanResult.type === 'doctor' ? 'Doctor' : 'Patient'} Profile
                </p>
                <p className="text-xs text-neutral-600 dark:text-neutral-400">
                  <strong>Name:</strong> {scanResult.name}
                </p>
                {scanResult.specialization && (
                  <p className="text-xs text-neutral-600 dark:text-neutral-400">
                    <strong>Specialization:</strong> {scanResult.specialization}
                  </p>
                )}
                {scanResult.type === 'doctor' && (
                  <button
                    onClick={handleScanAction}
                    className="mt-2 w-full flex items-center justify-center gap-2 bg-emerald-500 hover:bg-emerald-600 text-white text-xs font-semibold py-2 rounded-xl transition-colors"
                  >
                    <Calendar className="w-3.5 h-3.5" />
                    Book Appointment with {scanResult.name}
                  </button>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Camera Scanner Modal */}
      {showCameraScanner && (
        <QRScanner 
          onScan={handleCameraScan} 
          onClose={() => setShowCameraScanner(false)} 
        />
      )}
    </div>
  );
};

// Subcomponent: Fetches and displays QR image with auth token
const QRImageDisplay = ({ userId }) => {
  const [src, setSrc] = useState('');
  const [error, setError] = useState(false);

  useEffect(() => {
    if (!userId) return;
    const token = sessionStorage.getItem('accessToken') || localStorage.getItem('accessToken');
    fetch(`${API_BASE_URL}/qr/patient/${userId}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => {
        if (!res.ok) throw new Error('QR fetch failed');
        return res.blob();
      })
      .then(blob => setSrc(URL.createObjectURL(blob)))
      .catch(() => setError(true));
  }, [userId]);

  if (error) return (
    <div className="text-center p-4">
      <AlertCircle className="w-8 h-8 text-amber-400 mx-auto mb-2" />
      <p className="text-xs text-neutral-500">QR generation failed</p>
    </div>
  );

  if (!src) return <Loader2 className="w-8 h-8 text-primary-400 animate-spin" />;

  return <img src={src} alt="Patient QR Code" className="w-full h-full object-contain p-2" />;
};

export default QRHealthID;
