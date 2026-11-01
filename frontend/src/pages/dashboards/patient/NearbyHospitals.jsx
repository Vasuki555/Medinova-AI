/**
 * Nearby Hospitals Page
 * Find government hospitals near user's location
 */

import { useState, useEffect } from 'react';
import { apiService } from '@/services/api';
// Map rendered inline via OpenStreetMap iframe
import {
  MapPin, Phone, Clock, Navigation, Search,
  Building2, AlertCircle, Loader2
} from 'lucide-react';

const HospitalCard = ({ hospital, userLocation }) => {
  const [expanded, setExpanded] = useState(false);

  const getDirections = () => {
    const url = `https://www.google.com/maps/dir/?api=1&destination=${hospital.location?.coordinates?.[1]},${hospital.location?.coordinates?.[0]}`;
    window.open(url, '_blank');
  };

  return (
    <div className="bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 shadow-sm p-5">
      <div className="flex items-start gap-3">
        <div className="w-10 h-10 rounded-xl bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center flex-shrink-0">
          <Building2 className="w-5 h-5 text-blue-600 dark:text-blue-400" />
        </div>
        <div className="flex-grow min-w-0">
          <h3 className="font-bold text-neutral-900 dark:text-white leading-tight">{hospital.name}</h3>
          <p className="text-sm text-neutral-500 dark:text-neutral-400 mt-0.5 truncate">{hospital.address}</p>
          <div className="flex flex-wrap items-center gap-3 mt-2">
            {hospital.distance_km != null && (
              <span className="flex items-center gap-1 text-xs text-primary-500 font-medium">
                <Navigation className="w-3 h-3" />
                {hospital.distance_km.toFixed(1)} km away
              </span>
            )}
            {hospital.phone && (
              <a href={`tel:${hospital.phone}`} className="flex items-center gap-1 text-xs text-neutral-500 hover:text-primary-500">
                <Phone className="w-3 h-3" />
                {hospital.phone}
              </a>
            )}
            <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
              hospital.type === 'government'
                ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                : 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400'
            }`}>
              {hospital.type === 'government' ? '🏛️ Govt' : '🏢 Private'}
            </span>
            <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
              hospital.emergency_available
                ? 'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400'
                : 'bg-neutral-100 text-neutral-500 dark:bg-neutral-700 dark:text-neutral-400'
            }`}>
              {hospital.emergency_available ? '🚨 Emergency' : 'No Emergency'}
            </span>
          </div>
        </div>
      </div>

      {hospital.services?.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-1.5">
          {hospital.services.slice(0, 4).map(svc => (
            <span key={svc} className="text-xs bg-neutral-100 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-300 px-2 py-0.5 rounded-md">
              {svc}
            </span>
          ))}
          {hospital.services.length > 4 && (
            <span className="text-xs text-neutral-400">+{hospital.services.length - 4} more</span>
          )}
        </div>
      )}

      <div className="flex gap-2 mt-4 pt-4 border-t border-neutral-100 dark:border-neutral-700">
        <button
          onClick={getDirections}
          className="flex-1 flex items-center justify-center gap-2 bg-primary-500 text-white text-sm font-semibold py-2 rounded-xl hover:bg-primary-600 transition-colors"
        >
          <Navigation className="w-4 h-4" /> Get Directions
        </button>
        {hospital.phone && (
          <a
            href={`tel:${hospital.phone}`}
            className="flex items-center justify-center gap-2 bg-neutral-100 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 text-sm font-semibold px-4 py-2 rounded-xl hover:bg-neutral-200 dark:hover:bg-neutral-600 transition-colors"
          >
            <Phone className="w-4 h-4" /> Call
          </a>
        )}
      </div>
    </div>
  );
};

