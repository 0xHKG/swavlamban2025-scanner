export const APP_NAME = 'Swavlamban 2025 Scanner';
export const APP_VERSION = '1.0.0';

// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Scanning Configuration
export const SCAN_COOLDOWN_MS = 2000; // Prevent duplicate scans within 2 seconds
export const AUTO_SLEEP_MS = 30000; // Auto-sleep camera after 30 seconds of inactivity

// Sync Configuration
export const SYNC_INTERVAL_MS = 5 * 60 * 1000; // Sync every 5 minutes
export const MAX_OFFLINE_SCANS = 1000; // Maximum scans to store offline

// Session Storage Keys
export const STORAGE_KEYS = {
  TOKEN: 'scanner_token',
  GATE_NUMBER: 'gate_number',
  OPERATOR: 'operator',
  LAST_SYNC: 'last_sync'
} as const;

// Pass Types
export const PASS_TYPES = {
  EXHIBITION_DAY1: 'exhibition_day1',
  EXHIBITION_DAY2: 'exhibition_day2',
  INTERACTIVE_SESSIONS: 'interactive_sessions',
  PLENARY: 'plenary',
  EXHIBITOR: 'exhibitor_pass'
} as const;

// Event Dates
export const EVENT_DATES = {
  DAY1: '2025-11-25',
  DAY2: '2025-11-26'
} as const;
