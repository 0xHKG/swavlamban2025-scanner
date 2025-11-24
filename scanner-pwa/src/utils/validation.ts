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
  name?: string;
  id_type?: string;
} | null {
  try {
    // Try new human-readable format first
    // Format:
    // SWAVLAMBAN 2025 ENTRY PASS
    //
    // Name: John Doe
    // ID Type: Aadhaar
    // ID Number: 1234-5678-9012
    //
    // Session: Exhibition - 25 Nov
    // ...

    if (qrString.includes('SWAVLAMBAN 2025 ENTRY PASS')) {
      const lines = qrString.split('\n');

      let name = '';
      let idType = '';
      let idNumber = '';
      let session = '';

      for (const line of lines) {
        if (line.startsWith('Name:')) {
          name = line.replace('Name:', '').trim();
        } else if (line.startsWith('ID Type:')) {
          idType = line.replace('ID Type:', '').trim();
        } else if (line.startsWith('ID Number:')) {
          // Remove hyphens from formatted ID number
          idNumber = line.replace('ID Number:', '').trim().replace(/-/g, '');
        } else if (line.startsWith('Session:')) {
          session = line.replace('Session:', '').trim();
        }
      }

      if (!name || !idNumber) return null;

      // Determine pass type from session name
      let pass_type = 'unknown';
      if (session.includes('25 Nov') && session.includes('Exhibition')) {
        pass_type = 'exhibition_day1';
      } else if (session.includes('26 Nov') && session.includes('Exhibition')) {
        pass_type = 'exhibition_day2';
      } else if (session.includes('25 & 26') || session.includes('both')) {
        pass_type = 'exhibition_both_days';
      } else if (session.toLowerCase().includes('interactive')) {
        pass_type = 'interactive_sessions';
      } else if (session.toLowerCase().includes('plenary')) {
        pass_type = 'plenary';
      }

      // Use ID number as signature (for matching with downloaded entries)
      return {
        entry_id: 0, // Will be looked up by ID number
        pass_type,
        signature: idNumber,
        name,
        id_type: idType
      };
    }

    // Fallback to old format: entryId:passType:signature
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
