/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        success: '#10b981',
        error: '#ef4444',
        warning: '#f59e0b',
      },
      animation: {
        'pulse-success': 'pulse 0.5s cubic-bezier(0.4, 0, 0.6, 1)',
        'pulse-error': 'pulse 0.5s cubic-bezier(0.4, 0, 0.6, 1)',
      }
    },
  },
  plugins: [],
}
