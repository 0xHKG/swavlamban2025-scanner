import { format } from 'date-fns';

export function validateDateTime(
  currentDate: Date,
  currentTime: string,
  allowedDate: string,
  timeRange: string
): { valid: boolean; reason?: string } {
  // Check date
  const dateStr = format(currentDate, 'yyyy-MM-dd');
  if (dateStr !== allowedDate) {
    return { valid: false, reason: 'Wrong date for this pass' };
  }

  // Check time range
  const [startTime, endTime] = timeRange.split('-');
  if (currentTime < startTime || currentTime > endTime) {
    return { valid: false, reason: `Gates open ${timeRange}` };
  }

  return { valid: true };
}

export function parseQRData(qrString: string): {
  entry_id: number;
  pass_type: string;
  signature: string;
} | null {
  try {
    const parts = qrString.split(':');
    if (parts.length !== 3) return null;

    const entry_id = parseInt(parts[0], 10);
    if (isNaN(entry_id)) return null;

    return {
      entry_id,
      pass_type: parts[1],
      signature: parts[2]
    };
  } catch (error) {
    return null;
  }
}

export function formatTime(date: Date): string {
  return format(date, 'HHmm');
}

export function formatDate(date: Date): string {
  return format(date, 'yyyy-MM-dd');
}
