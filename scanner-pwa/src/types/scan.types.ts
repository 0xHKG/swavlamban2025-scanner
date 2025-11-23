export interface ScanRecord {
  id?: number;
  entry_id: number;
  name: string;
  organization: string;
  pass_type: string;
  gate_number: string;
  scan_time: Date;
  allowed: boolean;
  reason?: string;
  message?: string;
  uploaded: boolean;
}

export interface ScanStats {
  total: number;
  successful: number;
  rejected: number;
}
