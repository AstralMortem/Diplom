
import type { components } from '#open-fetch-schemas/backend';
import {FetchError} from 'ofetch';
import { defineStore } from "pinia";
import {useLocalStorage} from '@vueuse/core'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: {} as components["schemas"]["DoctorDetailRead"],
        isPending: false
    }),
    actions: {
        async login(username: string, password: string){
            const form = new FormData()
            form.append("username", username)
            form.append("password", password)
            try{
                this.isPending = true
                const {$backend} = useNuxtApp()
                const response = await $backend('/api/v1/auth/login', {
                    method: 'POST',
                    body: form,
                    cache: 'no-cache',
                    // credentials: 'include'
                })
                this.isPending = false
                const token = useLocalStorage('auth_token', response.access_token)
                if(token.value){
                    await this.fetchMe()
                }else{
                    token.value = response.access_token
                    await this.fetchMe()
                }
                
            }catch(error){
                this.isPending = false
                backendError(error)
            }
        },
        async fetchMe(){
            const {$backend} = useNuxtApp()
            try{
                this.isPending = true
                const response = await $backend('/api/v1/auth/me', {
                    // 
                    cache: 'no-cache'
                })
                this.isPending = false
                
                this.user = response
            }catch(error){
                this.isPending = false
                backendError(error)
            }
        },
        async logout(){
            const {$backend} = useNuxtApp()
            try{
                this.isPending = true
                await $backend('/api/v1/auth/logout', {
                    method: 'POST',
                    // credentials: 'include'
                })
                this.isPending = false
                this.user = {} as components["schemas"]["DoctorDetailRead"]
                const token = useLocalStorage('auth_token', '')
                if(token.value){
                    token.value = ''
                }
                navigateTo('/auth/login')
            }catch(error){
                this.isPending = false
                backendError(error)
            }
        },
        hasAccess(action:string, resouce?: string | undefined ){
            if(resouce){
                return this.user.role.permissions.some(obj => {
                    return Object.entries({resource: resouce, action: action}).every(([key, value]) => {
                        return obj[key] === value;
                    })
                })
            }
            return true
            
        }
    },
    getters: {
        isAuthenticated: (state) => Object.keys(state.user).length > 0,
        role: (state) => state.user.role.name
    }
})
