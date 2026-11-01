/**
 * Medications Page
 * Patient medication tracker with schedule and intake logging
 */

import { useState, useEffect } from 'react';
import { apiService } from '@/services/api';
import {
  Pill, Plus, Clock, CheckCircle, X, Trash2,
  Edit2, AlertCircle, Calendar, Package
} from 'lucide-react';

const FREQUENCIES = ['Once daily', 'Twice daily', 'Three times daily', 'Four times daily', 'As needed', 'Weekly'];
const TIMES = ['Morning', 'Afternoon', 'Evening', 'Night', 'Bedtime'];

const MedCard = ({ med, onLog, onDelete }) => {
  const [logging, setLogging] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const handleLog = async (taken) => {
    setLogging(true);
    try {
      await apiService.post(`/medications/${med.id}/log`, {
        taken,
        logged_at: new Date().toISOString(),
        notes: taken ? 'Taken on schedule' : 'Dose skipped',
      });
      onLog(med.id, taken);
    } catch {
      alert('Failed to log dose');
    } finally {
      setLogging(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm(`Remove ${med.name} from your tracker?`)) return;
    setDeleting(true);
    try {
      await apiService.delete(`/medications/${med.id}`);
      onDelete(med.id);
    } catch {
      alert('Failed to remove medication');
      setDeleting(false);
    }
  };

  const stockLevel = med.current_stock != null ? med.current_stock : null;
  const stockPercent = med.total_stock ? (stockLevel / med.total_stock) * 100 : null;

  return (
    <div className={`bg-white dark:bg-neutral-800 rounded-2xl border shadow-sm p-5 ${
      med.is_active !== false
        ? 'border-neutral-200 dark:border-neutral-700'
        : 'border-dashed border-neutral-300 dark:border-neutral-600 opacity-60'
    }`}>
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3">
          <div className="w-10 h-10 rounded-xl bg-violet-100 dark:bg-violet-900/30 flex items-center justify-center flex-shrink-0">
            <Pill className="w-5 h-5 text-violet-600 dark:text-violet-400" />
          </div>
          <div>
            <h3 className="font-bold text-neutral-900 dark:text-white">{med.name}</h3>
            <p className="text-sm text-neutral-500 dark:text-neutral-400">
              {med.dosage} · {med.frequency}
            </p>
            {med.schedule_times?.length > 0 && (
              <div className="flex flex-wrap gap-1 mt-2">
                {med.schedule_times.map(time => (
                  <span key={time} className="text-xs bg-neutral-100 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-300 px-2 py-0.5 rounded-md flex items-center gap-1">
                    <Clock className="w-3 h-3" /> {time}
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>
        <button
          onClick={handleDelete}
          disabled={deleting}
          className="p-1.5 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg text-neutral-400 hover:text-red-500 transition-colors"
        >
          <Trash2 className="w-4 h-4" />
        </button>
      </div>

      {/* Stock Level */}
      {stockLevel !== null && (
        <div className="mt-4">
          <div className="flex items-center justify-between text-xs mb-1">
            <span className="flex items-center gap-1 text-neutral-500 dark:text-neutral-400">
              <Package className="w-3 h-3" /> Stock
            </span>
            <span className={`font-medium ${
              stockLevel < 5 ? 'text-red-500' : stockLevel < 15 ? 'text-amber-500' : 'text-neutral-700 dark:text-neutral-300'
            }`}>
              {stockLevel} remaining
              {stockLevel < 5 && ' ⚠️ Low!'}
            </span>
          </div>
          {stockPercent !== null && (
            <div className="w-full h-1.5 bg-neutral-100 dark:bg-neutral-700 rounded-full overflow-hidden">
              <div
                className={`h-full rounded-full transition-all ${
                  stockPercent < 20 ? 'bg-red-500' : stockPercent < 40 ? 'bg-amber-500' : 'bg-emerald-500'
                }`}
                style={{ width: `${Math.min(stockPercent, 100)}%` }}
              />
            </div>
          )}
        </div>
      )}

      {/* Intake Log Today */}
      {med.is_active !== false && (
        <div className="flex gap-2 mt-4 pt-4 border-t border-neutral-100 dark:border-neutral-700">
          <button
            onClick={() => handleLog(true)}
            disabled={logging}
            className="flex-1 flex items-center justify-center gap-2 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600 dark:text-emerald-400 text-sm font-semibold py-2 rounded-xl hover:bg-emerald-100 dark:hover:bg-emerald-900/30 transition-colors disabled:opacity-50"
          >
            <CheckCircle className="w-4 h-4" /> Taken
          </button>
          <button
            onClick={() => handleLog(false)}
            disabled={logging}
            className="flex-1 flex items-center justify-center gap-2 bg-neutral-50 dark:bg-neutral-700/40 text-neutral-500 dark:text-neutral-400 text-sm font-semibold py-2 rounded-xl hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors disabled:opacity-50"
          >
            <X className="w-4 h-4" /> Skipped
          </button>
        </div>
      )}

      {med.notes && (
        <p className="text-xs text-neutral-400 mt-3 italic">"{med.notes}"</p>
      )}
    </div>
  );
};

const AddMedicationModal = ({ onClose, onAdded }) => {
  const [form, setForm] = useState({
    name: '',
    dosage: '',
    frequency: 'Once daily',
    schedule_times: [],
    start_date: '',
    end_date: '',
    total_stock: '',
    current_stock: '',
    notes: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const toggleTime = (time) => {
    setForm(f => ({
      ...f,
      schedule_times: f.schedule_times.includes(time)
        ? f.schedule_times.filter(t => t !== time)
        : [...f.schedule_times, time]
    }));
  };

  // Helper function to convert time labels to HH:MM format
  const convertTimeToFormat = (timeLabel) => {
    const timeMap = {
      'Morning': '08:00',
      'Afternoon': '14:00',
      'Evening': '18:00',
      'Night': '22:00',
      'Bedtime': '23:00'
    };
    return timeMap[timeLabel] || '09:00';
  };

  // Helper function to map frequency to backend format
  const mapFrequency = (freq) => {
    if (freq.includes('As needed')) return 'as_needed';
    return 'daily';
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.name || !form.dosage) { 
      setError('Name and dosage are required'); 
      return; 
    }
    
    // Ensure at least one schedule time
    if (form.schedule_times.length === 0) {
      setError('Please select at least one schedule time');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      // Create payload matching backend schema
      const startDate = form.start_date || new Date().toISOString();
      const endDate = form.end_date || null;
      
      const payload = {
        medicine_name: form.name,
        dosage: form.dosage,
        form: 'tablet', // default form type
        schedule: {
          frequency: mapFrequency(form.frequency),
          times_per_day: form.schedule_times.length,
          time_slots: form.schedule_times.map(time => ({
            time: convertTimeToFormat(time),
            with_meal: 'anytime'
          })),
          days_of_week: [], // empty means all days
          start_date: startDate,
          end_date: endDate,
          is_ongoing: !endDate
        },
        instructions: form.notes || null,
        current_quantity: form.current_stock ? parseInt(form.current_stock) : null,
        initial_quantity: form.total_stock ? parseInt(form.total_stock) : null,
        refill_reminder_at: 5, // remind when 5 pills left
        reminder_enabled: true
      };
      
      await apiService.post('/medications', payload);
      onAdded();
      onClose();
    } catch (err) {
      console.error('Medication creation error:', err);
      setError(err.response?.data?.detail || 'Failed to add medication. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white dark:bg-neutral-800 rounded-2xl w-full max-w-md shadow-2xl animate-scale-in max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between p-6 border-b border-neutral-200 dark:border-neutral-700 sticky top-0 bg-white dark:bg-neutral-800">
          <h2 className="font-bold text-neutral-900 dark:text-white">Add Medication</h2>
          <button onClick={onClose} className="p-2 hover:bg-neutral-100 dark:hover:bg-neutral-700 rounded-xl">
            <X className="w-5 h-5 text-neutral-500" />
          </button>
        </div>
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {error && <div className="p-3 bg-red-50 border border-red-200 rounded-xl text-red-600 text-sm">{error}</div>}

          <div className="grid grid-cols-2 gap-3">
            <div className="col-span-2">
              <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">
                Medicine Name <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                value={form.name}
                onChange={e => setForm(f => ({ ...f, name: e.target.value }))}
                placeholder="e.g., Paracetamol"
                className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">Dosage <span className="text-red-500">*</span></label>
              <input
                type="text"
                value={form.dosage}
                onChange={e => setForm(f => ({ ...f, dosage: e.target.value }))}
                placeholder="e.g., 500mg"
                className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">Frequency</label>
              <select
                value={form.frequency}
                onChange={e => setForm(f => ({ ...f, frequency: e.target.value }))}
                className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white"
              >
                {FREQUENCIES.map(f => <option key={f} value={f}>{f}</option>)}
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-2">Schedule Times</label>
            <div className="flex flex-wrap gap-2">
              {TIMES.map(time => (
                <button
                  key={time}
                  type="button"
                  onClick={() => toggleTime(time)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                    form.schedule_times.includes(time)
                      ? 'bg-primary-500 text-white'
                      : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'
                  }`}
                >
                  {time}
                </button>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">Start Date</label>
              <input type="date" value={form.start_date} onChange={e => setForm(f => ({ ...f, start_date: e.target.value }))} className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" />
            </div>
            <div>
              <label className="block text-xs font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">End Date</label>
              <input type="date" value={form.end_date} onChange={e => setForm(f => ({ ...f, end_date: e.target.value }))} className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" />
            </div>
            <div>
              <label className="block text-xs font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">Total Stock (pills)</label>
              <input type="number" value={form.total_stock} onChange={e => setForm(f => ({ ...f, total_stock: e.target.value, current_stock: e.target.value }))} placeholder="30" className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" />
            </div>
            <div>
              <label className="block text-xs font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">Current Stock</label>
              <input type="number" value={form.current_stock} onChange={e => setForm(f => ({ ...f, current_stock: e.target.value }))} placeholder="30" className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white" />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">Notes</label>
            <textarea
              value={form.notes}
              onChange={e => setForm(f => ({ ...f, notes: e.target.value }))}
              placeholder="Any special instructions..."
              rows={2}
              className="w-full px-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white resize-none"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-primary-500 text-white font-semibold py-3 rounded-xl hover:bg-primary-600 transition-colors disabled:opacity-50"
          >
            {loading ? 'Adding...' : 'Add Medication'}
          </button>
        </form>
      </div>
    </div>
  );
};

const Medications = () => {
  const [medications, setMedications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [filter, setFilter] = useState('active');

  const loadMeds = async () => {
    setLoading(true);
    try {
      const data = await apiService.get('/medications');
      setMedications(data || []);
    } catch {
      setMedications([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadMeds(); }, []);

  const handleLog = (id, taken) => {
    // Optimistic update - could show a toast here
  };

  const handleDelete = (id) => {
    setMedications(prev => prev.filter(m => m.id !== id));
  };

  const activeMeds = medications.filter(m => m.is_active !== false);
  const inactiveMeds = medications.filter(m => m.is_active === false);
  const filtered = filter === 'active' ? activeMeds : filter === 'inactive' ? inactiveMeds : medications;

  const lowStock = activeMeds.filter(m => m.current_stock != null && m.current_stock < 5);

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-neutral-900 dark:text-white">My Medications</h1>
          <p className="text-neutral-500 dark:text-neutral-400 mt-1">Track and manage your medication schedule</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="bg-primary-500 text-white text-sm font-semibold px-4 py-2 rounded-xl hover:bg-primary-600 transition-colors flex items-center gap-2"
        >
          <Plus className="w-4 h-4" /> Add Medication
        </button>
      </div>

      {/* Low stock alert */}
      {lowStock.length > 0 && (
        <div className="p-4 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-2xl flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-amber-600 dark:text-amber-400 flex-shrink-0 mt-0.5" />
          <div>
            <p className="font-semibold text-amber-800 dark:text-amber-300 text-sm">Low Stock Alert</p>
            <p className="text-amber-700 dark:text-amber-400 text-sm mt-0.5">
              {lowStock.map(m => m.name).join(', ')} {lowStock.length === 1 ? 'is' : 'are'} running low. Please refill soon.
            </p>
          </div>
        </div>
      )}

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white dark:bg-neutral-800 rounded-2xl p-4 border border-neutral-200 dark:border-neutral-700 text-center">
          <p className="text-2xl font-black text-primary-500">{activeMeds.length}</p>
          <p className="text-xs text-neutral-500 mt-1">Active</p>
        </div>
        <div className="bg-white dark:bg-neutral-800 rounded-2xl p-4 border border-neutral-200 dark:border-neutral-700 text-center">
          <p className="text-2xl font-black text-amber-500">{lowStock.length}</p>
          <p className="text-xs text-neutral-500 mt-1">Low Stock</p>
        </div>
        <div className="bg-white dark:bg-neutral-800 rounded-2xl p-4 border border-neutral-200 dark:border-neutral-700 text-center">
          <p className="text-2xl font-black text-neutral-400">{inactiveMeds.length}</p>
          <p className="text-xs text-neutral-500 mt-1">Inactive</p>
        </div>
      </div>

      {/* Filter */}
      <div className="flex gap-2">
        {[{ key: 'active', label: 'Active' }, { key: 'inactive', label: 'Inactive' }, { key: 'all', label: 'All' }].map(tab => (
          <button
            key={tab.key}
            onClick={() => setFilter(tab.key)}
            className={`px-4 py-2 rounded-xl text-sm font-medium transition-colors ${
              filter === tab.key
                ? 'bg-primary-500 text-white'
                : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[1, 2, 3, 4].map(i => (
            <div key={i} className="h-40 bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 animate-pulse" />
          ))}
        </div>
      ) : filtered.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filtered.map(med => (
            <MedCard key={med.id} med={med} onLog={handleLog} onDelete={handleDelete} />
          ))}
        </div>
      ) : (
        <div className="text-center py-16">
          <Pill className="w-12 h-12 text-neutral-300 mx-auto mb-3" />
          <p className="text-neutral-500 font-medium">No medications tracked</p>
          <p className="text-neutral-400 text-sm mt-1">Add your first medication to start tracking</p>
          <button
            onClick={() => setShowModal(true)}
            className="mt-4 inline-flex items-center gap-2 bg-primary-500 text-white px-4 py-2 rounded-xl text-sm font-medium hover:bg-primary-600 transition-colors"
          >
            <Plus className="w-4 h-4" /> Add Medication
          </button>
        </div>
      )}

      {showModal && (
        <AddMedicationModal
          onClose={() => setShowModal(false)}
          onAdded={() => { setShowModal(false); loadMeds(); }}
        />
      )}
    </div>
  );
};

export default Medications;
