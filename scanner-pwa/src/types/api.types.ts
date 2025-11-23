export interface LoginRequest {
  username: string;
  password: string;
  gate_number: string;
}

export interface LoginResponse {
  success: boolean;
  token: string;
  expires_at: string;
  gate_info: {
    gate_number: string;
    gate_location: string;
    session_type: string;
    operator: string;
  };
}

export interface VerifyRequest {
  qr_data: string;
  gate_number: string;
  scan_time: string;
}

export interface VerifyResponse {
  success: boolean;
  allowed: boolean;
  entry?: {
    entry_id: number;
    name: string;
    organization: string;
    pass_type: string;
  };
  message?: string;
  reason?: string;
}

export interface CheckInRequest {
  entry_id: number;
  session_type: string;
  session_name: string;
  gate_number: string;
  gate_location: string;
  scanner_device_id: string;
  scanner_operator: string;
  check_in_time: string;
  verification_status: string;
  notes?: string;
}

export interface CheckInResponse {
  success: boolean;
  checkin_id?: number;
  message: string;
  error?: string;
}

export interface BatchCheckInRequest {
  checkins: CheckInRequest[];
}

export interface BatchCheckInResponse {
  success: boolean;
  total: number;
  created: number;
  duplicates: number;
  errors: number;
  message: string;
}
