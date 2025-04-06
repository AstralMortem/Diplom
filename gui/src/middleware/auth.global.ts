export default defineNuxtRouteMiddleware(async (to, from) => {
    const authStore = useAuthStore()
    const token = useCookie('med_voice_auth_token')

    if(!token.value && !authStore.isAuthenticated && to.path !== '/auth/login'){
        return navigateTo('/auth/login')
    }

    if (token.value && !authStore.isAuthenticated) {
        await authStore.fetchMe();
    }
    
    if (to.meta.requiresAuth && !authStore.isAuthenticated && to.path !== '/auth/login'){
        return navigateTo('/auth/login')
    }


})