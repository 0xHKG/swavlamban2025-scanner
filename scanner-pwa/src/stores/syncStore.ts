import { create } from 'zustand';

interface SyncState {
  isOnline: boolean;
  isSyncing: boolean;
  lastSync: Date | null;
  pendingCount: number;
  setOnline: (online: boolean) => void;
  setSyncing: (syncing: boolean) => void;
  setLastSync: (date: Date) => void;
  setPendingCount: (count: number) => void;
}

export const useSyncStore = create<SyncState>((set) => ({
  isOnline: navigator.onLine,
  isSyncing: false,
  lastSync: null,
  pendingCount: 0,

  setOnline: (online) => set({ isOnline: online }),

  setSyncing: (syncing) => set({ isSyncing: syncing }),

  setLastSync: (date) => set({ lastSync: date }),

  setPendingCount: (count) => set({ pendingCount: count })
}));
