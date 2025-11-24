import { API_BASE_URL, STORAGE_KEYS } from '@/config/constants';

export async function apiCall<T = any>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = sessionStorage.getItem(STORAGE_KEYS.TOKEN);

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers
    }
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'API request failed' }));
    throw new Error(error.detail || error.message || error.error || 'API request failed');
  }

  return response.json();
}

export const api = {
  get: <T = any>(endpoint: string) => apiCall<T>(endpoint, { method: 'GET' }),

  post: <T = any>(endpoint: string, data: any) =>
    apiCall<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data)
    }),

  put: <T = any>(endpoint: string, data: any) =>
    apiCall<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data)
    }),

  delete: <T = any>(endpoint: string) =>
    apiCall<T>(endpoint, { method: 'DELETE' })
};
