import { useMDNS } from "~/composables/useMDNS"
import {useLocalStorage} from '@vueuse/core'

function createBackend(mdns: Ref, localFetch: any){
  const token = useLocalStorage('auth_token', '')
  const options = {
    baseURL: mdns.value,
    headers: [["Authorization", `Bearer ${token.value}`]]
  }
  return createOpenFetch(options, localFetch)

}

export default defineNuxtPlugin({
  enforce: 'pre', // clients will be ready to use by other plugins, Pinia stores etc.
  async setup() {
    const clients = useRuntimeConfig().public.openFetch
    const localFetch = useRequestFetch()

    const mdns = await useMDNS()

    return {
      provide: Object.entries(clients).reduce((acc, [name, options]) => ({
        ...acc,
        [name]: name === 'backend'? createBackend(mdns, localFetch) : createOpenFetch(options, localFetch)

        // or add the logging:

        // [name]: createOpenFetch(localOptions => ({
        //   ...options,
        //   ...localOptions,
        //   onRequest(ctx) {
        //     console.log('My logging', ctx.request)
        //     return localOptions?.onRequest?.(ctx)
        //   }
        // }), localFetch)
      }), {})
    }
  }
})