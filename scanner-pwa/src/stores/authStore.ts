import { create } from 'zustand';
import { getStoredToken, getStoredGateNumber, getStoredOperator } from '@/services/auth';
import type { GateInfo } from '@/types/gate.types';

interface AuthState {
  token: string | null;
  gateNumber: string | null;
  operator: string | null;
  gateInfo: GateInfo | null;
  setAuth: (token: string, gateInfo: GateInfo) => void;
  setGate: (gate: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: getStoredToken(),
  gateNumber: getStoredGateNumber(),
  operator: getStoredOperator(),
  gateInfo: null,

  setAuth: (token, gateInfo) => {
    set({
      token,
      gateInfo,
      operator: gateInfo.operator,
      gateNumber: gateInfo.gate_number
    });
  },

  setGate: (gate) => {
    sessionStorage.setItem('gate_number', gate);
    set({ gateNumber: gate });
  },

  logout: () => {
    sessionStorage.clear();
    localStorage.clear();
    set({ token: null, gateNumber: null, operator: null, gateInfo: null });
    window.location.reload();
  }
}));
