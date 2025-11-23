import { useEffect, useState } from 'react';
import type { ScanRecord } from '@/types/scan.types';
import { formatTime } from '@/utils/datetime';

interface Props {
  scan: ScanRecord | null;
}

export function ScanResult({ scan }: Props) {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (scan) {
      setVisible(true);
      const timer = setTimeout(() => setVisible(false), 3000);
      return () => clearTimeout(timer);
    }
  }, [scan]);

  if (!scan || !visible) return null;

  return (
    <div
      className={`p-4 rounded-lg mb-4 shadow-lg border-2 transition-all ${
        scan.allowed
          ? 'bg-green-100 border-green-500 animate-pulse-success'
          : 'bg-red-100 border-red-500 animate-pulse-error'
      }`}
    >
      <div className="flex items-center justify-between mb-2">
        <div className="text-3xl">
          {scan.allowed ? '✅' : '❌'}
        </div>
        <div className="text-sm text-gray-600">
          {formatTime(scan.scan_time)}
        </div>
      </div>

      <div className="font-semibold text-lg text-gray-900">{scan.name}</div>
      <div className="text-sm text-gray-700">{scan.organization}</div>
      <div className="text-sm text-gray-600 mt-1">
        {scan.pass_type.replace('_', ' ').toUpperCase()}
      </div>

      <div
        className={`mt-3 font-semibold text-base ${
          scan.allowed ? 'text-green-700' : 'text-red-700'
        }`}
      >
        {scan.allowed ? (
          <>🎫 {scan.message || 'Entry Granted'}</>
        ) : (
          <>🚫 {scan.reason || 'Entry Denied'}</>
        )}
      </div>
    </div>
  );
}
