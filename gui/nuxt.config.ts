// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  modules: [
    '@nuxt/ui',
    '@nuxt/image',
    '@nuxt/eslint',
    '@pinia/nuxt',
    'nuxt-api-party'
  ],
  css: ['~/assets/main.css'],
  ssr: false,
  srcDir: 'src',

  apiParty: {
    endpoints: {
      backend: {
        url: 'http://localhost:8000',
        cookies: true,
        schema: 'src/assets/openapi.json',
      }
    }
  }
})