const NearbyHospitals = () => {
  const [hospitals, setHospitals] = useState([]);
  const [loading, setLoading] = useState(false);
  const [locationError, setLocationError] = useState('');
  const [userLocation, setUserLocation] = useState(null);
  const [radius, setRadius] = useState(10);
  const [search, setSearch] = useState('');
  const [hospitalType, setHospitalType] = useState('all'); // 'all', 'government', 'private'

  const fetchHospitals = async (lat, lng) => {
    setLoading(true);
    console.log('🏥 Fetching hospitals for location:', lat, lng);
    try {
      // Fetch with large radius to get all hospitals (100 km to show everything)
      const url = `/hospitals/nearby?latitude=${lat}&longitude=${lng}&radius_km=100`;
      console.log('📡 API URL:', url);
      const data = await apiService.get(url);
      console.log('✅ Hospitals received:', data?.length || 0, data);
      setHospitals(data || []);
    } catch (err) {
      console.error('❌ Error fetching hospitals:', err);
      console.error('Error details:', err.response?.data);
      setHospitals([]);
    } finally {
      setLoading(false);
    }
  };

  const getUserLocation = () => {
    setLocationError('');
    if (!navigator.geolocation) {
      setLocationError('Geolocation is not supported by your browser');
      return;
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const { latitude, longitude } = pos.coords;
        setUserLocation({ lat: latitude, lng: longitude });
        fetchHospitals(latitude, longitude);
      },
      (err) => {
        setLocationError('Unable to get your location. Please enable location permissions.');
        // Demo fallback - use a default location
        const demoLat = 12.9716;
        const demoLng = 77.5946;
        setUserLocation({ lat: demoLat, lng: demoLng });
        fetchHospitals(demoLat, demoLng);
      }
    );
  };

  useEffect(() => {
    getUserLocation();
  }, []);

  useEffect(() => {
    if (userLocation) {
      // Filter locally by radius instead of fetching again
      // This keeps all hospitals loaded and just filters the display
    }
  }, [radius]);

  const filteredHospitals = hospitals.filter(h => {
    const matchesSearch = !search || h.name.toLowerCase().includes(search.toLowerCase()) || h.address?.toLowerCase().includes(search.toLowerCase());
    const matchesType = hospitalType === 'all' || h.type === hospitalType;
    
    // Filter by radius if distance is available
    const withinRadius = !h.distance_km || h.distance_km <= radius;
    
    return matchesSearch && matchesType && withinRadius;
  });

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-neutral-900 dark:text-white">Nearby Hospitals</h1>
        <p className="text-neutral-500 dark:text-neutral-400 mt-1">Find government and private hospitals near your location</p>
      </div>

      {locationError && (
        <div className="p-4 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-2xl flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-amber-800 dark:text-amber-300 text-sm font-medium">{locationError}</p>
            <p className="text-amber-700 dark:text-amber-400 text-xs mt-1">Showing results for a default location</p>
          </div>
        </div>
      )}

      {/* Controls */}
      <div className="bg-white dark:bg-neutral-800 rounded-2xl p-5 border border-neutral-200 dark:border-neutral-700 shadow-sm space-y-4">
        <div className="flex gap-3">
          <div className="flex-grow relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-neutral-400" />
            <input
              type="text"
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="Search hospitals..."
              className="w-full pl-10 pr-4 py-2.5 border border-neutral-300 dark:border-neutral-600 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-neutral-700 dark:text-white"
            />
          </div>
          <button
            onClick={getUserLocation}
            className="flex items-center gap-2 bg-primary-500 text-white text-sm font-semibold px-4 py-2.5 rounded-xl hover:bg-primary-600 transition-colors flex-shrink-0"
          >
            <Navigation className="w-4 h-4" />
            <span className="hidden sm:inline">My Location</span>
          </button>
        </div>
        
        {/* Hospital Type Filter */}
        <div className="flex gap-2 flex-wrap">
          <button
            onClick={() => setHospitalType('all')}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              hospitalType === 'all'
                ? 'bg-primary-500 text-white'
                : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'
            }`}
          >
            All Hospitals
          </button>
          <button
            onClick={() => setHospitalType('government')}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              hospitalType === 'government'
                ? 'bg-primary-500 text-white'
                : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'
            }`}
          >
            🏛️ Government
          </button>
          <button
            onClick={() => setHospitalType('private')}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
              hospitalType === 'private'
                ? 'bg-primary-500 text-white'
                : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-600 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'
            }`}
          >
            🏢 Private
          </button>
        </div>
        
        <div className="flex items-center gap-3">
          <label className="text-sm font-medium text-neutral-700 dark:text-neutral-300 flex-shrink-0">Radius:</label>
          <input
            type="range"
            min={1}
            max={50}
            value={radius}
            onChange={e => setRadius(Number(e.target.value))}
            className="flex-grow accent-primary-500"
          />
          <span className="text-sm font-bold text-primary-500 flex-shrink-0 w-12">{radius} km</span>
        </div>
      </div>

      {/* Map with all hospitals */}
      {userLocation && hospitals.length > 0 && (
        <div className="bg-white dark:bg-neutral-800 rounded-2xl border border-neutral-200 dark:border-neutral-700 overflow-hidden shadow-sm" style={{ height: '500px' }}>
          <iframe
            width="100%"
            height="100%"
            style={{ border: 0 }}
            loading="lazy"
            referrerPolicy="no-referrer-when-downgrade"
            src={`https://www.google.com/maps/embed/v1/search?key=AIzaSyBFw0Qbyq9zTFTd-tUY6dZWTgaQzuU17R8&q=hospitals+near+${userLocation.lat},${userLocation.lng}&zoom=12&center=${userLocation.lat},${userLocation.lng}`}
          ></iframe>
        </div>
      )}

      {/* Results */}
      <div>
        <p className="text-sm text-neutral-500 dark:text-neutral-400 mb-3">
          {loading ? 'Searching...' : `${filteredHospitals.length} hospital${filteredHospitals.length !== 1 ? 's' : ''} found`}
        </p>

        {loading ? (
          <div className="flex items-center justify-center py-16">
            <Loader2 className="w-8 h-8 text-primary-500 animate-spin" />
          </div>
        ) : filteredHospitals.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {filteredHospitals.map(h => (
              <HospitalCard key={h.id || h._id} hospital={h} userLocation={userLocation} />
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <Building2 className="w-12 h-12 text-neutral-300 mx-auto mb-3" />
            <p className="text-neutral-500 font-medium">No hospitals found in range</p>
            <p className="text-neutral-400 text-sm mt-1">Try increasing the radius</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default NearbyHospitals;
