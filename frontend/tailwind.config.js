export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        "rd-bg": "var(--background-color)",
        "rd-surface": "var(--fourth-color)",
        "rd-accent": "var(--first-color)",
        "rd-accent-soft": "var(--secondary-color)",
        "rd-text": "var(--foreground-third-color)",
        "rd-text-muted": "var(--foreground-secondary-color)",
        "rd-text-strong": "var(--foreground-color)",
      },
    },
  },
  plugins: [],
}
