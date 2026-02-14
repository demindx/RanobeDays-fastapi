import { fileURLToPath, URL } from 'node:url'

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import tailwindcss from '@tailwindcss/vite'
import { visualizer } from 'rollup-plugin-visualizer'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const isTest = mode === 'test' || process.env.VITEST === 'true'
  const isAnalyze = env.VITE_BUNDLE_ANALYZE === 'true'
  const usePolling = env.VITE_USE_POLLING === 'true'
  const pollingInterval = Number(env.VITE_POLLING_INTERVAL || 1000)

  return {
    plugins: [
      vue(),
      !isTest && vueDevTools(),
      tailwindcss(),
      isAnalyze &&
        visualizer({
          filename: 'dist/stats.html',
          open: false,
          gzipSize: true,
          brotliSize: true,
        }),
    ].filter(Boolean),
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
    test: {
      environment: 'jsdom',
      globals: true,
      include: ['src/**/*.spec.js'],
    },
    server: usePolling
      ? {
          watch: {
            usePolling: true,
            interval: pollingInterval,
          },
        }
      : undefined,
  }
})
