import Dexie, { Table } from 'dexie';
import type { Entry, PendingScan } from '@/types/entry.types';

export class ScannerDB extends Dexie {
  entries!: Table<Entry, number>;
  pending_scans!: Table<PendingScan, number>;

  constructor() {
    super('ScannerDB');
    this.version(1).stores({
      entries: 'entry_id, qr_signature, organization',
      pending_scans: '++id, entry_id, uploaded, check_in_time'
    });
  }

  // Sync entries from API
  async syncEntries(entries: Entry[]): Promise<void> {
    await this.entries.clear();
    await this.entries.bulkAdd(entries);
  }

  // Get entry by signature
  async getEntryBySignature(signature: string): Promise<Entry | undefined> {
    return await this.entries.where('qr_signature').equals(signature).first();
  }

  // Get entry by ID
  async getEntryById(entryId: number): Promise<Entry | undefined> {
    return await this.entries.get(entryId);
  }

  // Add pending scan
  async addPendingScan(scan: Omit<PendingScan, 'id' | 'created_at'>): Promise<number> {
    return await this.pending_scans.add({
      ...scan,
      created_at: new Date(),
      uploaded: false
    });
  }

  // Get all unuploaded scans
  async getUnuploadedScans(): Promise<PendingScan[]> {
    return await this.pending_scans.where('uploaded').equals(false).toArray();
  }

  // Mark scans as uploaded
  async markScansAsUploaded(scanIds: number[]): Promise<void> {
    await this.pending_scans.bulkUpdate(
      scanIds.map(id => ({ key: id, changes: { uploaded: true } }))
    );
  }

  // Get total entry count
  async getTotalEntries(): Promise<number> {
    return await this.entries.count();
  }

  // Get pending scans count
  async getPendingScansCount(): Promise<number> {
    return await this.pending_scans.where('uploaded').equals(false).count();
  }

  // Clear all pending scans (for testing)
  async clearPendingScans(): Promise<void> {
    await this.pending_scans.clear();
  }
}

export const db = new ScannerDB();
