/**
 * QR Scanner Component
 * Camera-based QR code scanner AND file upload for mobile and desktop
 * Uses html5-qrcode library for cross-platform scanning
 * Supports: Live camera + Image file upload
 */

import { useEffect, useRef, useState } from 'react';
import { Camera, X, AlertCircle, CheckCircle, Loader2, Upload, Image as ImageIcon } from 'lucide-react';

const QRScanner = ({ onScan, onClose }) => {
  const [mode, setMode] = useState('camera'); // 'camera' or 'file'
  const [scanning, setScanning] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [libraryLoading, setLibraryLoading] = useState(true);
  const scannerRef = useRef(null);
  const html5QrcodeRef = useRef(null);
  const fileInputRef = useRef(null);
  const libraryLoadedRef = useRef(false);

  // Load html5-qrcode library once on mount
  useEffect(() => {
    if (!libraryLoadedRef.current && !window.Html5Qrcode) {
      const script = document.createElement('script');
      script.src = 'https://unpkg.com/html5-qrcode@2.3.8/html5-qrcode.min.js';
      script.async = true;
      script.onload = () => {
        libraryLoadedRef.current = true;
        setLibraryLoading(false);
      };
      script.onerror = () => {
        setError('Failed to load QR scanner library. Please check your internet connection.');
        setLibraryLoading(false);
      };
      document.body.appendChild(script);
    } else if (window.Html5Qrcode) {
      libraryLoadedRef.current = true;
      setLibraryLoading(false);
    }

    return () => {
      if (html5QrcodeRef.current) {
        html5QrcodeRef.current.stop().catch(err => console.error('Cleanup error:', err));
      }
    };
  }, []);

  useEffect(() => {
    if (mode === 'camera' && libraryLoadedRef.current) {
      initCameraScanner();
    }
  }, [mode]);

  const initCameraScanner = async () => {
    try {
      // Wait for library to load
      if (!window.Html5Qrcode) {
        setError('QR scanner library loading...');
        setTimeout(initCameraScanner, 500);
        return;
      }
      startCamera();
    } catch (err) {
      setError('Failed to load QR scanner: ' + err.message);
    }
  };

  const startCamera = async () => {
    try {
      const Html5Qrcode = window.Html5Qrcode;
      if (!Html5Qrcode) {
        throw new Error('QR scanner library not loaded');
      }

      html5QrcodeRef.current = new Html5Qrcode('qr-reader');
      
      setScanning(true);
      
      await html5QrcodeRef.current.start(
        { facingMode: 'environment' }, // Use back camera on mobile
        {
          fps: 10,
          qrbox: { width: 250, height: 250 },
        },
        (decodedText) => {
          // Success callback
          handleScanSuccess(decodedText);
        },
        (errorMessage) => {
          // Error callback (fires frequently, ignore unless critical)
          if (!errorMessage.includes('NotFoundException')) {
            console.debug('QR scan error:', errorMessage);
          }
        }
      );
    } catch (err) {
      console.error('Camera start error:', err);
      setError(err.message || 'Failed to start camera. Please check permissions.');
      setScanning(false);
    }
  };

  const handleScanSuccess = (decodedText) => {
    setSuccess(true);
    setScanning(false);
    
    // Stop scanner
    if (html5QrcodeRef.current) {
      html5QrcodeRef.current.stop().then(() => {
        onScan(decodedText);
      }).catch(err => console.error('Stop error:', err));
    } else {
      onScan(decodedText);
    }
  };

  const handleFileSelect = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setError('');
    setScanning(true);

    try {
      // Check if library is loaded
      if (!window.Html5Qrcode) {
        throw new Error('QR scanner library not loaded yet. Please wait a moment and try again.');
      }

      const Html5Qrcode = window.Html5Qrcode;
      const html5Qrcode = new Html5Qrcode('qr-file-reader');

      // Scan the file directly
      const decodedText = await html5Qrcode.scanFile(file, true);
      
      // Clear the scanner instance
      await html5Qrcode.clear();
      
      handleScanSuccess(decodedText);
    } catch (err) {
      console.error('File scan error:', err);
      const errorMsg = err.message || 'Could not detect QR code in this image.';
      setError(errorMsg.includes('QR') ? errorMsg : 'Could not detect QR code in this image. Please try another image.');
      setScanning(false);
    } finally {
      // Reset file input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleBrowseClick = () => {
    fileInputRef.current?.click();
  };

  const handleClose = () => {
    if (html5QrcodeRef.current) {
      html5QrcodeRef.current.stop().then(() => {
        onClose();
      }).catch(err => {
        console.error('Close error:', err);
        onClose();
      });
    } else {
      onClose();
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4 animate-fade-in">
      <div className="bg-white dark:bg-neutral-800 rounded-2xl max-w-md w-full overflow-hidden shadow-2xl">
        {/* Header */}
        <div className="bg-gradient-to-r from-primary-500 to-cyan-500 p-4 flex items-center justify-between">
          <div className="flex items-center gap-2 text-white">
            {mode === 'camera' ? <Camera className="w-5 h-5" /> : <ImageIcon className="w-5 h-5" />}
            <h3 className="font-bold">Scan QR Code</h3>
          </div>
          <button
            onClick={handleClose}
            className="text-white hover:bg-white/20 p-1 rounded-lg transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Mode Toggle */}
        <div className="p-4 border-b border-neutral-200 dark:border-neutral-700">
          <div className="flex gap-2">
            <button
              onClick={() => setMode('camera')}
              className={`flex-1 flex items-center justify-center gap-2 py-2 px-3 rounded-lg font-medium text-sm transition-all ${
                mode === 'camera'
                  ? 'bg-primary-500 text-white shadow-md'
                  : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'
              }`}
            >
              <Camera className="w-4 h-4" />
              Camera
            </button>
            <button
              onClick={() => setMode('file')}
              className={`flex-1 flex items-center justify-center gap-2 py-2 px-3 rounded-lg font-medium text-sm transition-all ${
                mode === 'file'
                  ? 'bg-primary-500 text-white shadow-md'
                  : 'bg-neutral-100 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-200 dark:hover:bg-neutral-600'
              }`}
            >
              <Upload className="w-4 h-4" />
              Upload Photo
            </button>
          </div>
        </div>

        {/* Scanner Container */}
        <div className="p-4">
          {error ? (
            <div className="text-center py-8">
              <AlertCircle className="w-12 h-12 text-red-400 mx-auto mb-3" />
              <p className="text-sm font-semibold text-neutral-900 dark:text-white mb-2">
                Scanner Error
              </p>
              <p className="text-xs text-neutral-500 dark:text-neutral-400 mb-4">
                {error}
              </p>
              <button
                onClick={handleClose}
                className="px-4 py-2 bg-neutral-200 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 rounded-xl text-sm font-medium hover:bg-neutral-300 dark:hover:bg-neutral-600 transition-colors"
              >
                Close
              </button>
            </div>
          ) : success ? (
            <div className="text-center py-8">
              <CheckCircle className="w-12 h-12 text-emerald-400 mx-auto mb-3" />
              <p className="text-sm font-semibold text-neutral-900 dark:text-white mb-2">
                QR Code Scanned Successfully!
              </p>
              <p className="text-xs text-neutral-500 dark:text-neutral-400">
                Processing...
              </p>
            </div>
          ) : mode === 'camera' ? (
            <>
              {/* Camera Scanner */}
              <div 
                id="qr-reader" 
                className="w-full rounded-xl overflow-hidden bg-neutral-100 dark:bg-neutral-700"
                style={{ minHeight: '300px' }}
              />
              
              {/* Camera Instructions */}
              <div className="mt-4 text-center">
                {scanning ? (
                  <>
                    <div className="flex items-center justify-center gap-2 text-primary-600 dark:text-primary-400 mb-2">
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <p className="text-sm font-medium">Camera active</p>
                    </div>
                    <p className="text-xs text-neutral-500 dark:text-neutral-400">
                      Position the QR code within the frame
                    </p>
                  </>
                ) : (
                  <p className="text-xs text-neutral-500 dark:text-neutral-400">
                    Initializing camera...
                  </p>
                )}
              </div>

              {/* Tips */}
              <div className="mt-4 p-3 bg-primary-50 dark:bg-primary-900/20 rounded-xl border border-primary-200 dark:border-primary-800">
                <p className="text-xs text-neutral-600 dark:text-neutral-400">
                  <strong className="text-primary-700 dark:text-primary-300">Tips:</strong>
                  <br />
                  • Hold steady and ensure good lighting
                  <br />
                  • Keep the QR code within the frame
                  <br />
                  • Scanning happens automatically
                </p>
              </div>
            </>
          ) : (
            <>
              {/* File Upload */}
              <div className="space-y-4">
                {/* Hidden file input */}
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleFileSelect}
                  className="hidden"
                />

                {/* Upload Button */}
                <button
                  onClick={handleBrowseClick}
                  disabled={scanning || libraryLoading}
                  className="w-full flex flex-col items-center justify-center gap-3 py-12 border-2 border-dashed border-neutral-300 dark:border-neutral-600 rounded-xl hover:border-primary-500 hover:bg-primary-50 dark:hover:bg-primary-900/10 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {libraryLoading ? (
                    <>
                      <Loader2 className="w-12 h-12 text-cyan-500 animate-spin" />
                      <p className="text-sm font-medium text-neutral-900 dark:text-white">
                        Loading QR scanner...
                      </p>
                      <p className="text-xs text-neutral-500 dark:text-neutral-400">
                        Please wait a moment
                      </p>
                    </>
                  ) : scanning ? (
                    <>
                      <Loader2 className="w-12 h-12 text-primary-500 animate-spin" />
                      <p className="text-sm font-medium text-neutral-900 dark:text-white">
                        Scanning image...
                      </p>
                      <p className="text-xs text-neutral-500 dark:text-neutral-400">
                        This may take a few seconds
                      </p>
                    </>
                  ) : (
                    <>
                      <div className="w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-full flex items-center justify-center">
                        <Upload className="w-8 h-8 text-primary-600 dark:text-primary-400" />
                      </div>
                      <div className="text-center">
                        <p className="text-sm font-semibold text-neutral-900 dark:text-white mb-1">
                          Upload QR Code Image
                        </p>
                        <p className="text-xs text-neutral-500 dark:text-neutral-400">
                          Click to browse photos
                        </p>
                      </div>
                    </>
                  )}
                </button>

                {/* Hidden div for file scanning */}
                <div id="qr-file-reader" className="hidden" />

                {/* Tips */}
                <div className="p-3 bg-cyan-50 dark:bg-cyan-900/20 rounded-xl border border-cyan-200 dark:border-cyan-800">
                  <p className="text-xs text-neutral-600 dark:text-neutral-400">
                    <strong className="text-cyan-700 dark:text-cyan-300">Tips:</strong>
                    <br />
                    • Use clear, well-lit photos
                    <br />
                    • Ensure the entire QR code is visible
                    <br />
                    • Avoid blurry or distorted images
                    <br />
                    • Supports JPEG, PNG, WebP formats
                  </p>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default QRScanner;
