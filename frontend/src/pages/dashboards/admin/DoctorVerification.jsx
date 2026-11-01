/**
 * Admin - Doctor Verification
 * Review and verify doctor credentials
 */

import { useState, useEffect } from 'react';
import { apiService } from '@/services/api';
import {
  Shield, CheckCircle, Clock, Star, Award,
  ChevronDown, ChevronUp, RefreshCw, Stethoscope,
  AlertTriangle, Building2, Globe
} from 'lucide-react';

const DoctorVerificationCard = ({ doctor, onVerify }) => {
  const [expanded, setExpanded] = useState(false);
  const [verifying, setVerifying] = useState(false);

  const handleVerify = async () => {
    setVerifying(true);
    try {
      await apiService.post(`/admin/verify-doctor/${doctor.user_id}`);
      onVerify(doctor.user_id);
    } catch (err) {
      alert(err.response?.data?.detail || 'Verification failed');
    } finally {
      setVerifying(false);
    }
  };

  return (
    <div className="bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 shadow-sm overflow-hidden">
      <div className="flex items-center gap-4 p-5 cursor-pointer" onClick={() => setExpanded(e => !e)}>
        <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-violet-400 to-violet-600 flex items-center justify-center text-white font-bold text-lg flex-shrink-0">
          {(doctor.first_name || 'D')[0]}
        </div>
        <div className="flex-grow min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <h3 className="font-bold text-neutral-900 dark:text-white">
              Dr. {doctor.first_name} {doctor.last_name}
            </h3>
            {doctor.is_verified ? (
              <span className="flex items-center gap-1 text-xs font-medium px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400">
                <CheckCircle className="w-3 h-3" /> Verified
              </span>
            ) : (
              <span className="flex items-center gap-1 text-xs font-medium px-2 py-0.5 rounded-full bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400">
                <Clock className="w-3 h-3" /> Pending
              </span>
            )}
          </div>
          <p className="text-sm text-violet-500 font-medium">
            {doctor.specialization || 'General Practitioner'}
          </p>
          <p className="text-xs text-neutral-400">
            {doctor.qualifications?.join(', ') || 'MBBS'} · {doctor.years_of_experience || 0} yrs exp · ₹{doctor.consultation_fee || 500}
          </p>
        </div>
        {expanded ? <ChevronUp className="w-5 h-5 text-neutral-400" /> : <ChevronDown className="w-5 h-5 text-neutral-400" />}
      </div>

      {expanded && (
        <div className="border-t border-neutral-100 dark:border-neutral-700 p-5 space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-xs text-neutral-400 uppercase tracking-wide mb-1">License Number</p>
              <p className="text-sm font-medium text-neutral-800 dark:text-white font-mono">
                {doctor.license_number || 'Not provided'}
              </p>
            </div>
            <div>
              <p className="text-xs text-neutral-400 uppercase tracking-wide mb-1">Consultation Fee</p>
              <p className="text-sm font-medium text-emerald-600 dark:text-emerald-400">
                ₹{doctor.consultation_fee || 500}
              </p>
            </div>
            <div>
              <p className="text-xs text-neutral-400 uppercase tracking-wide mb-1">Experience</p>
              <p className="text-sm font-medium text-neutral-800 dark:text-white">
                {doctor.years_of_experience || 0} years
              </p>
            </div>
            <div>
              <p className="text-xs text-neutral-400 uppercase tracking-wide mb-1">Rating</p>
              <p className="text-sm font-medium text-neutral-800 dark:text-white flex items-center gap-1">
                <Star className="w-3.5 h-3.5 text-amber-400 fill-amber-400" />
                {doctor.rating?.toFixed(1) || '5.0'}
              </p>
            </div>
            {doctor.languages_spoken?.length > 0 && (
              <div className="col-span-2">
                <p className="text-xs text-neutral-400 uppercase tracking-wide mb-2">Languages</p>
                <div className="flex flex-wrap gap-2">
                  {doctor.languages_spoken.map(lang => (
                    <span key={lang} className="text-xs bg-neutral-100 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-300 px-2 py-0.5 rounded-md flex items-center gap-1">
                      <Globe className="w-3 h-3" /> {lang}
                    </span>
                  ))}
                </div>
              </div>
            )}
            {doctor.qualifications?.length > 0 && (
              <div className="col-span-2">
                <p className="text-xs text-neutral-400 uppercase tracking-wide mb-2">Qualifications</p>
                <div className="flex flex-wrap gap-2">
                  {doctor.qualifications.map((qual, idx) => (
                    <span key={idx} className="text-xs bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400 px-2 py-0.5 rounded-md font-medium">
                      {qual}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          {doctor.bio && (
            <div>
              <p className="text-xs text-neutral-400 uppercase tracking-wide mb-1">Bio</p>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">{doctor.bio}</p>
            </div>
          )}

          {!doctor.is_verified && (
            <button
              onClick={handleVerify}
              disabled={verifying}
              className="w-full bg-emerald-500 text-white font-semibold py-3 rounded-xl hover:bg-emerald-600 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
            >
              <Shield className="w-4 h-4" />
              {verifying ? 'Verifying...' : 'Verify Doctor Credentials'}
            </button>
          )}

          {doctor.is_verified && (
            <div className="p-3 bg-emerald-50 dark:bg-emerald-900/20 rounded-xl flex items-center gap-2 text-emerald-700 dark:text-emerald-400">
              <CheckCircle className="w-4 h-4" />
              <span className="text-sm font-medium">
                Verified on {doctor.verified_at ? new Date(doctor.verified_at).toLocaleDateString() : 'N/A'}
              </span>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

const DoctorVerification = () => {
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  const loadDoctors = async () => {
    setLoading(true);
    try {
      const data = await apiService.get('/admin/doctors');
      setDoctors(data || []);
    } catch {
      setDoctors([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadDoctors(); }, []);

  const handleVerify = (userId) => {
    setDoctors(prev => prev.map(d =>
      d.user_id === userId ? { ...d, is_verified: true, verified_at: new Date().toISOString() } : d
    ));
  };

  const pendingDoctors = doctors.filter(d => !d.is_verified);
  const verifiedDoctors = doctors.filter(d => d.is_verified);
  const filtered = filter === 'pending' ? pendingDoctors : filter === 'verified' ? verifiedDoctors : doctors;

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-neutral-900 dark:text-white">Doctor Verification</h1>
          <p className="text-neutral-500 dark:text-neutral-400 mt-1">Review and approve doctor credentials</p>
        </div>
        <button onClick={loadDoctors} className="p-2 rounded-xl border border-neutral-200 dark:border-neutral-700 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors">
          <RefreshCw className={`w-4 h-4 text-neutral-500 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      {pendingDoctors.length > 0 && (
        <div className="p-4 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-2xl flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-amber-600 dark:text-amber-400 flex-shrink-0 mt-0.5" />
          <p className="text-amber-800 dark:text-amber-300 text-sm">
            <strong>{pendingDoctors.length}</strong> doctor{pendingDoctors.length > 1 ? 's' : ''} pending verification. Review their credentials below.
          </p>
        </div>
      )}

      {/* Summary Cards */}
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white dark:bg-neutral-800 rounded-2xl p-4 border border-neutral-200 dark:border-neutral-700 text-center">
          <p className="text-2xl font-black text-neutral-800 dark:text-white">{doctors.length}</p>
          <p className="text-xs text-neutral-500 mt-1">Total Doctors</p>
        </div>
        <div className="bg-white dark:bg-neutral-800 rounded-2xl p-4 border border-neutral-200 dark:border-neutral-700 text-center">
          <p className="text-2xl font-black text-emerald-500">{verifiedDoctors.length}</p>
          <p className="text-xs text-neutral-500 mt-1">Verified</p>
        </div>
        <div className="bg-white dark:bg-neutral-800 rounded-2xl p-4 border border-neutral-200 dark:border-neutral-700 text-center">
          <p className="text-2xl font-black text-amber-500">{pendingDoctors.length}</p>
          <p className="text-xs text-neutral-500 mt-1">Pending</p>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex gap-2">
        {[
          { key: 'all', label: 'All Doctors', count: doctors.length },
          { key: 'pending', label: 'Pending', count: pendingDoctors.length },
          { key: 'verified', label: 'Verified', count: verifiedDoctors.length },
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
            <span className={`text-xs px-1.5 py-0.5 rounded-full ${
              filter === tab.key ? 'bg-white/20 text-white' : 'bg-neutral-200 dark:bg-neutral-600 text-neutral-600 dark:text-neutral-300'
            }`}>
              {tab.count}
            </span>
          </button>
        ))}
      </div>

      {loading ? (
        <div className="space-y-4">
          {[1, 2, 3].map(i => (
            <div key={i} className="h-24 bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 animate-pulse" />
          ))}
        </div>
      ) : filtered.length > 0 ? (
        <div className="space-y-4">
          {filtered.map(doc => (
            <DoctorVerificationCard key={doc.user_id} doctor={doc} onVerify={handleVerify} />
          ))}
        </div>
      ) : (
        <div className="text-center py-16">
          <Stethoscope className="w-12 h-12 text-neutral-300 mx-auto mb-3" />
          <p className="text-neutral-500 font-medium">
            {filter === 'pending' ? 'No doctors pending verification' : 'No doctors found'}
          </p>
        </div>
      )}
    </div>
  );
};

export default DoctorVerification;
