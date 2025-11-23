import { useState } from 'react';
import { useScanStore } from '@/stores/scanStore';
import { useSyncStore } from '@/stores/syncStore';
import { useAuthStore } from '@/stores/authStore';
import { uploadPendingScans } from '@/services/sync';

export function Footer() {
  const stats = useScanStore(state => state.stats);
  const logout = useAuthStore(state => state.logout);
  const { isSyncing, setSyncing, setLastSync, pendingCount } = useSyncStore();
  const [syncStatus, setSyncStatus] = useState<string>('');

  const successRate = stats.total > 0
    ? ((stats.successful / stats.total) * 100).toFixed(1)
    : '0.0';

  const handleSync = async () => {
    if (isSyncing) return;

    setSyncing(true);
    setSyncStatus('Syncing...');

    try {
      const result = await uploadPendingScans();
      setLastSync(new Date());
      setSyncStatus(`✅ Synced ${result.created} scans`);
      setTimeout(() => setSyncStatus(''), 3000);
    } catch (error) {
      setSyncStatus('❌ Sync failed');
      setTimeout(() => setSyncStatus(''), 3000);
    } finally {
      setSyncing(false);
    }
  };

  return (
    <div className="bg-gray-100 border-t shadow-lg">
      <div className="px-4 py-3">
        {/* Stats */}
        <div className="flex items-center justify-between mb-3 text-sm">
          <div>
            <span className="font-semibold">Today:</span> {stats.total} scans
          </div>
          <div>
            <span className="font-semibold">Success:</span> {successRate}%
          </div>
          <div>
            <span className="font-semibold">Pending:</span> {pendingCount}
          </div>
        </div>

        {/* Sync status */}
        {syncStatus && (
          <div className="mb-3 text-center text-sm font-medium text-blue-600">
            {syncStatus}
          </div>
        )}

        {/* Controls */}
        <div className="grid grid-cols-2 gap-2">
          <button
            onClick={handleSync}
            disabled={isSyncing}
            className="px-4 py-2 bg-white border border-gray-300 rounded-lg text-sm font-medium hover:bg-gray-50 disabled:opacity-50 transition-colors flex items-center justify-center gap-2"
          >
            {isSyncing ? '⏳' : '🔄'} Sync Now
          </button>

          <button
            onClick={logout}
            className="px-4 py-2 bg-red-500 text-white rounded-lg text-sm font-medium hover:bg-red-600 transition-colors flex items-center justify-center gap-2"
          >
            🚪 Logout
          </button>
        </div>
      </div>
    </div>
  );
}
