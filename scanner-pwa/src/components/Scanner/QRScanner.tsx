import { useEffect, useRef, useState } from 'react';
import { BrowserMultiFormatReader } from '@zxing/browser';
import { useScanStore } from '@/stores/scanStore';
import { useAuthStore } from '@/stores/authStore';
import { validateScan } from '@/services/scanner';
import { playFeedback } from '@/utils/feedback';
import { SCAN_COOLDOWN_MS } from '@/config/constants';

export function QRScanner() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [scanning, setScanning] = useState(false);
  const [lastScan, setLastScan] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const gateNumber = useAuthStore(state => state.gateNumber);
  const addScan = useScanStore(state => state.addScan);

  useEffect(() => {
    let codeReader: BrowserMultiFormatReader | null = null;

    const startScanning = async () => {
      if (!videoRef.current) return;

      try {
        codeReader = new BrowserMultiFormatReader();

        await codeReader.decodeFromVideoDevice(
          undefined, // Auto-select camera (prefer back camera on mobile)
          videoRef.current,
          async (result, error) => {
            if (result) {
              const qrData = result.getText();

              // Prevent duplicate scans (cooldown)
              if (qrData === lastScan) return;

              setLastScan(qrData);
              setTimeout(() => setLastScan(null), SCAN_COOLDOWN_MS);

              // Validate and record
              try {
                const scanResult = await validateScan(qrData, gateNumber || '');
                addScan(scanResult);

                // Visual/audio feedback
                playFeedback(scanResult.allowed);
              } catch (err) {
                console.error('Scan validation error:', err);
              }
            }

            // Log errors silently (don't show to user as ZXing logs many harmless errors)
            if (error && error.name !== 'NotFoundException') {
              console.debug('Scanner error:', error);
            }
          }
        );

        setScanning(true);
        setError(null);
      } catch (err: any) {
        console.error('Camera error:', err);
        setError(err.message || 'Failed to start camera');
        setScanning(false);
      }
    };

    startScanning();

    return () => {
      if (codeReader) {
        codeReader.reset();
      }
    };
  }, [gateNumber, lastScan, addScan]);

  return (
    <div className="relative w-full bg-black rounded-lg overflow-hidden shadow-2xl" style={{ height: '400px' }}>
      <video
        ref={videoRef}
        className="w-full h-full object-cover"
        autoPlay
        playsInline
        muted
      />

      {!scanning && !error && (
        <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 text-white">
          <div className="text-center">
            <div className="text-xl mb-2">📷 Starting camera...</div>
            <div className="text-sm">Please grant camera permission</div>
          </div>
        </div>
      )}

      {error && (
        <div className="absolute inset-0 flex items-center justify-center bg-red-900 bg-opacity-90 text-white">
          <div className="text-center p-4">
            <div className="text-xl mb-2">❌ Camera Error</div>
            <div className="text-sm">{error}</div>
            <button
              onClick={() => window.location.reload()}
              className="mt-4 px-4 py-2 bg-white text-red-900 rounded-lg font-semibold"
            >
              Retry
            </button>
          </div>
        </div>
      )}

      {scanning && (
        <>
          {/* Scanner overlay with targeting box */}
          <div className="absolute inset-0 pointer-events-none">
            <div className="absolute inset-0 border-4 border-blue-500 opacity-30" />
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 border-4 border-white rounded-lg shadow-lg" />
          </div>

          {/* Instructions */}
          <div className="absolute bottom-4 left-0 right-0 text-center">
            <div className="inline-block bg-black bg-opacity-75 px-4 py-2 rounded-lg text-white text-sm font-medium">
              📱 Point camera at QR code
            </div>
          </div>
        </>
      )}
    </div>
  );
}
