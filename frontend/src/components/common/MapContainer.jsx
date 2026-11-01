/**
 * Map Container Component
 * Renders Leaflet OpenStreetMap dynamically with custom markers
 */

import { useEffect, useRef, useState } from 'react';

const MapContainer = ({ hospitals = [], center = [28.6139, 77.2090], zoom = 13, onMarkerClick }) => {
  const mapRef = useRef(null);
  const leafletMapInstance = useRef(null);
  const markersGroupRef = useRef(null);
  const [isLoaded, setIsLoaded] = useState(false);

  // Dynamically load Leaflet assets from CDN
  useEffect(() => {
    // Add CSS
    const cssId = 'leaflet-cdn-css';
    if (!document.getElementById(cssId)) {
      const link = document.createElement('link');
      link.id = cssId;
      link.rel = 'stylesheet';
      link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
      link.integrity = 'sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=';
      link.crossOrigin = '';
      document.head.appendChild(link);
    }

    // Add JS
    const jsId = 'leaflet-cdn-js';
    if (!document.getElementById(jsId)) {
      const script = document.createElement('script');
      script.id = jsId;
      script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
      script.integrity = 'sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=';
      script.crossOrigin = '';
      script.onload = () => setIsLoaded(true);
      document.head.appendChild(script);
    } else {
      if (window.L) {
        setIsLoaded(true);
      }
    }
  }, []);

  // Initialize Map
  useEffect(() => {
    if (!isLoaded || !mapRef.current || !window.L) return;

    const L = window.L;

    // Reset instance if exists
    if (leafletMapInstance.current) {
      leafletMapInstance.current.remove();
    }

    // Set custom icon
    const defaultIcon = L.icon({
      iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
      shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41]
    });
    L.Marker.prototype.options.icon = defaultIcon;

    // Create map
    leafletMapInstance.current = L.map(mapRef.current, {
      center: center,
      zoom: zoom,
      zoomControl: true
    });

    // Add OpenStreetMap tile layer (premium dark or light mode based on body classes)
    const isDarkMode = document.documentElement.classList.contains('dark');
    const tileUrl = isDarkMode
      ? 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
      : 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

    L.tileLayer(tileUrl, {
      attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
    }).addTo(leafletMapInstance.current);

    markersGroupRef.current = L.layerGroup().addTo(leafletMapInstance.current);

    return () => {
      if (leafletMapInstance.current) {
        leafletMapInstance.current.remove();
        leafletMapInstance.current = null;
      }
    };
  }, [isLoaded]);

  // Handle center or zoom updates
  useEffect(() => {
    if (leafletMapInstance.current && window.L) {
      leafletMapInstance.current.setView(center, zoom);
    }
  }, [center, zoom]);

  // Update Markers
  useEffect(() => {
    if (!isLoaded || !leafletMapInstance.current || !markersGroupRef.current || !window.L) return;

    const L = window.L;
    markersGroupRef.current.clearLayers();

    // Red Cross icon for Government Hospitals
    const hospitalIcon = L.icon({
      iconUrl: 'https://cdn-icons-png.flaticon.com/512/809/809957.png', // red cross hospital pin
      iconSize: [32, 32],
      iconAnchor: [16, 32],
      popupAnchor: [0, -32]
    });

    hospitals.forEach((hosp) => {
      const coords = hosp.address?.location?.coordinates;
      if (!coords || coords.length < 2) return;
      
      // Coordinates in DB are [lng, lat], Leaflet wants [lat, lng]
      const lat = coords[1];
      const lng = coords[0];

      const marker = L.marker([lat, lng], { icon: hospitalIcon })
        .addTo(markersGroupRef.current);

      const popupContent = `
        <div class="p-2 text-neutral-900 font-sans">
          <h4 class="font-bold text-sm text-primary-700">${hosp.name}</h4>
          <p class="text-xs text-neutral-600 mt-1">${hosp.address.street || ''}, ${hosp.address.city}</p>
          <div class="flex gap-2 items-center mt-2 text-xs">
            <span class="bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded-full font-semibold">
              ${hosp.facilities?.emergency_services ? '24/7 ER' : 'OPD Only'}
            </span>
            <span class="text-neutral-500">Rating: ${hosp.rating || '4.0'}★</span>
          </div>
        </div>
      `;

      marker.bindPopup(popupContent);

      marker.on('click', () => {
        if (onMarkerClick) {
          onMarkerClick(hosp);
        }
      });
    });
  }, [isLoaded, hospitals]);

  return (
    <div className="relative w-full h-full min-h-[350px] bg-neutral-800 rounded-2xl overflow-hidden shadow-glass border border-white/10">
      {!isLoaded && (
        <div className="absolute inset-0 z-10 flex flex-col items-center justify-center bg-neutral-900/80 backdrop-blur-md">
          <div className="w-12 h-12 border-4 border-primary-500 border-t-transparent rounded-full animate-spin"></div>
          <span className="text-white mt-4 font-semibold tracking-wide">Loading Leaflet Map...</span>
        </div>
      )}
      <div ref={mapRef} className="w-full h-full min-h-[350px] z-0" />
    </div>
  );
};

export default MapContainer;
