import { api } from './api';
import { STORAGE_KEYS } from '@/config/constants';
import type { LoginRequest, LoginResponse } from '@/types/api.types';

export async function login(
  username: string,
  password: string,
  gateNumber: string
): Promise<LoginResponse> {
  const response = await api.post<LoginResponse>('/scanner/login', {
    username,
    password,
    gate_number: gateNumber
  } as LoginRequest);

  // Store token and gate info
  sessionStorage.setItem(STORAGE_KEYS.TOKEN, response.token);
  sessionStorage.setItem(STORAGE_KEYS.GATE_NUMBER, response.gate_info.gate_number);
  sessionStorage.setItem(STORAGE_KEYS.OPERATOR, response.gate_info.operator);

  return response;
}

export function logout(): void {
  sessionStorage.clear();
  localStorage.clear();
  window.location.reload();
}

export function getStoredToken(): string | null {
  return sessionStorage.getItem(STORAGE_KEYS.TOKEN);
}

export function getStoredGateNumber(): string | null {
  return sessionStorage.getItem(STORAGE_KEYS.GATE_NUMBER);
}

export function getStoredOperator(): string | null {
  return sessionStorage.getItem(STORAGE_KEYS.OPERATOR);
}

export function isAuthenticated(): boolean {
  return !!getStoredToken();
}
