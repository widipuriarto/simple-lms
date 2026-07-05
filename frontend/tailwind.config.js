/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        apple: {
          bg: '#F5F5F7',
          dark: '#1D1D1F',
          blue: '#0071E3',
          'blue-hover': '#0077ED',
          gray: '#86868B',
          light: '#FFFFFF'
        }
      },
      fontFamily: {
        sans: [
          '-apple-system', 
          'BlinkMacSystemFont', 
          '"SF Pro Text"', 
          '"Segoe UI"', 
          'Roboto', 
          'Helvetica', 
          'Arial', 
          'sans-serif'
        ],
      },
      boxShadow: {
        'apple': '0 4px 24px rgba(0, 0, 0, 0.04)',
        'apple-lg': '0 8px 32px rgba(0, 0, 0, 0.08)',
      },
      borderRadius: {
        '2xl': '16px',
        '3xl': '24px',
      }
    },
  },
  plugins: [],
}
