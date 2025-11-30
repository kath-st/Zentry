/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        zentry: {
          dark: "#0B0A15",
          card: "#151423",
          primary: "#6366F1",
          secondary: "#8B5CF6",
          text: "#E2E8F0",
          muted: "#94A3B8",
          success: "#10B981",
          error: "#EF4444",
          warning: "#F59E0B"
        }
      }
    },
  },
  plugins: [],
}