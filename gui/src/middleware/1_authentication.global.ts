import {useLocalStorage} from '@vueuse/core'
import type { NuxtError } from '#app'

export default defineNuxtRouteMiddleware(async (to, from) => {
    const authStore = useAuthStore()
    const token = useLocalStorage<string | null>('auth_token', null)


    if(!token.value && to.path !== '/auth/login'){
        return navigateTo('/auth/login')
    }

    if(token.value && !authStore.isAuthenticated){
        try{
            await authStore.fetchMe();
            return navigateTo(to.fullPath)
        }catch(error){
            if((error as NuxtError).statusCode == 401){
                token.value = null
                return navigateTo('/auth/login')
            }else{
                backendError(error)
            }
        }
    }

})