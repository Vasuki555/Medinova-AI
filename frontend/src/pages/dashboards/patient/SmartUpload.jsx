/**
 * Smart Document Upload Page
 * Automatically extract and process medical documents
 */

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiService } from '@/services/api';
import {
  Upload, FileText, Pill, Activity, CheckCircle,
  XCircle, Loader2, AlertTriangle, Edit2, Save,
  Sparkles, FileImage, ChevronDown, ChevronUp
} from 'lucide-react';

const DocumentTypeSelector = ({ selected, onChange }) => {
  const types = [
    { id: 'prescription', label: 'Prescription', icon: Pill, desc: 'Extract medicines automatically' },
    { id: 'lab_report', label: 'Lab Report', icon: Activity, desc: 'Extract test results' },
  ];

  return (
    <div className="grid grid-cols-2 gap-3 mb-6">
      {types.map(type => {
        const Icon = type.icon;
        return (
          <button
            key={type.id}
            onClick={() => onChange(type.id)}
            className={`p-4 rounded-2xl border-2 transition-all text-left ${
              selected === type.id
                ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                : 'border-neutral-200 dark:border-neutral-700 hover:border-primary-300'
            }`}
          >
            <Icon className={`w-6 h-6 mb-2 ${selected === type.id ? 'text-primary-500' : 'text-neutral-400'}`} />
            <h3 className="font-bold text-neutral-900 dark:text-white text-sm">{type.label}</h3>
            <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-1">{type.desc}</p>
          </button>
        );
      })}
    </div>
  );
};

