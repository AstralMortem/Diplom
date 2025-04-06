import type { components } from "#nuxt-api-party/backend";
import {FetchError} from 'ofetch';
import { defineStore } from "pinia";

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: {} as components["schemas"]["DoctorDetailRead"],
        isPending: false
    }),
    actions: {
        async login(username: string, password: string){
            try{
                this.isPending = true
                await $backend('/api/v1/auth/login', {
                    method: 'POST',
                    body: {
                        username,
                        password
                    }
                })
                this.isPending = false
                const cookie = useCookie('med_voice_auth_token')
                if(cookie.value){
                    await this.fetchMe()
                }else{
                    throw new FetchError('No cookie found')
                }
                
            }catch(error){
                this.isPending = false
                backendError(error)
            }
        },
        async fetchMe(){
            try{
                this.isPending = true
                const response = await $backend('/api/v1/auth/me')
                this.isPending = false
                
                this.user = response
            }catch(error){
                this.isPending = false
                backendError(error)
            }
        },
        async logout(){
            try{
                this.isPending = true
                await $backend('/api/v1/auth/logout', {
                    method: 'POST'
                })
                this.isPending = false
                this.user = {} as components["schemas"]["DoctorDetailRead"]
                navigateTo('/auth/login')
            }catch(error){
                this.isPending = false
                backendError(error)
            }
        }
    },
    getters: {
        isAuthenticated: (state) => Object.keys(state.user).length > 0,
        role: (state) => state.user.role.name
    }
})
