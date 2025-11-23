import { useState } from 'react';
import { useAuthStore } from '@/stores/authStore';
import { GATE_CONFIG } from '@/config/gates';

export function GateSelector() {
  const [selectedGate, setSelectedGate] = useState('');
  const setGate = useAuthStore(state => state.setGate);

  const handleSelect = () => {
    if (selectedGate) {
      setGate(selectedGate);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-800 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-2xl p-8 w-full max-w-md">
        <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
          Select Your Gate
        </h2>

        <div className="space-y-3 mb-6">
          {Object.entries(GATE_CONFIG).map(([key, gate]) => (
            <button
              key={key}
              onClick={() => setSelectedGate(key)}
              className={`w-full p-4 border-2 rounded-lg text-left transition-all ${
                selectedGate === key
                  ? 'border-blue-600 bg-blue-50 shadow-md'
                  : 'border-gray-300 hover:border-blue-400 hover:shadow'
              }`}
            >
              <div className="font-semibold text-gray-900">{gate.name}</div>
              <div className="text-sm text-gray-600 mt-1">{gate.location}</div>
              {gate.time && (
                <div className="text-xs text-gray-500 mt-1">⏰ {gate.time}</div>
              )}
            </button>
          ))}
        </div>

        <button
          onClick={handleSelect}
          disabled={!selectedGate}
          className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Continue
        </button>
      </div>
    </div>
  );
}
