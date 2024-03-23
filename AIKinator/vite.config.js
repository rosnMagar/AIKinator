import { defineConfig } from 'vite'

// https://vitejs.dev/config/
export default defineConfig({
  plugins:[restart()],
  server: {
    watch: {
      usePolling: true
    }
  },
  css: {
    postcss: {
      plugins: [tailwindcss()],
    },
  }
})