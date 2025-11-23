import { useEffect } from 'react';
import { useAuthStore } from './stores/authStore';
import { useScanStore } from './stores/scanStore';
import { useSyncStore } from './stores/syncStore';
import { LoginForm } from './components/Auth/LoginForm';
import { Header } from './components/Layout/Header';
import { Footer } from './components/Layout/Footer';
import { StatusBar } from './components/Layout/StatusBar';
import { QRScanner } from './components/Scanner/QRScanner';
import { ScanResult } from './components/Scanner/ScanResult';
import { ScanHistory } from './components/Scanner/ScanHistory';
import { downloadEntries, uploadPendingScans, getSyncStats } from './services/sync';
import { SYNC_INTERVAL_MS } from './config/constants';

function App() {
  const token = useAuthStore(state => state.token);
  const gateNumber = useAuthStore(state => state.gateNumber);
  const recentScans = useScanStore(state => state.recentScans);
  const { setOnline, setSyncing, setLastSync, setPendingCount } = useSyncStore();

  // Get latest scan for display
  const latestScan = recentScans.length > 0 ? recentScans[0] : null;

  // Monitor online/offline status
  useEffect(() => {
    const updateOnlineStatus = () => {
      setOnline(navigator.onLine);
    };

    window.addEventListener('online', updateOnlineStatus);
    window.addEventListener('offline', updateOnlineStatus);

    return () => {
      window.removeEventListener('online', updateOnlineStatus);
      window.removeEventListener('offline', updateOnlineStatus);
    };
  }, [setOnline]);

  // Download entries on login
  useEffect(() => {
    if (token && gateNumber) {
      const loadEntries = async () => {
        try {
          const count = await downloadEntries(gateNumber);
          console.log(`Downloaded ${count} entries for ${gateNumber}`);
        } catch (error) {
          console.error('Failed to download entries:', error);
        }
      };

      loadEntries();
    }
  }, [token, gateNumber]);

  // Background sync every 5 minutes
  useEffect(() => {
    if (!token) return;

    const syncInterval = setInterval(async () => {
      if (navigator.onLine) {
        try {
          setSyncing(true);
          await uploadPendingScans();
          setLastSync(new Date());

          // Update pending count
          const stats = await getSyncStats();
          setPendingCount(stats.pendingScans);
        } catch (error) {
          console.error('Background sync failed:', error);
        } finally {
          setSyncing(false);
        }
      }
    }, SYNC_INTERVAL_MS);

    return () => clearInterval(syncInterval);
  }, [token, setSyncing, setLastSync, setPendingCount]);

  // Update pending count on mount and after each scan
  useEffect(() => {
    if (token) {
      getSyncStats().then(stats => {
        setPendingCount(stats.pendingScans);
      });
    }
  }, [token, recentScans.length, setPendingCount]);

  // Show login if not authenticated
  if (!token || !gateNumber) {
    return <LoginForm />;
  }

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <Header />
      <StatusBar />

      <main className="flex-1 container mx-auto px-4 py-6 max-w-2xl">
        {/* Scanner */}
        <div className="mb-6">
          <QRScanner />
        </div>

        {/* Latest Scan Result */}
        <ScanResult scan={latestScan} />

        {/* Scan History */}
        <ScanHistory />
      </main>

      <Footer />
    </div>
  );
}

export default App;
