export const GATE_CONFIG = {
  'Gate 1': {
    name: 'Gate 1 - Exhibition Day 1',
    location: 'Exhibition Hall',
    date: '2025-11-25',
    time: '0001-1730',
    allowedPasses: ['exhibition_day1', 'exhibitor_pass'],
    sessionType: 'exhibition_day1'
  },
  'Gate 2': {
    name: 'Gate 2 - Exhibition Day 2',
    location: 'Exhibition Hall',
    date: '2025-11-26',
    time: '0700-1730',
    allowedPasses: ['exhibition_day2', 'exhibitor_pass'],
    sessionType: 'exhibition_day2'
  },
  'Gate 3': {
    name: 'Gate 3 - Interactive Sessions',
    location: 'Zorawar Hall',
    date: '2025-11-26',
    time: '1020-1330',
    allowedPasses: ['interactive_sessions'],
    sessionType: 'interactive_sessions'
  },
  'Gate 4': {
    name: 'Gate 4 - Plenary Session',
    location: 'Zorawar Hall',
    date: '2025-11-26',
    time: '1500-1615',
    allowedPasses: ['plenary'],
    sessionType: 'plenary'
  },
  'Main Entrance': {
    name: 'Main Entrance',
    location: 'Manekshaw Centre',
    date: null,
    time: null,
    allowedPasses: [], // All passes (date-specific)
    sessionType: null
  }
} as const;

export type GateNumber = keyof typeof GATE_CONFIG;
