/**
 * Admin - User Management
 * View all users, search, filter by role
 */

import { useState, useEffect } from 'react';
import { apiService } from '@/services/api';
import {
  Search, Users, User, Stethoscope, Shield,
  CheckCircle, XCircle, RefreshCw, Filter, Eye, X,
  MapPin, Phone, Mail, DollarSign, Clock, Award,
  Activity, FileText, Pill, Calendar
} from 'lucide-react';

const roleConfig = {
  patient: { color: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400', icon: User },
  doctor: { color: 'bg-violet-100 text-violet-700 dark:bg-violet-900/30 dark:text-violet-400', icon: Stethoscope },
  admin: { color: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400', icon: Shield },
};

const PatientDetailsModal = ({ patient, onClose }) => {
  const [patientData, setPatientData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadPatientDetails = async () => {
      setLoading(true);
      try {
        // Fetch patient profile, health records, medications, and appointments
        const [profile, healthRecords, medications, appointments] = await Promise.all([
          apiService.get(`/patients/${patient.id}`).catch(() => null),
          apiService.get(`/health-records`).catch(() => []),
          apiService.get(`/medications`).catch(() => []),
          apiService.get(`/appointments`).catch(() => [])
        ]);

        setPatientData({
          profile,
          healthRecords: Array.isArray(healthRecords) ? healthRecords : [],
          medications: Array.isArray(medications) ? medications.filter(m => m.patient_id === patient.id) : [],
          appointments: Array.isArray(appointments) ? appointments.filter(a => a.patient_id === patient.id) : []
        });
      } catch (err) {
        console.error('Error loading patient details:', err);
        setPatientData({ profile: null, healthRecords: [], medications: [], appointments: [] });
      } finally {
        setLoading(false);
      }
    };

    loadPatientDetails();
  }, [patient.id]);

  if (!patient) return null;

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-fade-in" onClick={onClose}>
      <div 
        className="bg-white dark:bg-neutral-800 rounded-2xl max-w-5xl w-full max-h-[90vh] overflow-y-auto shadow-2xl animate-scale-in"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="sticky top-0 bg-gradient-to-br from-blue-500 to-blue-600 text-white p-6 rounded-t-2xl z-10">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-4">
              <div className="w-20 h-20 rounded-2xl bg-white/20 backdrop-blur-sm flex items-center justify-center text-3xl font-bold border-2 border-white/30">
                {(patient.first_name || 'P')[0].toUpperCase()}
              </div>
              <div>
                <h2 className="text-3xl font-bold">{patient.first_name} {patient.last_name}</h2>
                <p className="text-blue-100 text-base mt-1">Patient Profile</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-2 hover:bg-white/10 rounded-xl transition-colors"
            >
              <X className="w-6 h-6" />
            </button>
          </div>
        </div>

        {loading ? (
          <div className="p-12 text-center">
            <div className="animate-spin w-12 h-12 border-4 border-primary-500 border-t-transparent rounded-full mx-auto mb-4"></div>
            <p className="text-neutral-500">Loading patient details...</p>
          </div>
        ) : (
          <div className="p-6">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Left Column - Patient Info */}
              <div className="lg:col-span-1 space-y-4">
                {/* Contact Card */}
                <div className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-xl p-4 border border-blue-200 dark:border-blue-800">
                  <h3 className="font-semibold text-neutral-900 dark:text-white mb-3 flex items-center gap-2">
                    <User className="w-5 h-5 text-blue-600" />
                    Contact Information
                  </h3>
                  <div className="space-y-3">
                    <div className="flex items-center gap-2 text-sm">
                      <Mail className="w-4 h-4 text-neutral-400" />
                      <span className="text-neutral-600 dark:text-neutral-300">{patient.email}</span>
                    </div>
                    {patient.phone && (
                      <div className="flex items-center gap-2 text-sm">
                        <Phone className="w-4 h-4 text-neutral-400" />
                        <span className="text-neutral-600 dark:text-neutral-300">{patient.phone}</span>
                      </div>
                    )}
                  </div>
                </div>

                {/* Account Status */}
                <div className={`rounded-xl p-4 border ${
                  patient.is_active !== false
                    ? 'bg-gradient-to-br from-emerald-50 to-green-50 dark:from-emerald-900/20 dark:to-green-900/20 border-emerald-200 dark:border-emerald-800'
                    : 'bg-gradient-to-br from-red-50 to-rose-50 dark:from-red-900/20 dark:to-rose-900/20 border-red-200 dark:border-red-800'
                }`}>
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-semibold text-neutral-900 dark:text-white text-sm mb-1">
                        Account Status
                      </h3>
                      <p className={`text-sm font-medium ${
                        patient.is_active !== false 
                          ? 'text-emerald-700 dark:text-emerald-400' 
                          : 'text-red-700 dark:text-red-400'
                      }`}>
                        {patient.is_active !== false ? 'Active' : 'Inactive'}
                      </p>
                    </div>
                    {patient.is_active !== false ? (
                      <CheckCircle className="w-8 h-8 text-emerald-600" />
                    ) : (
                      <XCircle className="w-8 h-8 text-red-600" />
                    )}
                  </div>
                  <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-2">
                    Member since {new Date(patient.created_at).toLocaleDateString('en', { 
                      month: 'long', 
                      year: 'numeric' 
                    })}
                  </p>
                </div>

                {/* Quick Stats */}
                <div className="bg-white dark:bg-neutral-700/50 rounded-xl p-4 border border-neutral-200 dark:border-neutral-700">
                  <h3 className="font-semibold text-neutral-900 dark:text-white mb-3">Quick Stats</h3>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-neutral-500">Total Appointments</span>
                      <span className="text-lg font-bold text-blue-600">{patientData?.appointments?.length || 0}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-neutral-500">Health Records</span>
                      <span className="text-lg font-bold text-emerald-600">{patientData?.healthRecords?.length || 0}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-neutral-500">Active Medications</span>
                      <span className="text-lg font-bold text-amber-600">
                        {patientData?.medications?.filter(m => m.is_active).length || 0}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Right Column - Medical History */}
              <div className="lg:col-span-2 space-y-6">
                {/* Health Records */}
                <div className="bg-white dark:bg-neutral-700/50 rounded-xl p-5 border border-neutral-200 dark:border-neutral-700">
                  <h3 className="text-lg font-semibold text-neutral-900 dark:text-white mb-4 flex items-center gap-2">
                    <FileText className="w-5 h-5 text-primary-500" />
                    Health Records ({patientData?.healthRecords?.length || 0})
                  </h3>
                  {patientData?.healthRecords && patientData.healthRecords.length > 0 ? (
                    <div className="space-y-3 max-h-64 overflow-y-auto">
                      {patientData.healthRecords.map((record, idx) => (
                        <div key={idx} className="p-4 bg-neutral-50 dark:bg-neutral-800 rounded-lg border border-neutral-200 dark:border-neutral-700">
                          <div className="flex items-start justify-between mb-2">
                            <h4 className="font-medium text-neutral-900 dark:text-white">{record.record_type || 'Medical Record'}</h4>
                            <span className="text-xs text-neutral-500">
                              {new Date(record.record_date || record.created_at).toLocaleDateString('en', { 
                                month: 'short', 
                                day: 'numeric', 
                                year: 'numeric' 
                              })}
                            </span>
                          </div>
                          {record.diagnosis && (
                            <p className="text-sm text-neutral-600 dark:text-neutral-300 mb-2">
                              <strong>Diagnosis:</strong> {record.diagnosis}
                            </p>
                          )}
                          {record.notes && (
                            <p className="text-sm text-neutral-600 dark:text-neutral-400">{record.notes}</p>
                          )}
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-center py-8 text-neutral-400">No health records found</p>
                  )}
                </div>

                {/* Medications */}
                <div className="bg-white dark:bg-neutral-700/50 rounded-xl p-5 border border-neutral-200 dark:border-neutral-700">
                  <h3 className="text-lg font-semibold text-neutral-900 dark:text-white mb-4 flex items-center gap-2">
                    <Pill className="w-5 h-5 text-primary-500" />
                    Medications ({patientData?.medications?.length || 0})
                  </h3>
                  {patientData?.medications && patientData.medications.length > 0 ? (
                    <div className="space-y-3 max-h-64 overflow-y-auto">
                      {patientData.medications.map((med, idx) => (
                        <div key={idx} className="p-4 bg-neutral-50 dark:bg-neutral-800 rounded-lg border border-neutral-200 dark:border-neutral-700">
                          <div className="flex items-start justify-between mb-2">
                            <div>
                              <h4 className="font-medium text-neutral-900 dark:text-white">{med.medication_name}</h4>
                              <p className="text-sm text-neutral-500">{med.dosage} - {med.frequency}</p>
                            </div>
                            <span className={`text-xs px-2 py-1 rounded-full font-medium ${
                              med.is_active 
                                ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400'
                                : 'bg-neutral-200 text-neutral-600 dark:bg-neutral-700 dark:text-neutral-400'
                            }`}>
                              {med.is_active ? 'Active' : 'Completed'}
                            </span>
                          </div>
                          {med.instructions && (
                            <p className="text-xs text-neutral-600 dark:text-neutral-400 mt-2">{med.instructions}</p>
                          )}
                          <p className="text-xs text-neutral-400 mt-2">
                            {new Date(med.start_date).toLocaleDateString()} - {med.end_date ? new Date(med.end_date).toLocaleDateString() : 'Ongoing'}
                          </p>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-center py-8 text-neutral-400">No medications found</p>
                  )}
                </div>

                {/* Recent Appointments */}
                <div className="bg-white dark:bg-neutral-700/50 rounded-xl p-5 border border-neutral-200 dark:border-neutral-700">
                  <h3 className="text-lg font-semibold text-neutral-900 dark:text-white mb-4 flex items-center gap-2">
                    <Calendar className="w-5 h-5 text-primary-500" />
                    Appointments ({patientData?.appointments?.length || 0})
                  </h3>
                  {patientData?.appointments && patientData.appointments.length > 0 ? (
                    <div className="space-y-3 max-h-64 overflow-y-auto">
                      {patientData.appointments.slice(0, 10).map((apt, idx) => (
                        <div key={idx} className="p-4 bg-neutral-50 dark:bg-neutral-800 rounded-lg border border-neutral-200 dark:border-neutral-700">
                          <div className="flex items-start justify-between mb-2">
                            <div>
                              <h4 className="font-medium text-neutral-900 dark:text-white">
                                {apt.doctor_name || 'Doctor Appointment'}
                              </h4>
                              <p className="text-sm text-neutral-500 mt-1">
                                {new Date(apt.appointment_date).toLocaleDateString('en', { 
                                  weekday: 'short',
                                  month: 'short', 
                                  day: 'numeric', 
                                  year: 'numeric' 
                                })} at {apt.appointment_time}
                              </p>
                            </div>
                            <span className={`text-xs px-2 py-1 rounded-full font-medium ${
                              apt.status === 'completed' 
                                ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400'
                                : apt.status === 'confirmed'
                                ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400'
                                : apt.status === 'cancelled'
                                ? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                                : 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400'
                            }`}>
                              {apt.status || 'Pending'}
                            </span>
                          </div>
                          {apt.reason && (
                            <p className="text-sm text-neutral-600 dark:text-neutral-400 mt-2">
                              <strong>Reason:</strong> {apt.reason}
                            </p>
                          )}
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-center py-8 text-neutral-400">No appointments found</p>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="sticky bottom-0 bg-neutral-50 dark:bg-neutral-900 border-t border-neutral-200 dark:border-neutral-700 p-4 rounded-b-2xl flex justify-end gap-3">
          <button
            onClick={onClose}
            className="px-6 py-2.5 bg-neutral-200 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 rounded-xl font-medium hover:bg-neutral-300 dark:hover:bg-neutral-600 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

const DoctorDetailsModal = ({ doctor, onClose }) => {
  if (!doctor) return null;

  const profile = doctor.doctorProfile;

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-fade-in" onClick={onClose}>
      <div 
        className="bg-white dark:bg-neutral-800 rounded-2xl max-w-5xl w-full max-h-[90vh] overflow-y-auto shadow-2xl animate-scale-in"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="sticky top-0 bg-gradient-to-br from-primary-500 to-primary-600 text-white p-6 rounded-t-2xl z-10">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-4">
              <div className="w-20 h-20 rounded-2xl bg-white/20 backdrop-blur-sm flex items-center justify-center text-3xl font-bold border-2 border-white/30">
                {(doctor.first_name || 'D')[0].toUpperCase()}
              </div>
              <div>
                <h2 className="text-3xl font-bold">Dr. {doctor.first_name} {doctor.last_name}</h2>
                <div className="flex items-center gap-3 mt-2">
                  <span className="text-primary-100 text-base font-medium">
                    {profile?.specialization || 'General Practitioner'}
                  </span>
                  {profile?.years_of_experience && (
                    <span className="text-primary-100 text-sm flex items-center gap-1">
                      <Award className="w-4 h-4" />
                      {profile.years_of_experience} years exp.
                    </span>
                  )}
                </div>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-2 hover:bg-white/10 rounded-xl transition-colors"
            >
              <X className="w-6 h-6" />
            </button>
          </div>
        </div>

        {/* Content - Grid Layout */}
        <div className="p-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left Column - Key Stats */}
            <div className="lg:col-span-1 space-y-4">
              {/* Quick Stats Card */}
              <div className="bg-gradient-to-br from-emerald-50 to-teal-50 dark:from-emerald-900/20 dark:to-teal-900/20 rounded-xl p-4 border border-emerald-200 dark:border-emerald-800">
                <h3 className="font-semibold text-neutral-900 dark:text-white mb-3 flex items-center gap-2">
                  <DollarSign className="w-5 h-5 text-emerald-600" />
                  Consultation Fee
                </h3>
                <p className="text-3xl font-bold text-emerald-600 dark:text-emerald-400">
                  ₹{profile?.consultation_fee || 'N/A'}
                </p>
                <p className="text-sm text-neutral-500 dark:text-neutral-400 mt-1">
                  {profile?.consultation_duration || 30} minutes session
                </p>
              </div>

              {/* Rating & Reviews */}
              {profile?.rating && (
                <div className="bg-gradient-to-br from-amber-50 to-orange-50 dark:from-amber-900/20 dark:to-orange-900/20 rounded-xl p-4 border border-amber-200 dark:border-amber-800">
                  <h3 className="font-semibold text-neutral-900 dark:text-white mb-3">Rating</h3>
                  <div className="flex items-center gap-2">
                    <span className="text-3xl font-bold text-amber-600 dark:text-amber-400">
                      {profile.rating.toFixed(1)}
                    </span>
                    <div>
                      <div className="flex gap-0.5">
                        {[...Array(5)].map((_, i) => (
                          <span key={i} className="text-amber-400">★</span>
                        ))}
                      </div>
                      <p className="text-xs text-neutral-500 dark:text-neutral-400">
                        {profile.review_count || 0} reviews
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {/* Verification Status */}
              <div className={`rounded-xl p-4 border ${
                profile?.is_verified
                  ? 'bg-gradient-to-br from-emerald-50 to-green-50 dark:from-emerald-900/20 dark:to-green-900/20 border-emerald-200 dark:border-emerald-800'
                  : 'bg-gradient-to-br from-amber-50 to-yellow-50 dark:from-amber-900/20 dark:to-yellow-900/20 border-amber-200 dark:border-amber-800'
              }`}>
                <div className="flex items-center gap-2 mb-2">
                  {profile?.is_verified ? (
                    <CheckCircle className="w-5 h-5 text-emerald-600" />
                  ) : (
                    <XCircle className="w-5 h-5 text-amber-600" />
                  )}
                  <h3 className="font-semibold text-neutral-900 dark:text-white">
                    Verification Status
                  </h3>
                </div>
                <p className={`text-sm font-medium ${
                  profile?.is_verified 
                    ? 'text-emerald-700 dark:text-emerald-400' 
                    : 'text-amber-700 dark:text-amber-400'
                }`}>
                  {profile?.is_verified ? 'Verified Doctor' : 'Pending Verification'}
                </p>
                {profile?.verified_at && (
                  <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-1">
                    Verified on {new Date(profile.verified_at).toLocaleDateString('en', { 
                      month: 'short', 
                      day: 'numeric', 
                      year: 'numeric' 
                    })}
                  </p>
                )}
              </div>

              {/* Account Status */}
              <div className={`rounded-xl p-4 border ${
                doctor.is_active !== false
                  ? 'bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 border-blue-200 dark:border-blue-800'
                  : 'bg-gradient-to-br from-red-50 to-rose-50 dark:from-red-900/20 dark:to-rose-900/20 border-red-200 dark:border-red-800'
              }`}>
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-semibold text-neutral-900 dark:text-white text-sm mb-1">
                      Account Status
                    </h3>
                    <p className={`text-sm font-medium ${
                      doctor.is_active !== false 
                        ? 'text-blue-700 dark:text-blue-400' 
                        : 'text-red-700 dark:text-red-400'
                    }`}>
                      {doctor.is_active !== false ? 'Active' : 'Inactive'}
                    </p>
                  </div>
                  {doctor.is_active !== false ? (
                    <CheckCircle className="w-8 h-8 text-blue-600" />
                  ) : (
                    <XCircle className="w-8 h-8 text-red-600" />
                  )}
                </div>
                <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-2">
                  Member since {new Date(doctor.created_at).toLocaleDateString('en', { 
                    month: 'short', 
                    year: 'numeric' 
                  })}
                </p>
              </div>
            </div>

            {/* Right Column - Detailed Information */}
            <div className="lg:col-span-2 space-y-6">
              {/* Contact Information */}
              <div className="bg-white dark:bg-neutral-700/50 rounded-xl p-5 border border-neutral-200 dark:border-neutral-700">
                <h3 className="text-lg font-semibold text-neutral-900 dark:text-white mb-4 flex items-center gap-2">
                  <Mail className="w-5 h-5 text-primary-500" />
                  Contact Information
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="flex items-center gap-3 p-3 bg-neutral-50 dark:bg-neutral-800 rounded-lg">
                    <Mail className="w-5 h-5 text-neutral-400" />
                    <div>
                      <p className="text-xs text-neutral-500 dark:text-neutral-400">Email</p>
                      <p className="text-sm font-medium text-neutral-900 dark:text-white">{doctor.email}</p>
                    </div>
                  </div>
                  {doctor.phone && (
                    <div className="flex items-center gap-3 p-3 bg-neutral-50 dark:bg-neutral-800 rounded-lg">
                      <Phone className="w-5 h-5 text-neutral-400" />
                      <div>
                        <p className="text-xs text-neutral-500 dark:text-neutral-400">Phone</p>
                        <p className="text-sm font-medium text-neutral-900 dark:text-white">{doctor.phone}</p>
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* Professional Details */}
              {profile && (
                <div className="bg-white dark:bg-neutral-700/50 rounded-xl p-5 border border-neutral-200 dark:border-neutral-700">
                  <h3 className="text-lg font-semibold text-neutral-900 dark:text-white mb-4 flex items-center gap-2">
                    <Award className="w-5 h-5 text-primary-500" />
                    Professional Details
                  </h3>
                  <div className="grid grid-cols-2 gap-4">
                    {profile.license_number && (
                      <div className="p-3 bg-neutral-50 dark:bg-neutral-800 rounded-lg">
                        <p className="text-xs text-neutral-500 dark:text-neutral-400 mb-1">License Number</p>
                        <p className="text-sm font-medium text-neutral-900 dark:text-white">{profile.license_number}</p>
                      </div>
                    )}
                    {profile.years_of_experience && (
                      <div className="p-3 bg-neutral-50 dark:bg-neutral-800 rounded-lg">
                        <p className="text-xs text-neutral-500 dark:text-neutral-400 mb-1">Experience</p>
                        <p className="text-sm font-medium text-neutral-900 dark:text-white">{profile.years_of_experience} years</p>
                      </div>
                    )}
                    {profile.total_consultations !== undefined && (
                      <div className="p-3 bg-neutral-50 dark:bg-neutral-800 rounded-lg">
                        <p className="text-xs text-neutral-500 dark:text-neutral-400 mb-1">Total Consultations</p>
                        <p className="text-sm font-medium text-neutral-900 dark:text-white">{profile.total_consultations}</p>
                      </div>
                    )}
                    {profile.accepts_insurance !== undefined && (
                      <div className="p-3 bg-neutral-50 dark:bg-neutral-800 rounded-lg">
                        <p className="text-xs text-neutral-500 dark:text-neutral-400 mb-1">Insurance</p>
                        <p className="text-sm font-medium text-neutral-900 dark:text-white">
                          {profile.accepts_insurance ? 'Accepted' : 'Not Accepted'}
                        </p>
                      </div>
                    )}
                  </div>

                  {/* Qualifications */}
                  {profile.qualifications && profile.qualifications.length > 0 && (
                    <div className="mt-4">
                      <p className="text-xs text-neutral-500 dark:text-neutral-400 mb-2">Qualifications</p>
                      <div className="flex flex-wrap gap-2">
                        {profile.qualifications.map((qual, idx) => (
                          <span key={idx} className="px-3 py-1 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400 rounded-full text-sm font-medium">
                            {qual}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Languages */}
                  {profile.languages_spoken && profile.languages_spoken.length > 0 && (
                    <div className="mt-4">
                      <p className="text-xs text-neutral-500 dark:text-neutral-400 mb-2">Languages Spoken</p>
                      <div className="flex flex-wrap gap-2">
                        {profile.languages_spoken.map((lang, idx) => (
                          <span key={idx} className="px-3 py-1 bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 rounded-full text-sm">
                            {lang}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Bio */}
              {profile?.bio && (
                <div className="bg-white dark:bg-neutral-700/50 rounded-xl p-5 border border-neutral-200 dark:border-neutral-700">
                  <h3 className="text-lg font-semibold text-neutral-900 dark:text-white mb-3">About Doctor</h3>
                  <p className="text-sm text-neutral-600 dark:text-neutral-300 leading-relaxed">
                    {profile.bio}
                  </p>
                </div>
              )}

              {/* Clinic Details */}
              {(profile?.clinic_address || profile?.clinic_name) && (
                <div className="bg-white dark:bg-neutral-700/50 rounded-xl p-5 border border-neutral-200 dark:border-neutral-700">
                  <h3 className="text-lg font-semibold text-neutral-900 dark:text-white mb-4 flex items-center gap-2">
                    <MapPin className="w-5 h-5 text-primary-500" />
                    Clinic Information
                  </h3>
                  <div className="space-y-3">
                    {profile.clinic_name && (
                      <div className="p-3 bg-neutral-50 dark:bg-neutral-800 rounded-lg">
                        <p className="text-xs text-neutral-500 dark:text-neutral-400 mb-1">Clinic Name</p>
                        <p className="text-sm font-medium text-neutral-900 dark:text-white">{profile.clinic_name}</p>
                      </div>
                    )}
                    {profile.clinic_address && (
                      <div className="p-3 bg-neutral-50 dark:bg-neutral-800 rounded-lg">
                        <p className="text-xs text-neutral-500 dark:text-neutral-400 mb-1">Address</p>
                        <p className="text-sm text-neutral-600 dark:text-neutral-300">{profile.clinic_address}</p>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Available Days */}
              {profile?.availability && profile.availability.length > 0 && (
                <div className="bg-white dark:bg-neutral-700/50 rounded-xl p-5 border border-neutral-200 dark:border-neutral-700">
                  <h3 className="text-lg font-semibold text-neutral-900 dark:text-white mb-4 flex items-center gap-2">
                    <Clock className="w-5 h-5 text-primary-500" />
                    Availability Schedule
                  </h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                    {profile.availability.map((slot) => (
                      <div
                        key={slot.day}
                        className={`p-3 rounded-lg text-center border ${
                          slot.is_available
                            ? 'bg-primary-50 dark:bg-primary-900/20 border-primary-200 dark:border-primary-800'
                            : 'bg-neutral-50 dark:bg-neutral-800 border-neutral-200 dark:border-neutral-700 opacity-50'
                        }`}
                      >
                        <p className={`text-sm font-medium capitalize ${
                          slot.is_available 
                            ? 'text-primary-700 dark:text-primary-400' 
                            : 'text-neutral-500 dark:text-neutral-400'
                        }`}>
                          {slot.day}
                        </p>
                        {slot.is_available && slot.time_slots && slot.time_slots.length > 0 && (
                          <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-1">
                            {slot.time_slots[0].start_time} - {slot.time_slots[slot.time_slots.length - 1].end_time}
                          </p>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="sticky bottom-0 bg-neutral-50 dark:bg-neutral-900 border-t border-neutral-200 dark:border-neutral-700 p-4 rounded-b-2xl flex justify-end gap-3">
          <button
            onClick={onClose}
            className="px-6 py-2.5 bg-neutral-200 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 rounded-xl font-medium hover:bg-neutral-300 dark:hover:bg-neutral-600 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

const UserRow = ({ user, onViewDetails }) => {
  const config = roleConfig[user.role] || roleConfig.patient;
  const RoleIcon = config.icon;

  return (
    <div className="flex items-center gap-4 p-4 hover:bg-neutral-50 dark:hover:bg-neutral-700/40 rounded-xl transition-colors">
      <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center text-white font-bold flex-shrink-0">
        {(user.first_name || 'U')[0].toUpperCase()}
      </div>
      <div className="flex-grow min-w-0">
        <div className="flex items-center gap-2 flex-wrap">
          <p className="font-semibold text-sm text-neutral-900 dark:text-white">
            {user.first_name} {user.last_name}
          </p>
          <span className={`text-xs font-medium px-2 py-0.5 rounded-full flex items-center gap-1 ${config.color}`}>
            <RoleIcon className="w-3 h-3" />
            {user.role}
          </span>
          {user.role === 'doctor' && user.specialization && (
            <span className="text-xs bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-400 px-2 py-0.5 rounded-full font-medium">
              {user.specialization}
            </span>
          )}
          {user.role === 'doctor' && user.doctorProfile?.years_of_experience && (
            <span className="text-xs bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-400 px-2 py-0.5 rounded-full font-medium">
              {user.doctorProfile.years_of_experience}y exp.
            </span>
          )}
        </div>
        <p className="text-xs text-neutral-400 truncate">{user.email}</p>
        {user.phone && <p className="text-xs text-neutral-400">{user.phone}</p>}
      </div>
      <div className="flex items-center gap-3 flex-shrink-0">
        <div className="text-right hidden sm:block">
          <p className="text-xs text-neutral-400">
            Joined {new Date(user.created_at).toLocaleDateString('en', { month: 'short', day: 'numeric', year: 'numeric' })}
          </p>
        </div>
        <div className="flex items-center gap-2">
          {user.role === 'doctor' && (
            <button
              onClick={() => onViewDetails(user)}
              className="p-2 rounded-lg bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400 hover:bg-primary-100 dark:hover:bg-primary-900/30 transition-colors"
              title="View Doctor Details"
            >
              <Eye className="w-4 h-4" />
            </button>
          )}
          {user.role === 'patient' && (
            <button
              onClick={() => onViewDetails(user)}
              className="p-2 rounded-lg bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 hover:bg-blue-100 dark:hover:bg-blue-900/30 transition-colors"
              title="View Patient Details"
            >
              <Eye className="w-4 h-4" />
            </button>
          )}
          {user.is_active !== false ? (
            <span className="flex items-center gap-1 text-xs text-emerald-600 bg-emerald-50 dark:bg-emerald-900/20 dark:text-emerald-400 px-2 py-0.5 rounded-full">
              <CheckCircle className="w-3 h-3" /> Active
            </span>
          ) : (
            <span className="flex items-center gap-1 text-xs text-red-600 bg-red-50 dark:bg-red-900/20 dark:text-red-400 px-2 py-0.5 rounded-full">
              <XCircle className="w-3 h-3" /> Inactive
            </span>
          )}
        </div>
      </div>
    </div>
  );
};

const UserManagement = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [roleFilter, setRoleFilter] = useState('all');
  const [departmentFilter, setDepartmentFilter] = useState('all');
  const [selectedDoctor, setSelectedDoctor] = useState(null);
  const [selectedPatient, setSelectedPatient] = useState(null);

  const loadUsers = async () => {
    setLoading(true);
    try {
      const data = await apiService.get('/admin/users');
      
      // For doctors, fetch their profiles to get specialization and full details
      const usersWithProfiles = await Promise.all(
        (data || []).map(async (user) => {
          if (user.role === 'doctor') {
            try {
              // Fetch specific doctor profile using their user_id (note: user.id, not user._id)
              const doctorProfile = await apiService.get(`/doctors/${user.id}`);
              if (doctorProfile) {
                return { 
                  ...user, 
                  specialization: doctorProfile.specialization,
                  doctorProfile: doctorProfile
                };
              }
            } catch (err) {
              console.error('Error fetching doctor profile for user', user.id, ':', err);
            }
          }
          return user;
        })
      );
      
      setUsers(usersWithProfiles);
    } catch (err) {
      console.error('Error loading users:', err);
      setUsers([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadUsers(); }, []);

  const handleViewDetails = (user) => {
    if (user.role === 'doctor') {
      setSelectedDoctor(user);
    } else if (user.role === 'patient') {
      setSelectedPatient(user);
    }
  };

  // Get unique departments (specializations)
  const departments = ['all', ...new Set(
    users
      .filter(u => u.role === 'doctor' && u.specialization)
      .map(u => u.specialization)
  )];

  const filtered = users.filter(u => {
    const matchesRole = roleFilter === 'all' || u.role === roleFilter;
    const matchesDepartment = departmentFilter === 'all' || u.specialization === departmentFilter;
    const matchesSearch = !search ||
      `${u.first_name} ${u.last_name}`.toLowerCase().includes(search.toLowerCase()) ||
      u.email.toLowerCase().includes(search.toLowerCase()) ||
      (u.specialization && u.specialization.toLowerCase().includes(search.toLowerCase()));
    return matchesRole && matchesDepartment && matchesSearch;
  });

  const counts = {
    all: users.length,
    patient: users.filter(u => u.role === 'patient').length,
    doctor: users.filter(u => u.role === 'doctor').length,
    admin: users.filter(u => u.role === 'admin').length,
  };

  // Group doctors by department
  const doctorsByDepartment = {};
  filtered.filter(u => u.role === 'doctor').forEach(doctor => {
    const dept = doctor.specialization || 'General';
    if (!doctorsByDepartment[dept]) {
      doctorsByDepartment[dept] = [];
    }
    doctorsByDepartment[dept].push(doctor);
  });

  return (
    <>
      <div className="space-y-6 animate-fade-in">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-neutral-900 dark:text-white">User Management</h1>
            <p className="text-neutral-500 dark:text-neutral-400 mt-1">View and manage all platform users</p>
          </div>
          <button
            onClick={loadUsers}
            className="p-2 rounded-xl border border-neutral-200 dark:border-neutral-700 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
          >
            <RefreshCw className={`w-4 h-4 text-neutral-500 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>

        {/* Search & Filter */}
        <div className="bg-white dark:bg-neutral-800 rounded-2xl p-5 border border-neutral-200 dark:border-neutral-700 shadow-sm space-y-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-neutral-400" />
            <input
              type="text"
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="Search by name, email, or specialization..."
              className="w-full pl-10 pr-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white"
            />
          </div>
          
          {/* Role Filter */}
          <div className="flex gap-2 flex-wrap">
            {[
              { key: 'all', label: 'All Users' },
              { key: 'patient', label: 'Patients' },
              { key: 'doctor', label: 'Doctors' },
              { key: 'admin', label: 'Admins' },
            ].map(tab => (
              <button
                key={tab.key}
                onClick={() => { setRoleFilter(tab.key); setDepartmentFilter('all'); }}
                className={`flex items-center gap-1.5 px-4 py-2 rounded-xl text-sm font-medium transition-colors ${
                  roleFilter === tab.key
                    ? 'bg-primary-500 text-white'
                    : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'
                }`}
              >
                {tab.label}
                <span className={`text-xs px-1.5 py-0.5 rounded-full ${
                  roleFilter === tab.key ? 'bg-white/20 text-white' : 'bg-neutral-200 dark:bg-neutral-600 text-neutral-600 dark:text-neutral-300'
                }`}>
                  {counts[tab.key]}
                </span>
              </button>
            ))}
          </div>

          {/* Department Filter (only show for doctors) */}
          {roleFilter === 'doctor' && departments.length > 1 && (
            <div>
              <p className="text-xs font-semibold text-neutral-500 dark:text-neutral-400 uppercase tracking-wider mb-2">
                Filter by Department
              </p>
              <div className="flex gap-2 flex-wrap">
                {departments.map(dept => (
                  <button
                    key={dept}
                    onClick={() => setDepartmentFilter(dept)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                      departmentFilter === dept
                        ? 'bg-emerald-500 text-white'
                        : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'
                    }`}
                  >
                    {dept === 'all' ? 'All Departments' : dept}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* User List or Grouped by Department */}
        {roleFilter === 'doctor' && departmentFilter === 'all' && !search ? (
          /* Show doctors grouped by department */
          <div className="space-y-4">
            {Object.entries(doctorsByDepartment).map(([department, doctors]) => (
              <div key={department} className="bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 shadow-sm overflow-hidden">
                <div className="bg-gradient-to-r from-emerald-50 to-teal-50 dark:from-emerald-900/20 dark:to-teal-900/20 px-5 py-3 border-b border-neutral-200 dark:border-neutral-700">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-bold text-neutral-900 dark:text-white flex items-center gap-2">
                      <Stethoscope className="w-5 h-5 text-emerald-600" />
                      {department}
                    </h3>
                    <span className="text-sm font-medium text-emerald-600 dark:text-emerald-400">
                      {doctors.length} doctor{doctors.length !== 1 ? 's' : ''}
                    </span>
                  </div>
                </div>
                <div className="p-4 divide-y divide-neutral-100 dark:divide-neutral-700">
                  {doctors.map(user => (
                    <div key={user.id} className="py-1">
                      <UserRow user={user} onViewDetails={handleViewDetails} />
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        ) : (
          /* Show regular flat list */
          <div className="bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 shadow-sm overflow-hidden">
            <div className="p-4 border-b border-neutral-100 dark:border-neutral-700">
              <p className="text-sm text-neutral-500 dark:text-neutral-400">
                Showing <strong className="text-neutral-900 dark:text-white">{filtered.length}</strong> of {users.length} users
              </p>
            </div>

            {loading ? (
              <div className="p-4 space-y-3">
                {[1, 2, 3, 4, 5].map(i => (
                  <div key={i} className="h-14 bg-neutral-100 dark:bg-neutral-700 rounded-xl animate-pulse" />
                ))}
              </div>
            ) : filtered.length > 0 ? (
              <div className="p-4 divide-y divide-neutral-100 dark:divide-neutral-700">
                {filtered.map(user => (
                  <div key={user.id} className="py-1">
                    <UserRow user={user} onViewDetails={handleViewDetails} />
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-16">
                <Users className="w-12 h-12 text-neutral-300 mx-auto mb-3" />
                <p className="text-neutral-500 font-medium">No users found</p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Doctor Details Modal */}
      {selectedDoctor && (
        <DoctorDetailsModal 
          doctor={selectedDoctor} 
          onClose={() => setSelectedDoctor(null)} 
        />
      )}

      {/* Patient Details Modal */}
      {selectedPatient && (
        <PatientDetailsModal 
          patient={selectedPatient} 
          onClose={() => setSelectedPatient(null)} 
        />
      )}
    </>
  );
};

export default UserManagement;