const MedicineEditCard = ({ medicine, onChange, onRemove }) => {
  const [expanded, setExpanded] = useState(true);

  return (
    <div className="bg-white dark:bg-neutral-800 rounded-xl border border-neutral-200 dark:border-neutral-700 overflow-hidden">
      <div
        className="p-4 cursor-pointer flex items-center justify-between"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="flex items-center gap-3">
          <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
            medicine.confidence === 'high' ? 'bg-emerald-100 dark:bg-emerald-900/30' :
            medicine.confidence === 'medium' ? 'bg-amber-100 dark:bg-amber-900/30' :
            'bg-red-100 dark:bg-red-900/30'
          }`}>
            <Pill className={`w-5 h-5 ${
              medicine.confidence === 'high' ? 'text-emerald-600' :
              medicine.confidence === 'medium' ? 'text-amber-600' :
              'text-red-600'
            }`} />
          </div>
          <div>
            <h4 className="font-bold text-neutral-900 dark:text-white">{medicine.medicine_name}</h4>
            <p className="text-xs text-neutral-500 dark:text-neutral-400">
              {medicine.dosage} · {medicine.frequency}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className={`text-xs px-2 py-1 rounded-full ${
            medicine.confidence === 'high' ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-900/20 dark:text-emerald-400' :
            medicine.confidence === 'medium' ? 'bg-amber-50 text-amber-700 dark:bg-amber-900/20 dark:text-amber-400' :
            'bg-red-50 text-red-700 dark:bg-red-900/20 dark:text-red-400'
          }`}>
            {medicine.confidence} confidence
          </span>
          {expanded ? <ChevronUp className="w-4 h-4 text-neutral-400" /> : <ChevronDown className="w-4 h-4 text-neutral-400" />}
        </div>
      </div>

      {expanded && (
        <div className="border-t border-neutral-100 dark:border-neutral-700 p-4 space-y-3">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs font-medium text-neutral-600 dark:text-neutral-400 block mb-1">
                Medicine Name *
              </label>
              <input
                type="text"
                value={medicine.medicine_name}
                onChange={e => onChange({ ...medicine, medicine_name: e.target.value })}
                className="w-full px-3 py-2 text-sm border border-neutral-200 dark:border-neutral-700 rounded-lg bg-white dark:bg-neutral-900 text-neutral-900 dark:text-white"
              />
            </div>
            <div>
              <label className="text-xs font-medium text-neutral-600 dark:text-neutral-400 block mb-1">
                Dosage *
              </label>
              <input
                type="text"
                value={medicine.dosage}
                onChange={e => onChange({ ...medicine, dosage: e.target.value })}
                placeholder="e.g., 500mg, 5ml"
                className="w-full px-3 py-2 text-sm border border-neutral-200 dark:border-neutral-700 rounded-lg bg-white dark:bg-neutral-900 text-neutral-900 dark:text-white"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs font-medium text-neutral-600 dark:text-neutral-400 block mb-1">
                Frequency *
              </label>
              <input
                type="text"
                value={medicine.frequency}
                onChange={e => onChange({ ...medicine, frequency: e.target.value })}
                placeholder="e.g., twice daily"
                className="w-full px-3 py-2 text-sm border border-neutral-200 dark:border-neutral-700 rounded-lg bg-white dark:bg-neutral-900 text-neutral-900 dark:text-white"
              />
            </div>
            <div>
              <label className="text-xs font-medium text-neutral-600 dark:text-neutral-400 block mb-1">
                Duration (days)
              </label>
              <input
                type="number"
                value={medicine.duration_days || ''}
                onChange={e => onChange({ ...medicine, duration_days: e.target.value ? parseInt(e.target.value) : null })}
                placeholder="e.g., 7"
                className="w-full px-3 py-2 text-sm border border-neutral-200 dark:border-neutral-700 rounded-lg bg-white dark:bg-neutral-900 text-neutral-900 dark:text-white"
              />
            </div>
          </div>

          <div>
            <label className="text-xs font-medium text-neutral-600 dark:text-neutral-400 block mb-1">
              Instructions
            </label>
            <textarea
              value={medicine.instructions}
              onChange={e => onChange({ ...medicine, instructions: e.target.value })}
              rows={2}
              className="w-full px-3 py-2 text-sm border border-neutral-200 dark:border-neutral-700 rounded-lg bg-white dark:bg-neutral-900 text-neutral-900 dark:text-white resize-none"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs font-medium text-neutral-600 dark:text-neutral-400 block mb-1">
                Meal Timing
              </label>
              <select
                value={medicine.meal_timing}
                onChange={e => onChange({ ...medicine, meal_timing: e.target.value })}
                className="w-full px-3 py-2 text-sm border border-neutral-200 dark:border-neutral-700 rounded-lg bg-white dark:bg-neutral-900 text-neutral-900 dark:text-white"
              >
                <option value="anytime">Anytime</option>
                <option value="before_meal">Before Meal</option>
                <option value="after_meal">After Meal</option>
                <option value="with_meal">With Meal</option>
              </select>
            </div>
            <div>
              <label className="text-xs font-medium text-neutral-600 dark:text-neutral-400 block mb-1">
                Current Stock
              </label>
              <input
                type="number"
                value={medicine.current_quantity || ''}
                onChange={e => onChange({ ...medicine, current_quantity: e.target.value ? parseInt(e.target.value) : null })}
                placeholder="e.g., 30"
                className="w-full px-3 py-2 text-sm border border-neutral-200 dark:border-neutral-700 rounded-lg bg-white dark:bg-neutral-900 text-neutral-900 dark:text-white"
              />
            </div>
          </div>

          <button
            onClick={onRemove}
            className="text-xs text-red-500 hover:text-red-600 flex items-center gap-1"
          >
            <XCircle className="w-3 h-3" />
            Remove this medicine
          </button>
        </div>
      )}
    </div>
  );
};

const SmartUpload = () => {
  const navigate = useNavigate();
  const [docType, setDocType] = useState('prescription');
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  
  // Extracted data editing
  const [medicines, setMedicines] = useState([]);
  const [saving, setSaving] = useState(false);

  const handleSaveLabReport = async () => {
    if (!result?.record_info) return;

    setSaving(true);
    try {
      const info = result.record_info;
      
      // Convert key_findings array to LabResultItem format
      const labResults = (info.key_findings || []).map(finding => {
        // Handle different finding formats
        if (typeof finding === 'string') {
          // Parse string like "Hemoglobin: 14.5 g/dL (Normal)"
          const match = finding.match(/^(.+?):\s*([0-9.]+)\s*(.+?)(?:\s*\((.+)\))?$/);
          if (match) {
            const [_, parameter, value, unit, range] = match;
            return {
              parameter: parameter.trim(),
              value: parseFloat(value),
              unit: unit.trim(),
              reference_range: range || null,
              is_abnormal: false
            };
          }
          // Fallback for unparseable strings
          return {
            parameter: finding,
            value: 0,
            unit: "",
            reference_range: null,
            is_abnormal: false
          };
        } else if (typeof finding === 'object') {
          // Already in object format
          return {
            parameter: finding.parameter || finding.name || "Unknown",
            value: parseFloat(finding.value) || 0,
            unit: finding.unit || "",
            reference_range: finding.reference_range || finding.range || null,
            is_abnormal: finding.is_abnormal || false
          };
        }
        return null;
      }).filter(Boolean);

      // Build the correct schema structure
      const recordData = {
        record_type: "lab_test",
        recorded_at: info.test_date || new Date().toISOString(),
        lab_test: {
          test_name: info.report_name || info.test_name || "Medical Report",
          lab_name: info.lab_name || info.hospital || null,
          ordered_by: null,
          results: labResults,
          report_document_id: null
        },
        source: "smart_upload"
      };

      // Add diagnosis if present
      if (info.diagnosis) {
        recordData.diagnosis = {
          condition: info.diagnosis,
          icd10_code: null,
          diagnosed_by: null,
          severity: "moderate",
          notes: info.summary || null
        };
      }

      // Add notes if summary exists and no diagnosis
      if (info.summary && !info.diagnosis) {
        recordData.note = {
          title: info.report_name || "Medical Report",
          content: info.summary,
          category: "general"
        };
      }

      console.log('Sending health record:', recordData);
      const response = await apiService.post('/health-records', recordData);
      console.log('Health record created:', response);

      // Update result to mark as saved
      setResult(prev => ({
        ...prev,
        saved_record_id: response.id
      }));

      alert('Lab report saved to Health Records successfully!');
      
      // Navigate to health records page to view the saved record
      navigate('/patient/phr');
      
      // Reset
      setFile(null);
      setResult(null);
    } catch (err) {
      console.error('Save error:', err);
      console.error('Error response:', err.response?.data);
      alert('Failed to save lab report: ' + (err.response?.data?.detail || err.message));
    } finally {
      setSaving(false);
    }
  };

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files?.[0];
    if (!selectedFile) return;

    // Validate file type
    const validTypes = ['image/jpeg', 'image/png', 'image/webp', 'application/pdf'];
    if (!validTypes.includes(selectedFile.type)) {
      setError('Invalid file type. Please upload JPEG, PNG, WEBP, or PDF');
      return;
    }

    // Validate size (50MB)
    if (selectedFile.size > 50 * 1024 * 1024) {
      setError('File too large. Maximum size is 50MB');
      return;
    }

    setFile(selectedFile);
    setError(null);
    setResult(null);
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    setUploadProgress(0);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('auto_save', 'true'); // Auto-save without manual confirmation

      let endpoint = '';
      if (docType === 'prescription') {
        endpoint = '/documents/upload-prescription';
      } else {
        endpoint = '/documents/upload-medical-record';
      }

      const response = await apiService.upload(endpoint, formData, setUploadProgress);

      if (!response.success) {
        setError(response.error || 'Upload failed');
        return;
      }

      setResult(response);

      // Show success message if auto-saved
      if (response.auto_saved && response.saved_record_id) {
        alert('Medical record extracted and saved successfully!');
      }

      // Set medicines for editing if prescription
      if (docType === 'prescription' && response.medicine_info?.medicines) {
        setMedicines(response.medicine_info.medicines);
      }

    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const handleSaveMedicines = async () => {
    if (medicines.length === 0) return;

    setSaving(true);
    try {
      let successCount = 0;
      let errorCount = 0;

      for (const med of medicines) {
        if (!med.medicine_name || !med.dosage) continue;

        // Calculate schedule_times from time_of_day
        const timeMapping = {
          morning: '08:00',
          afternoon: '14:00',
          evening: '18:00',
          night: '22:00'
        };
        
        const schedule_times = med.time_of_day?.map(t => timeMapping[t]).filter(Boolean) || ['09:00'];

        // Build proper schedule object as per backend schema
        const schedule = {
          frequency: "daily",
          times_per_day: schedule_times.length,
          time_slots: schedule_times.map(time => ({
            time: time,
            with_meal: med.meal_timing || "anytime"
          })),
          days_of_week: [0, 1, 2, 3, 4, 5, 6], // All days
          start_date: new Date().toISOString(),
          is_ongoing: !med.duration_days,
          end_date: med.duration_days ? new Date(Date.now() + med.duration_days * 24 * 60 * 60 * 1000).toISOString() : null
        };

        try {
          console.log('Saving medicine:', med.medicine_name, { dosage: med.dosage, schedule });
          
          await apiService.post('/medications', {
            medicine_name: med.medicine_name,
            dosage: med.dosage,
            schedule: schedule,
            instructions: med.instructions,
            current_quantity: med.current_quantity,
            refill_reminder_at: med.current_quantity ? 5 : null
          });
          successCount++;
          console.log('✓ Saved:', med.medicine_name);
        } catch (err) {
          console.error('✗ Failed to save medicine:', med.medicine_name);
          console.error('Error details:', {
            status: err.response?.status,
            statusText: err.response?.statusText,
            data: err.response?.data,
            message: err.message
          });
          errorCount++;
        }
      }

      if (successCount > 0) {
        alert(`Successfully saved ${successCount} medicine(s)!`);
        // Reset
        setFile(null);
        setResult(null);
        setMedicines([]);
      }

      if (errorCount > 0) {
        alert(`${errorCount} medicine(s) could not be saved. Please check for duplicates.`);
      }

    } catch (err) {
      alert('Failed to save medicines: ' + (err.message || 'Unknown error'));
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto animate-fade-in">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-violet-500 to-primary-500 flex items-center justify-center shadow-lg">
          <Sparkles className="w-6 h-6 text-white" />
        </div>
        <div>
          <h1 className="text-2xl font-black text-neutral-900 dark:text-white">Smart Document Upload</h1>
          <p className="text-sm text-neutral-500 dark:text-neutral-400">
            Automatically extract medicines and medical data from documents
          </p>
        </div>
      </div>

      {/* Document Type Selector */}
      <DocumentTypeSelector selected={docType} onChange={setDocType} />

      {/* Upload Area */}
      {!result && (
        <div className="bg-white dark:bg-neutral-800 rounded-2xl border-2 border-dashed border-neutral-300 dark:border-neutral-600 p-8">
          <div className="text-center">
            <div className="w-16 h-16 bg-primary-50 dark:bg-primary-900/30 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <Upload className="w-8 h-8 text-primary-500" />
            </div>

            <h3 className="text-lg font-bold text-neutral-900 dark:text-white mb-2">
              Upload {docType === 'prescription' ? 'Prescription' : 'Medical Report'}
            </h3>
            <p className="text-sm text-neutral-500 dark:text-neutral-400 mb-4">
              Drag and drop or click to browse · JPEG, PNG, PDF · Max 50MB
            </p>

            <input
              type="file"
              accept="image/jpeg,image/png,image/webp,application/pdf"
              onChange={handleFileSelect}
              className="hidden"
              id="file-upload"
            />

            <label
              htmlFor="file-upload"
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-primary-500 hover:bg-primary-600 text-white font-medium rounded-xl cursor-pointer transition-colors"
            >
              <FileImage className="w-4 h-4" />
              Select File
            </label>

            {file && (
              <div className="mt-4 p-4 bg-primary-50 dark:bg-primary-900/20 rounded-xl border border-primary-200 dark:border-primary-800">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <FileText className="w-5 h-5 text-primary-500" />
                    <div className="text-left">
                      <p className="text-sm font-medium text-neutral-900 dark:text-white">{file.name}</p>
                      <p className="text-xs text-neutral-500 dark:text-neutral-400">
                        {(file.size / 1024 / 1024).toFixed(2)} MB
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={handleUpload}
                    disabled={uploading}
                    className="px-4 py-2 bg-primary-500 hover:bg-primary-600 text-white text-sm font-medium rounded-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                  >
                    {uploading ? (
                      <>
                        <Loader2 className="w-4 h-4 animate-spin" />
                        Processing... {uploadProgress}%
                      </>
                    ) : (
                      <>
                        <Sparkles className="w-4 h-4" />
                        Extract Info
                      </>
                    )}
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="mt-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
          <div>
            <h4 className="font-bold text-red-900 dark:text-red-300">Upload Failed</h4>
            <p className="text-sm text-red-700 dark:text-red-400 mt-1">{error}</p>
          </div>
        </div>
      )}

      {/* Results - Medicines */}
      {result && docType === 'prescription' && medicines.length > 0 && (
        <div className="bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 p-6 mt-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-lg font-bold text-neutral-900 dark:text-white flex items-center gap-2">
                <CheckCircle className="w-5 h-5 text-emerald-500" />
                Extracted Medicines ({medicines.length})
              </h3>
              <p className="text-sm text-neutral-500 dark:text-neutral-400 mt-1">
                Review and edit the information below before saving
              </p>
            </div>
            <button
              onClick={handleSaveMedicines}
              disabled={saving}
              className="px-4 py-2 bg-emerald-500 hover:bg-emerald-600 text-white font-medium rounded-xl flex items-center gap-2 disabled:opacity-50"
            >
              {saving ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Saving...
                </>
              ) : (
                <>
                  <Save className="w-4 h-4" />
                  Save All
                </>
              )}
            </button>
          </div>

          <div className="space-y-3">
            {medicines.map((med, idx) => (
              <MedicineEditCard
                key={idx}
                medicine={med}
                onChange={updated => {
                  const newMeds = [...medicines];
                  newMeds[idx] = updated;
                  setMedicines(newMeds);
                }}
                onRemove={() => {
                  setMedicines(medicines.filter((_, i) => i !== idx));
                }}
              />
            ))}
          </div>

          {result.medicine_info?.prescriber_name && (
            <div className="mt-4 p-3 bg-neutral-50 dark:bg-neutral-900 rounded-lg text-sm text-neutral-600 dark:text-neutral-400">
              <strong>Prescribed by:</strong> {result.medicine_info.prescriber_name}
              {result.medicine_info.prescription_date && (
                <> · <strong>Date:</strong> {result.medicine_info.prescription_date}</>
              )}
            </div>
          )}
        </div>
      )}

      {/* Results - Medical Record */}
      {result && docType === 'lab_report' && result.record_info && (
        <div className="bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 p-6 mt-6">
          <h3 className="text-lg font-bold text-neutral-900 dark:text-white flex items-center gap-2 mb-4">
            <CheckCircle className="w-5 h-5 text-emerald-500" />
            Medical Record Extracted
          </h3>

          <div className="space-y-4">
            <div>
              <label className="text-xs font-medium text-neutral-600 dark:text-neutral-400 block mb-1">
                Report Name
              </label>
              <p className="text-sm font-medium text-neutral-900 dark:text-white">
                {result.record_info.report_name || 'Unnamed Report'}
              </p>
            </div>

            {result.record_info.summary && (
              <div>
                <label className="text-xs font-medium text-neutral-600 dark:text-neutral-400 block mb-1">
                  Summary
                </label>
                <p className="text-sm text-neutral-700 dark:text-neutral-300">
                  {result.record_info.summary}
                </p>
              </div>
            )}

            {result.record_info.key_findings?.length > 0 && (
              <div>
                <label className="text-xs font-medium text-neutral-600 dark:text-neutral-400 block mb-2">
                  Key Findings
                </label>
                <div className="space-y-2">
                  {result.record_info.key_findings.map((finding, idx) => (
                    <div key={idx} className="p-3 bg-neutral-50 dark:bg-neutral-900 rounded-lg">
                      <div className="flex items-center justify-between">
                        <span className="font-medium text-sm text-neutral-900 dark:text-white">
                          {finding.parameter}
                        </span>
                        <span className={`text-xs px-2 py-1 rounded-full ${
                          finding.status === 'normal' ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/20 dark:text-emerald-400' :
                          finding.status === 'high' || finding.status === 'low' ? 'bg-amber-100 text-amber-700 dark:bg-amber-900/20 dark:text-amber-400' :
                          finding.status === 'critical' ? 'bg-red-100 text-red-700 dark:bg-red-900/20 dark:text-red-400' :
                          'bg-neutral-100 text-neutral-600 dark:bg-neutral-800 dark:text-neutral-400'
                        }`}>
                          {finding.status}
                        </span>
                      </div>
                      <p className="text-sm text-neutral-600 dark:text-neutral-400 mt-1">
                        {finding.value} {finding.unit}
                        {finding.normal_range && ` (Normal: ${finding.normal_range})`}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {result.saved_record_id ? (
              <div className="space-y-3">
                <div className="p-3 bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-lg flex items-center gap-2 text-sm text-emerald-700 dark:text-emerald-400">
                  <CheckCircle className="w-4 h-4" />
                  Record saved successfully to your health records
                </div>
                <button
                  onClick={() => navigate('/patient/phr')}
                  className="w-full px-4 py-3 bg-primary-500 hover:bg-primary-600 text-white rounded-xl font-medium transition-colors flex items-center justify-center gap-2"
                >
                  <FileText className="w-4 h-4" />
                  View Health Records
                </button>
              </div>
            ) : (
              <div className="space-y-3">
                <p className="text-xs text-neutral-500 dark:text-neutral-400">
                  This record was extracted but not saved. You can save it to your health records.
                </p>
                <button
                  onClick={handleSaveLabReport}
                  disabled={saving}
                  className="w-full px-4 py-3 bg-primary-500 hover:bg-primary-600 text-white rounded-xl font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  {saving ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Saving...
                    </>
                  ) : (
                    <>
                      <Save className="w-4 h-4" />
                      Save to Health Records
                    </>
                  )}
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default SmartUpload;
