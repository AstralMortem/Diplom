export default defineNuxtRouteMiddleware(async (to, from) => {
    const authStore = useAuthStore()

    if (to.meta.requiresAuth && !authStore.isAuthenticated){
        return navigateTo('/auth/login')
    }
    
    if (to.meta.resource && !authStore.hasAccess("retrieve", to.meta.resource as string)){
        return abortNavigation()
    }


})