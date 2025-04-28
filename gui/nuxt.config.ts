// https://nuxt.com/docs/api/configuration/nuxt-config
import { resolve } from 'path'
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: false },
  css: ['~/assets/main.css'],
  modules: [
    '@nuxt/ui',
    '@nuxt/image',
    '@nuxt/icon',
    '@nuxt/eslint',
    'nuxt-open-fetch',
    '@pinia/nuxt'
  ],
  srcDir: 'src/',
  ssr: false,
  openFetch: {
    disableNuxtPlugin: true,
    clients: {
      backend: {
        schema: './openapi.json'
      }
    }
  },
  devServer: { host: process.env.TAURI_DEV_HOST || 'localhost' },
  vite: {
    // Better support for Tauri CLI output
    clearScreen: false,
    // Enable environment variables
    // Additional environment variables can be found at
    // https://v2.tauri.app/reference/environment-variables/
    envPrefix: ['VITE_', 'TAURI_'],
    server: {
      // Tauri requires a consistent port
      strictPort: true,
    },
    resolve: {
      alias: {
        html2canvas: resolve(__dirname, 'node_modules/html2canvas-pro')
      }
    }
  },

})