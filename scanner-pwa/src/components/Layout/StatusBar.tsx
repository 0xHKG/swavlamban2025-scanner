import { useSyncStore } from '@/stores/syncStore';

export function StatusBar() {
  const { isOnline, lastSync, pendingCount, totalEntries } = useSyncStore();

  return (
    <div className={`px-4 py-2 text-sm font-medium ${
      isOnline ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
    }`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span>{isOnline ? '✅' : '⚠️'}</span>
          <span>
            {isOnline ? 'Connected' : 'Offline Mode'}
          </span>
          {totalEntries > 0 && (
            <span className="ml-2 bg-gray-200 text-gray-800 px-2 py-1 rounded text-xs font-semibold">
              📋 {totalEntries} entries
            </span>
          )}
        </div>

        <div className="flex items-center gap-4">
          {pendingCount > 0 && (
            <span className="bg-blue-500 text-white px-2 py-1 rounded text-xs">
              {pendingCount} pending
            </span>
          )}
          {lastSync && (
            <span className="text-xs">
              Last sync: {new Date(lastSync).toLocaleTimeString()}
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
