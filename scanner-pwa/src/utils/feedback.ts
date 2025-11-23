export function playFeedback(allowed: boolean): void {
  // Visual feedback (body background flash)
  const body = document.body;
  const originalBg = body.style.backgroundColor;

  if (allowed) {
    // Green flash for allowed
    body.style.backgroundColor = '#10b981';
    body.style.transition = 'background-color 0.3s';
  } else {
    // Red flash for rejected
    body.style.backgroundColor = '#ef4444';
    body.style.transition = 'background-color 0.3s';
  }

  setTimeout(() => {
    body.style.backgroundColor = originalBg;
  }, 500);

  // Audio feedback
  try {
    if (allowed) {
      // Pleasant beep for success
      playBeep(800, 0.1, 'sine');
    } else {
      // Buzzer for failure
      playBeep(200, 0.2, 'square');
    }
  } catch (error) {
    console.log('Audio not supported:', error);
  }

  // Vibration feedback (if supported)
  if ('vibrate' in navigator) {
    if (allowed) {
      navigator.vibrate(100); // Single short vibration
    } else {
      navigator.vibrate([100, 50, 100]); // Double pulse
    }
  }
}

function playBeep(frequency: number, duration: number, type: OscillatorType): void {
  const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
  const oscillator = audioContext.createOscillator();
  const gainNode = audioContext.createGain();

  oscillator.connect(gainNode);
  gainNode.connect(audioContext.destination);

  oscillator.frequency.value = frequency;
  oscillator.type = type;

  gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
  gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + duration);

  oscillator.start(audioContext.currentTime);
  oscillator.stop(audioContext.currentTime + duration);
}

export function showToast(message: string, type: 'success' | 'error' | 'info' = 'info'): void {
  // Simple toast notification (can be enhanced with a toast library)
  const toast = document.createElement('div');
  toast.className = `fixed top-4 left-1/2 transform -translate-x-1/2 px-6 py-3 rounded-lg shadow-lg text-white font-semibold z-50 ${
    type === 'success' ? 'bg-green-600' :
    type === 'error' ? 'bg-red-600' :
    'bg-blue-600'
  }`;
  toast.textContent = message;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.remove();
  }, 3000);
}
