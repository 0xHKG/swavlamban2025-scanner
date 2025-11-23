import { create } from 'zustand';
import type { ScanRecord, ScanStats } from '@/types/scan.types';

interface ScanState {
  recentScans: ScanRecord[];
  stats: ScanStats;
  addScan: (scan: ScanRecord) => void;
  clearScans: () => void;
  resetStats: () => void;
}

export const useScanStore = create<ScanState>((set) => ({
  recentScans: [],
  stats: { total: 0, successful: 0, rejected: 0 },

  addScan: (scan) => set((state) => {
    // Keep only last 10 scans
    const newScans = [scan, ...state.recentScans].slice(0, 10);

    // Update stats
    const newStats = {
      total: state.stats.total + 1,
      successful: scan.allowed ? state.stats.successful + 1 : state.stats.successful,
      rejected: !scan.allowed ? state.stats.rejected + 1 : state.stats.rejected
    };

    return {
      recentScans: newScans,
      stats: newStats
    };
  }),

  clearScans: () => set({ recentScans: [] }),

  resetStats: () => set({ stats: { total: 0, successful: 0, rejected: 0 } })
}));
