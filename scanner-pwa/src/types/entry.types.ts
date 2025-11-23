export interface Entry {
  entry_id: number;
  name: string;
  organization: string;
  mobile: string;
  qr_signature: string;
  passes: {
    exhibition_day1: boolean;
    exhibition_day2: boolean;
    interactive_sessions: boolean;
    plenary: boolean;
  };
}

export interface PendingScan {
  id?: number;
  entry_id: number;
  session_type: string;
  session_name: string;
  gate_number: string;
  gate_location: string;
  check_in_time: Date;
  scanner_device_id: string;
  scanner_operator: string;
  uploaded: boolean;
  created_at: Date;
}
