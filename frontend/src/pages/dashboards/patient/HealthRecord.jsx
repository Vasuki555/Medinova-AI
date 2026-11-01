/**
 * Personal Health Record (PHR) Page
 * Patient can view and add their health records and vitals
 */

import { useState, useEffect } from 'react';
import { apiService } from '@/services/api';
import {
  HeartPulse, Plus, TrendingUp, Activity, Thermometer,
  Wind, Weight, ChevronDown, ChevronUp, X, FileText,
  FlaskConical, Stethoscope
} from 'lucide-react';
import { SVGLineChart } from '@/components/common/SVGLineChart';

const RECORD_TYPES = ['vitals', 'lab_test', 'diagnosis', 'note'];

const VitalBadge = ({ icon: Icon, label, value, unit, color }) => (
  <div className={`flex items-center gap-3 p-3 rounded-xl ${color}`}>
    <Icon className="w-5 h-5 flex-shrink-0" />
    <div>
      <p className="text-xs opacity-75">{label}</p>
      <p className="font-bold text-sm">{value || '—'} <span className="font-normal text-xs opacity-75">{unit}</span></p>
    </div>
  </div>
);

const RecordItem = ({ record }) => {
  const [expanded, setExpanded] = useState(false);
  const typeIcons = {
    vitals: HeartPulse,
    lab_test: FlaskConical,
    diagnosis: Stethoscope,
    note: FileText,
  };
  const typeColors = {
    vitals: 'text-rose-500 bg-rose-50 dark:bg-rose-900/20',
    lab_test: 'text-blue-500 bg-blue-50 dark:bg-blue-900/20',
    diagnosis: 'text-violet-500 bg-violet-50 dark:bg-violet-900/20',
    note: 'text-neutral-500 bg-neutral-50 dark:bg-neutral-700/40',
  };
  const Icon = typeIcons[record.record_type] || FileText;
  const colorClass = typeColors[record.record_type] || typeColors.note;

  return (
    <div className="bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 shadow-sm overflow-hidden">
      <div
        className="flex items-center gap-4 p-4 cursor-pointer"
        onClick={() => setExpanded(e => !e)}
      >
        <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${colorClass}`}>
          <Icon className="w-5 h-5" />
        </div>
        <div className="flex-grow">
          <p className="font-semibold text-neutral-900 dark:text-white text-sm capitalize">
            {record.record_type.replace('_', ' ')}
          </p>
          <p className="text-xs text-neutral-400">
            {new Date(record.recorded_at || record.created_at).toLocaleDateString('en', {
              year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
            })}
          </p>
        </div>
        {expanded ? <ChevronUp className="w-4 h-4 text-neutral-400" /> : <ChevronDown className="w-4 h-4 text-neutral-400" />}
      </div>

      {expanded && (
        <div className="border-t border-neutral-100 dark:border-neutral-700 p-4">
          {record.record_type === 'vitals' && record.vitals && (
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
              <VitalBadge icon={Activity} label="Heart Rate" value={record.vitals.heart_rate} unit="bpm" color="bg-rose-50 text-rose-700 dark:bg-rose-900/20 dark:text-rose-400" />
              {record.vitals.blood_pressure_systolic && (
                <VitalBadge icon={TrendingUp} label="Blood Pressure" value={`${record.vitals.blood_pressure_systolic}/${record.vitals.blood_pressure_diastolic}`} unit="mmHg" color="bg-blue-50 text-blue-700 dark:bg-blue-900/20 dark:text-blue-400" />
              )}
              {record.vitals.temperature && (
                <VitalBadge icon={Thermometer} label="Temperature" value={record.vitals.temperature} unit="°F" color="bg-orange-50 text-orange-700 dark:bg-orange-900/20 dark:text-orange-400" />
              )}
              {record.vitals.oxygen_saturation && (
                <VitalBadge icon={Wind} label="SpO₂" value={record.vitals.oxygen_saturation} unit="%" color="bg-cyan-50 text-cyan-700 dark:bg-cyan-900/20 dark:text-cyan-400" />
              )}
              {record.vitals.weight && (
                <VitalBadge icon={Weight} label="Weight" value={record.vitals.weight} unit="kg" color="bg-emerald-50 text-emerald-700 dark:bg-emerald-900/20 dark:text-emerald-400" />
              )}
            </div>
          )}
          {record.record_type === 'note' && record.note && (
            <div>
              <h4 className="font-semibold text-neutral-900 dark:text-white text-sm mb-2">{record.note.title}</h4>
              <p className="text-sm text-neutral-700 dark:text-neutral-300 whitespace-pre-wrap">{record.note.content}</p>
            </div>
          )}
          {record.record_type === 'diagnosis' && record.diagnosis && (
            <div>
              <h4 className="font-semibold text-neutral-900 dark:text-white text-sm mb-2">{record.diagnosis.condition}</h4>
              {record.diagnosis.icd10_code && <p className="text-xs text-neutral-500 mb-2">ICD-10: {record.diagnosis.icd10_code}</p>}
              {record.diagnosis.notes && <p className="text-sm text-neutral-700 dark:text-neutral-300 whitespace-pre-wrap">{record.diagnosis.notes}</p>}
              {record.diagnosis.severity && (
                <span className={`inline-block mt-2 px-2 py-1 rounded-lg text-xs font-medium ${
                  record.diagnosis.severity === 'severe' ? 'bg-red-100 text-red-700 dark:bg-red-900/20 dark:text-red-400' :
                  record.diagnosis.severity === 'moderate' ? 'bg-amber-100 text-amber-700 dark:bg-amber-900/20 dark:text-amber-400' :
                  'bg-green-100 text-green-700 dark:bg-green-900/20 dark:text-green-400'
                }`}>
                  {record.diagnosis.severity}
                </span>
              )}
            </div>
          )}
          {record.record_type === 'lab_test' && record.lab_test && (
            <div>
              <h4 className="font-semibold text-neutral-900 dark:text-white text-sm mb-3">{record.lab_test.test_name}</h4>
              {record.lab_test.lab_name && (
                <p className="text-xs text-neutral-500 mb-3">Lab: {record.lab_test.lab_name}</p>
              )}
              {record.lab_test.results && record.lab_test.results.length > 0 && (
                <div className="space-y-2">
                  {record.lab_test.results.map((result, idx) => (
                    <div key={idx} className={`flex justify-between items-center text-sm p-2 rounded-lg ${
                      result.is_abnormal ? 'bg-red-50 dark:bg-red-900/10' : 'bg-neutral-50 dark:bg-neutral-700/50'
                    }`}>
                      <span className="text-neutral-600 dark:text-neutral-300">{result.parameter}</span>
                      <div className="text-right">
                        <span className={`font-medium ${result.is_abnormal ? 'text-red-600 dark:text-red-400' : 'text-neutral-900 dark:text-white'}`}>
                          {result.value} {result.unit}
                        </span>
                        {result.reference_range && (
                          <p className="text-xs text-neutral-400">Ref: {result.reference_range}</p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
          {record.source && (
            <p className="text-xs text-neutral-400 mt-3">
              Recorded by: <span className="font-medium capitalize">{record.source}</span>
            </p>
          )}
        </div>
      )}
    </div>
  );
};

const AddRecordModal = ({ onClose, onAdded }) => {
  const [form, setForm] = useState({
    record_type: 'vitals',
    // Vitals
    heart_rate: '',
    blood_pressure: '',
    temperature: '',
    oxygen_saturation: '',
    weight: '',
    height: '',
    // Diagnosis
    condition: '',
    icd_code: '',
    severity: 'moderate',
    diagnosed_by: '',
    diagnosis_notes: '',
    // Lab Test
    test_name: '',
    result_value: '',
    result_unit: '',
    reference_range: '',
    test_status: 'normal',
    lab_name: '',
    lab_notes: '',
    // General Note
    note_title: '',
    note_category: 'general',
    note_description: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const payload = { 
        record_type: form.record_type,
        recorded_at: new Date().toISOString()
      };
      
      if (form.record_type === 'vitals') {
        const vitals = {};
        if (form.heart_rate) vitals.heart_rate = parseFloat(form.heart_rate);
        if (form.blood_pressure) {
          const parts = form.blood_pressure.split('/');
          if (parts.length === 2) {
            vitals.blood_pressure_systolic = parseFloat(parts[0]);
            vitals.blood_pressure_diastolic = parseFloat(parts[1]);
          }
        }
        if (form.temperature) vitals.temperature = parseFloat(form.temperature);
        if (form.oxygen_saturation) vitals.oxygen_saturation = parseFloat(form.oxygen_saturation);
        if (form.weight) vitals.weight = parseFloat(form.weight);
        if (form.height) vitals.height = parseFloat(form.height);
        payload.vitals = vitals;
      } else if (form.record_type === 'diagnosis') {
        payload.diagnosis = {
          condition: form.condition || 'General diagnosis',
          icd_code: form.icd_code || null,
          severity: form.severity,
          diagnosed_by: form.diagnosed_by || 'Self-reported',
          notes: form.diagnosis_notes || ''
        };
      } else if (form.record_type === 'lab_test') {
        payload.lab_test = {
          test_name: form.test_name || 'General lab test',
          result_value: form.result_value || 'N/A',
          unit: form.result_unit || '',
          reference_range: form.reference_range || '',
          status: form.test_status,
          lab_name: form.lab_name || 'Self-reported',
          notes: form.lab_notes || ''
        };
      } else if (form.record_type === 'note') {
        payload.note = {
          title: form.note_title || 'General Note',
          content: form.note_description || 'Manual health record entry',
          category: form.note_category
        };
      }
      
      await apiService.post('/health-records', payload);
      onAdded();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save record');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white dark:bg-neutral-800 rounded-2xl w-full max-w-md shadow-2xl animate-scale-in max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between p-6 border-b border-neutral-200 dark:border-neutral-700 sticky top-0 bg-white dark:bg-neutral-800">
          <h2 className="font-bold text-neutral-900 dark:text-white">Add Health Record</h2>
          <button onClick={onClose} className="p-2 hover:bg-neutral-100 dark:hover:bg-neutral-700 rounded-xl">
            <X className="w-5 h-5 text-neutral-500" />
          </button>
        </div>
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {error && <div className="p-3 bg-red-50 border border-red-200 rounded-xl text-red-600 text-sm">{error}</div>}
          
          <div>
            <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">Record Type</label>
            <select
              value={form.record_type}
              onChange={e => setForm(f => ({ ...f, record_type: e.target.value }))}
              className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white"
            >
              {RECORD_TYPES.map(t => (
                <option key={t} value={t}>{t.replace('_', ' ').replace(/^\w/, c => c.toUpperCase())}</option>
              ))}
            </select>
          </div>

          {form.record_type === 'vitals' && (
            <>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-neutral-600 dark:text-neutral-400 mb-1">Heart Rate (bpm)</label>
                  <input type="number" value={form.heart_rate} onChange={e => setForm(f => ({ ...f, heart_rate: e.target.value }))} placeholder="72" className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" />
                </div>
                <div>
                  <label className="block text-xs font-medium text-neutral-600 dark:text-neutral-400 mb-1">Blood Pressure (sys/dia)</label>
                  <input type="text" value={form.blood_pressure} onChange={e => setForm(f => ({ ...f, blood_pressure: e.target.value }))} placeholder="120/80" className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" />
                </div>
                <div>
                  <label className="block text-xs font-medium text-neutral-600 dark:text-neutral-400 mb-1">Temperature (°F)</label>
                  <input type="number" step="0.1" value={form.temperature} onChange={e => setForm(f => ({ ...f, temperature: e.target.value }))} placeholder="98.6" className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" />
                </div>
                <div>
                  <label className="block text-xs font-medium text-neutral-600 dark:text-neutral-400 mb-1">SpO₂ (%)</label>
                  <input type="number" value={form.oxygen_saturation} onChange={e => setForm(f => ({ ...f, oxygen_saturation: e.target.value }))} placeholder="98" className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" />
                </div>
                <div>
                  <label className="block text-xs font-medium text-neutral-600 dark:text-neutral-400 mb-1">Weight (kg)</label>
                  <input type="number" step="0.1" value={form.weight} onChange={e => setForm(f => ({ ...f, weight: e.target.value }))} placeholder="70" className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" />
                </div>
                <div>
                  <label className="block text-xs font-medium text-neutral-600 dark:text-neutral-400 mb-1">Height (cm)</label>
                  <input type="number" value={form.height} onChange={e => setForm(f => ({ ...f, height: e.target.value }))} placeholder="170" className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" />
                </div>
              </div>
            </>
          )}

          {form.record_type === 'diagnosis' && (
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">Condition/Disease *</label>
                <input 
                  type="text" 
                  value={form.condition} 
                  onChange={e => setForm(f => ({ ...f, condition: e.target.value }))} 
                  placeholder="e.g., Type 2 Diabetes, Hypertension"
                  required
                  className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" 
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-neutral-600 dark:text-neutral-400 mb-1">ICD-10 Code (optional)</label>
                  <input 
                    type="text" 
                    value={form.icd_code} 
                    onChange={e => setForm(f => ({ ...f, icd_code: e.target.value }))} 
                    placeholder="E11.9"
                    className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" 
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-neutral-600 dark:text-neutral-400 mb-1">Severity</label>
                  <select 
                    value={form.severity} 
                    onChange={e => setForm(f => ({ ...f, severity: e.target.value }))}
                    className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white"
                  >
                    <option value="mild">Mild</option>
                    <option value="moderate">Moderate</option>
                    <option value="severe">Severe</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">Diagnosed By</label>
                <input 
                  type="text" 
                  value={form.diagnosed_by} 
                  onChange={e => setForm(f => ({ ...f, diagnosed_by: e.target.value }))} 
                  placeholder="Dr. Smith, General Hospital"
                  className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" 
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">Additional Notes</label>
                <textarea
                  value={form.diagnosis_notes}
                  onChange={e => setForm(f => ({ ...f, diagnosis_notes: e.target.value }))}
                  placeholder="Symptoms, treatment plan, recommendations..."
                  rows={3}
                  className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white resize-none"
                />
              </div>
            </div>
          )}

          {form.record_type === 'lab_test' && (
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">Test Name *</label>
                <input 
                  type="text" 
                  value={form.test_name} 
                  onChange={e => setForm(f => ({ ...f, test_name: e.target.value }))} 
                  placeholder="e.g., Blood Glucose, Cholesterol, CBC"
                  required
                  className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" 
                />
              </div>
              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="block text-xs font-medium text-neutral-600 dark:text-neutral-400 mb-1">Result *</label>
                  <input 
                    type="text" 
                    value={form.result_value} 
                    onChange={e => setForm(f => ({ ...f, result_value: e.target.value }))} 
                    placeholder="120"
                    required
                    className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" 
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-neutral-600 dark:text-neutral-400 mb-1">Unit</label>
                  <input 
                    type="text" 
                    value={form.result_unit} 
                    onChange={e => setForm(f => ({ ...f, result_unit: e.target.value }))} 
                    placeholder="mg/dL"
                    className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" 
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-neutral-600 dark:text-neutral-400 mb-1">Status</label>
                  <select 
                    value={form.test_status} 
                    onChange={e => setForm(f => ({ ...f, test_status: e.target.value }))}
                    className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white"
                  >
                    <option value="normal">Normal</option>
                    <option value="abnormal">Abnormal</option>
                    <option value="critical">Critical</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">Reference Range</label>
                <input 
                  type="text" 
                  value={form.reference_range} 
                  onChange={e => setForm(f => ({ ...f, reference_range: e.target.value }))} 
                  placeholder="70-100 mg/dL"
                  className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" 
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">Lab/Facility Name</label>
                <input 
                  type="text" 
                  value={form.lab_name} 
                  onChange={e => setForm(f => ({ ...f, lab_name: e.target.value }))} 
                  placeholder="City Hospital Lab"
                  className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" 
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">Additional Notes</label>
                <textarea
                  value={form.lab_notes}
                  onChange={e => setForm(f => ({ ...f, lab_notes: e.target.value }))}
                  placeholder="Doctor's observations, recommendations..."
                  rows={3}
                  className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white resize-none"
                />
              </div>
            </div>
          )}

          {form.record_type === 'note' && (
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">Title *</label>
                <input 
                  type="text" 
                  value={form.note_title} 
                  onChange={e => setForm(f => ({ ...f, note_title: e.target.value }))} 
                  placeholder="e.g., Symptom Log, Medication Side Effects"
                  required
                  className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" 
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">Category</label>
                <select 
                  value={form.note_category} 
                  onChange={e => setForm(f => ({ ...f, note_category: e.target.value }))}
                  className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white"
                >
                  <option value="general">General</option>
                  <option value="medication">Medication</option>
                  <option value="symptom">Symptom</option>
                  <option value="lifestyle">Lifestyle</option>
                  <option value="other">Other</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">Description *</label>
                <textarea
                  value={form.note_description}
                  onChange={e => setForm(f => ({ ...f, note_description: e.target.value }))}
                  placeholder="Enter details..."
                  rows={4}
                  required
                  className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white resize-none"
                />
              </div>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-primary-500 text-white font-semibold py-3 rounded-xl hover:bg-primary-600 transition-colors disabled:opacity-50"
          >
            {loading ? 'Saving...' : 'Save Record'}
          </button>
        </form>
      </div>
    </div>
  );
};

const HealthRecord = () => {
  const [records, setRecords] = useState([]);
  const [trends, setTrends] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [typeFilter, setTypeFilter] = useState('all');

  const loadData = async () => {
    setLoading(true);
    try {
      const [recs, trendData] = await Promise.allSettled([
        apiService.get('/health-records'),
        apiService.get('/health-records/trends'),
      ]);
      console.log('[HealthRecord] API Response:', {
        recsStatus: recs.status,
        recsValue: recs.value,
        recsValueType: typeof recs.value,
        recsValueIsArray: Array.isArray(recs.value),
        recsValueLength: recs.value?.length,
      });
      if (recs.status === 'fulfilled') setRecords(recs.value || []);
      if (trendData.status === 'fulfilled') setTrends(trendData.value || []);
    } catch (error) {
      console.error('[HealthRecord] Load error:', error);
      setRecords([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadData(); }, []);

  const filtered = typeFilter === 'all' ? records : records.filter(r => r.record_type === typeFilter);

  const heartRateData = trends
    .filter(r => r.vitals?.heart_rate)
    .slice(-10)
    .map(r => ({ y: r.vitals.heart_rate, label: new Date(r.recorded_at).toLocaleDateString('en', { month: 'short', day: 'numeric' }) }));

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-neutral-900 dark:text-white">Health Record</h1>
          <p className="text-neutral-500 dark:text-neutral-400 mt-1">Your personal health history</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="bg-primary-500 text-white text-sm font-semibold px-4 py-2 rounded-xl hover:bg-primary-600 transition-colors flex items-center gap-2"
        >
          <Plus className="w-4 h-4" /> Add Record
        </button>
      </div>

      {/* Trend Chart */}
      {heartRateData.length > 1 && (
        <div className="bg-white dark:bg-neutral-800 rounded-2xl p-6 border border-neutral-200 dark:border-neutral-700 shadow-sm">
          <div className="flex items-center gap-2 mb-4">
            <Activity className="w-5 h-5 text-rose-500" />
            <h2 className="font-bold text-neutral-900 dark:text-white">Heart Rate Trend</h2>
          </div>
          <SVGLineChart
            data={heartRateData}
            color="#ef4444"
            label="bpm"
            height={120}
          />
        </div>
      )}

      {/* Filter Tabs */}
      <div className="flex gap-2 flex-wrap">
        {['all', ...RECORD_TYPES].map(type => (
          <button
            key={type}
            onClick={() => setTypeFilter(type)}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              typeFilter === type
                ? 'bg-primary-500 text-white'
                : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'
            }`}
          >
            {type === 'all' ? 'All Records' : type.replace('_', ' ')}
          </button>
        ))}
      </div>

      {/* Records List */}
      {loading ? (
        <div className="space-y-3">
          {[1, 2, 3].map(i => (
            <div key={i} className="h-16 bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 animate-pulse" />
          ))}
        </div>
      ) : filtered.length > 0 ? (
        <div className="space-y-3">
          {filtered.map(r => <RecordItem key={r.id || r._id} record={r} />)}
        </div>
      ) : (
        <div className="text-center py-16">
          <HeartPulse className="w-12 h-12 text-neutral-300 mx-auto mb-3" />
          <p className="text-neutral-500 font-medium">No health records yet</p>
          <p className="text-neutral-400 text-sm mt-1">Start tracking your health by adding a record</p>
          <button
            onClick={() => setShowModal(true)}
            className="mt-4 inline-flex items-center gap-2 bg-primary-500 text-white px-4 py-2 rounded-xl text-sm font-medium hover:bg-primary-600 transition-colors"
          >
            <Plus className="w-4 h-4" /> Add Record
          </button>
        </div>
      )}

      {showModal && (
        <AddRecordModal
          onClose={() => setShowModal(false)}
          onAdded={() => { setShowModal(false); loadData(); }}
        />
      )}
    </div>
  );
};

export default HealthRecord;
