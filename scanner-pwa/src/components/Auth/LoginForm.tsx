import { useState } from 'react';
import { useAuthStore } from '@/stores/authStore';
import { login } from '@/services/auth';

export function LoginForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [gateNumber, setGateNumber] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const setAuth = useAuthStore(state => state.setAuth);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await login(username, password, gateNumber);
      setAuth(response.token, response.gate_info);
    } catch (err: any) {
      setError(err.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 sm:p-6" style={{ background: 'linear-gradient(135deg, #1a365d 0%, #2c5282 50%, #1a365d 100%)' }}>
      <div className="bg-white rounded-xl shadow-2xl p-6 sm:p-8 w-full max-w-md border border-gray-200">
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <span className="text-5xl">🇮🇳</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold mb-2" style={{ color: '#1a365d' }}>
            Swavlamban 2025
          </h1>
          <h2 className="text-base sm:text-lg" style={{ color: '#4a5568' }}>Scanner Login</h2>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-medium mb-2" style={{ color: '#4a5568' }}>
              Username
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-4 py-4 rounded-lg text-base"
              style={{ border: '1px solid #cbd5e0', outline: 'none', fontSize: '16px' }}
              placeholder="Enter username"
              required
              autoComplete="username"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2" style={{ color: '#4a5568' }}>
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-4 rounded-lg text-base"
              style={{ border: '1px solid #cbd5e0', outline: 'none', fontSize: '16px' }}
              placeholder="Enter password"
              required
              autoComplete="current-password"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2" style={{ color: '#4a5568' }}>
              Gate Number
            </label>
            <select
              value={gateNumber}
              onChange={(e) => setGateNumber(e.target.value)}
              className="w-full px-4 py-4 rounded-lg text-base"
              style={{ border: '1px solid #cbd5e0', outline: 'none', fontSize: '16px' }}
              required
            >
              <option value="">Select Gate</option>
              <option value="Main Entrance">Main Entrance</option>
              <option value="Gate 1">Gate 1 - Exhibition Day 1</option>
              <option value="Gate 2">Gate 2 - Exhibition Day 2</option>
              <option value="Gate 3">Gate 3 - Interactive Sessions</option>
              <option value="Gate 4">Gate 4 - Plenary Session</option>
            </select>
          </div>

          {error && (
            <div className="p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg">
              <p className="text-sm font-medium">{error}</p>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full text-white py-4 rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-lg mt-2"
            style={{ backgroundColor: loading ? '#4a5568' : '#1a365d', minHeight: '56px' }}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className="mt-6 text-center text-sm" style={{ color: '#718096' }}>
          <p>🔒 Secure scanner access</p>
          <p className="mt-1">Indian Navy • TDAC</p>
        </div>
      </div>
    </div>
  );
}
