import {useLocalStorage} from '@vueuse/core'

export default defineNuxtRouteMiddleware(async (to, from) => {
    const authStore = useAuthStore()
    const token = useLocalStorage('auth_token', '')

    
    if(!token.value && !authStore.isAuthenticated && to.path !== '/auth/login'){
        return navigateTo('/auth/login')
    }

    if (token.value && !authStore.isAuthenticated) {
        await authStore.fetchMe();
    }
    
    if (to.meta.requiresAuth && !authStore.isAuthenticated && to.path !== '/auth/login'){
        return navigateTo('/auth/login')
    }

    
    if (to.meta.resource && !authStore.hasAccess("retrieve", to.meta.resource as string)){
        return abortNavigation()
    }


})