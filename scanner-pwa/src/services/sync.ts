import { db } from './db';
import { api } from './api';
import type { Entry } from '@/types/entry.types';
import type { BatchCheckInRequest, BatchCheckInResponse } from '@/types/api.types';
import { toISOString } from '@/utils/datetime';

export async function downloadEntries(gateNumber?: string, date?: string): Promise<number> {
  try {
    const params = new URLSearchParams();
    if (gateNumber) params.append('gate_number', gateNumber);
    if (date) params.append('date', date);

    const response = await api.get<{ success: boolean; count: number; entries: Entry[] }>(
      `/scanner/entries?${params.toString()}`
    );

    if (response.success && response.entries) {
      await db.syncEntries(response.entries);
      return response.count;
    }

    return 0;
  } catch (error) {
    console.error('Failed to download entries:', error);
    throw error;
  }
}

export async function uploadPendingScans(): Promise<{
  total: number;
  created: number;
  duplicates: number;
  errors: number;
}> {
  try {
    const pendingScans = await db.getUnuploadedScans();

    if (pendingScans.length === 0) {
      return { total: 0, created: 0, duplicates: 0, errors: 0 };
    }

    // Convert to API format
    const checkins = pendingScans.map((scan) => ({
      entry_id: scan.entry_id,
      session_type: scan.session_type,
      session_name: scan.session_name,
      gate_number: scan.gate_number,
      gate_location: scan.gate_location,
      scanner_device_id: scan.scanner_device_id,
      scanner_operator: scan.scanner_operator,
      check_in_time: toISOString(scan.check_in_time),
      verification_status: 'verified',
      notes: undefined
    }));

    const response = await api.post<BatchCheckInResponse>('/scanner/checkin/batch', {
      checkins
    } as BatchCheckInRequest);

    if (response.success) {
      // Mark all scans as uploaded
      const scanIds = pendingScans.map((scan) => scan.id!).filter((id) => id !== undefined);
      await db.markScansAsUploaded(scanIds);
    }

    return {
      total: response.total,
      created: response.created,
      duplicates: response.duplicates,
      errors: response.errors
    };
  } catch (error) {
    console.error('Failed to upload pending scans:', error);
    throw error;
  }
}

export async function getSyncStats(): Promise<{
  totalEntries: number;
  pendingScans: number;
}> {
  const totalEntries = await db.getTotalEntries();
  const pendingScans = await db.getPendingScansCount();

  return {
    totalEntries,
    pendingScans
  };
}
