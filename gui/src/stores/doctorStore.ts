import type { components } from "#nuxt-api-party/backend";

export const useDoctorStore = defineStore("doctorStore", {
    state: () => ({
        _doctors: [] as components["schemas"]["DoctorRead"][],
        isPending: false,
        total: 0,
        page: 0,
        size: 10,
        pages: 0

    }),
    actions:{
        async fetchDoctors(){
            try{
                this.isPending = true
                const response = await $backend('/api/v1/doctors/', {
                    query:{
                        page: this.page + 1,
                        size: this.size
                    }
                })
                this.isPending = false
                this._doctors = [...this._doctors, ...response.items]
                this.total = response.total as number
                this.pages = response.pages as number
                this.page = response.page as number
                this.size = response.size as number
                
            }catch(error){
                this.isPending = false
                backendError(error)
            }
        },
        async createDoctor(doctor: components["schemas"]["DoctorCreate"]){
            try{
                this.isPending = true
                const response = await $backend('/api/v1/doctors/', {
                    method: 'POST',
                    body: doctor
                })
                this.isPending = false
                this._doctors.push(response)
                this.total += 1
                return response
            }catch(error){
                this.isPending = false
                backendError(error)
                return false
            }
        },
        async updateDoctor(doctor_id: string, doctor: components["schemas"]["DoctorUpdate"]){
            try{
                this.isPending = true
                const response = await $backend(`/api/v1/doctors/{doctor_id}`, {
                    method: 'PATCH',
                    path: {
                        doctor_id
                    },
                    body: doctor
                })
                this._doctors = this._doctors.map(d => d.doctor_id === doctor_id ? response : d)
                this.isPending = false
                return true
            }catch(error){
                this.isPending = false
                backendError(error)
                return false
            }
        } ,
        async deleteDoctor(doctor_id: string){
            try{
                this.isPending = true
                await $backend(`/api/v1/doctors/{doctor_id}`, {
                    method: 'DELETE',
                    path: {
                        doctor_id
                    }
                })
                this._doctors = this._doctors.filter(p => p.doctor_id !== doctor_id)
                this.isPending = false  
                return true
            }catch(error){
                this.isPending = false
                backendError(error)
                return false
            }
        }
    },
    getters:{
        doctors: (state) => {
            const authStore = useAuthStore()
            return state._doctors.filter(doctor => doctor.doctor_id !== authStore.user.doctor_id)
        }
    }
})