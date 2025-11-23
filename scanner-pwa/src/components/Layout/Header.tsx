import { useEffect, useState } from 'react';
import { useAuthStore } from '@/stores/authStore';
import { useSyncStore } from '@/stores/syncStore';

export function Header() {
  const { gateNumber, operator } = useAuthStore();
  const isOnline = useSyncStore(state => state.isOnline);
  const [battery, setBattery] = useState(100);
  const [currentTime, setCurrentTime] = useState(new Date());

  // Update battery level
  useEffect(() => {
    if ('getBattery' in navigator) {
      (navigator as any).getBattery().then((battery: any) => {
        setBattery(Math.round(battery.level * 100));
        battery.addEventListener('levelchange', () => {
          setBattery(Math.round(battery.level * 100));
        });
      });
    }
  }, []);

  // Update time every second
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="bg-gray-800 text-white shadow-lg">
      <div className="px-4 py-3">
        <div className="flex items-center justify-between">
          {/* Left: Event branding */}
          <div>
            <div className="text-xl font-bold flex items-center gap-2">
              🎫 Swavlamban 2025
            </div>
            <div className="text-sm text-gray-300 mt-1">
              {gateNumber} • {operator}
            </div>
          </div>

          {/* Right: Status indicators */}
          <div className="flex items-center gap-4 text-sm">
            {/* Time */}
            <div className="text-right">
              <div className="font-mono font-bold">
                {currentTime.toLocaleTimeString('en-IN', {
                  hour: '2-digit',
                  minute: '2-digit',
                  second: '2-digit'
                })}
              </div>
              <div className="text-xs text-gray-400">
                {currentTime.toLocaleDateString('en-IN')}
              </div>
            </div>

            {/* Online/Offline */}
            <div
              className={`flex items-center gap-1 px-2 py-1 rounded ${
                isOnline ? 'bg-green-600' : 'bg-red-600'
              }`}
            >
              <span>{isOnline ? '📶' : '📵'}</span>
              <span className="text-xs font-medium">
                {isOnline ? 'Online' : 'Offline'}
              </span>
            </div>

            {/* Battery */}
            <div className="flex items-center gap-1">
              <span>🔋</span>
              <span className="text-xs font-medium">{battery}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
