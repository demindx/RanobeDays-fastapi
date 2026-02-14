export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'rd-bg': 'var(--background-color)',
        'rd-surface': 'var(--fourth-color)',
        'rd-surface-elevated': 'var(--surface-elevated-color)',
        'rd-accent': 'var(--first-color)',
        'rd-accent-soft': 'var(--secondary-color)',
        'rd-text': 'var(--foreground-third-color)',
        'rd-text-muted': 'var(--foreground-secondary-color)',
        'rd-text-strong': 'var(--foreground-color)',
        'rd-danger': 'var(--danger-color)',
      },
      spacing: {
        'rd-1': '0.25rem',
        'rd-2': '0.5rem',
        'rd-3': '0.75rem',
        'rd-4': '1rem',
        'rd-6': '1.5rem',
        'rd-8': '2rem',
      },
      borderRadius: {
        'rd-sm': '0.375rem',
        'rd-md': '0.5rem',
        'rd-lg': '0.75rem',
        'rd-xl': '1rem',
      },
      boxShadow: {
        'rd-soft': 'var(--shadow-soft)',
        'rd-md': 'var(--shadow-md)',
        'rd-lg': 'var(--shadow-lg)',
      },
      fontFamily: {
        body: ['var(--font-body)'],
        display: ['var(--font-display)'],
      },
      screens: {
        xs: '420px',
        '3xl': '1600px',
      },
    },
  },
  plugins: [],
}
