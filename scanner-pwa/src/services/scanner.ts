import { db } from './db';
import { parseQRData } from '@/utils/validation';
import { GATE_CONFIG } from '@/config/gates';
import { formatDate, getCurrentTime, getDeviceId } from '@/utils/datetime';
import type { ScanRecord } from '@/types/scan.types';
import { getStoredOperator } from './auth';

export async function validateScan(
  qrData: string,
  gateNumber: string
): Promise<ScanRecord> {
  // Parse QR code
  const parsed = parseQRData(qrData);
  if (!parsed) {
    return createErrorResult('Invalid QR code format');
  }

  // Find entry in offline database
  const entry = await db.getEntryById(parsed.entry_id);
  if (!entry) {
    return createErrorResult('Entry not found');
  }

  // Verify signature
  if (entry.qr_signature !== parsed.signature) {
    return createErrorResult('Invalid QR signature');
  }

  // Get gate config
  const gate = GATE_CONFIG[gateNumber as keyof typeof GATE_CONFIG];
  if (!gate) {
    return createErrorResult('Invalid gate');
  }

  // Check if pass type is allowed at this gate
  if (gate.allowedPasses && gate.allowedPasses.length > 0) {
    if (!(gate.allowedPasses as readonly string[]).includes(parsed.pass_type)) {
      return createErrorResult('Wrong pass for this gate');
    }
  }

  // Check date (simplified - if gate has date restriction)
  if (gate.date) {
    const now = new Date();
    const currentDate = formatDate(now);
    const currentTime = getCurrentTime();

    if (currentDate !== gate.date) {
      return createErrorResult('Wrong date for this pass');
    }

    // Check time range
    if (gate.time) {
      const [startTime, endTime] = gate.time.split('-');
      if (currentTime < startTime || currentTime > endTime) {
        return createErrorResult(`Session time: ${gate.time}`);
      }
    }
  }

  // Record scan in pending queue
  const now = new Date();
  const operator = getStoredOperator() || 'unknown';

  await db.addPendingScan({
    entry_id: entry.entry_id,
    session_type: gate.sessionType || parsed.pass_type,
    session_name: gate.name,
    gate_number: gateNumber,
    gate_location: gate.location,
    check_in_time: now,
    scanner_device_id: getDeviceId(),
    scanner_operator: operator,
    uploaded: false
  });

  // Return success
  return {
    entry_id: entry.entry_id,
    name: entry.name,
    organization: entry.organization,
    pass_type: parsed.pass_type,
    gate_number: gateNumber,
    scan_time: now,
    allowed: true,
    message: 'Entry granted',
    uploaded: false
  };
}

function createErrorResult(reason: string): ScanRecord {
  return {
    entry_id: 0,
    name: 'Unknown',
    organization: 'Unknown',
    pass_type: 'unknown',
    gate_number: '',
    scan_time: new Date(),
    allowed: false,
    reason,
    uploaded: false
  };
}
