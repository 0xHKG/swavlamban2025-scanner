import { useScanStore } from '@/stores/scanStore';
import { formatTime } from '@/utils/datetime';

export function ScanHistory() {
  const recentScans = useScanStore(state => state.recentScans);

  if (recentScans.length === 0) {
    return (
      <div className="bg-gray-50 rounded-lg p-6 text-center">
        <div className="text-4xl mb-2">📋</div>
        <div className="text-gray-600">No scans yet</div>
        <div className="text-sm text-gray-500 mt-1">Scan a QR code to get started</div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden">
      <div className="bg-gray-800 text-white px-4 py-3 font-semibold">
        📋 Recent Scans ({recentScans.length})
      </div>

      <div className="divide-y divide-gray-200 max-h-96 overflow-y-auto">
        {recentScans.map((scan, index) => (
          <div
            key={`${scan.entry_id}-${scan.scan_time}-${index}`}
            className={`p-3 ${
              scan.allowed ? 'bg-white hover:bg-green-50' : 'bg-red-50 hover:bg-red-100'
            } transition-colors`}
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <span className="text-xl">
                    {scan.allowed ? '✅' : '❌'}
                  </span>
                  <span className="font-medium text-gray-900">
                    {scan.name}
                  </span>
                </div>
                <div className="text-sm text-gray-600 ml-7">
                  {scan.organization}
                </div>
                <div className="text-xs text-gray-500 ml-7 mt-1">
                  {scan.pass_type.replace('_', ' ').toUpperCase()}
                </div>
              </div>
              <div className="text-xs text-gray-500 text-right">
                {formatTime(scan.scan_time)}
              </div>
            </div>

            {!scan.allowed && scan.reason && (
              <div className="mt-2 ml-7 text-sm text-red-600 font-medium">
                {scan.reason}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
