export interface GateConfig {
  name: string;
  location: string;
  date?: string;
  time?: string;
  allowedPasses: string[];
  sessionType?: string;
  tier?: number;
}

export type GateInfo = {
  gate_number: string;
  gate_location: string;
  session_type: string;
  operator: string;
};
