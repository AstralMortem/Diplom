import type { components } from "#nuxt-api-party/backend";


export const usePatientStore = defineStore('patient', {
    state: () => ({
        patients: [] as Array<components["schemas"]["PatientRead"]>,
        isPending: false,
        total: 0,
        page: 0,
        size: 10,
        pages: 0
    }),
    actions: {
        async fetchPatients(){
            try{
                this.isPending = true
                const response = await $backend('/api/v1/patients/', {
                    method: 'GET',
                    query: {
                        page: this.page + 1,
                        size: this.size
                    }
                })
                this.patients = [...this.patients,...response.items]
                this.total = response.total as number
                this.pages = response.pages as number
                this.page = response.page as number
                this.size = response.size as number
                this.isPending = false
            }catch(error){
                this.isPending = false
                backendError(error)
            }
        },
        async createPatient(patient: components["schemas"]["PatientCreate"]){
            try{
                this.isPending = true
                const response = await $backend('/api/v1/patients/', {
                    method: 'POST',
                    body: patient
                })
                this.patients.push(response)
                this.isPending = false
                this.total += 1
                return response
            }catch(error){
                this.isPending = false
                backendError(error)
                return false
            }
        },
        async updatePatient(patient_id: string, patient: components["schemas"]["PatientUpdate"]){
            try{
                this.isPending = true
                const response = await $backend(`/api/v1/patients/{patient_id}`, {
                    method: 'PATCH',
                    path: {
                        patient_id
                    },
                    body: patient
                })
                this.patients = this.patients.map(p => p.patient_id === patient_id ? response : p)
                this.isPending = false
                return true
            }catch(error){
                this.isPending = false
                backendError(error)
                return false
            }
        } ,
        
        async deletePatient(patient_id: string){
            try{
                this.isPending = true
                await $backend(`/api/v1/patients/{patient_id}`, {
                    method: 'DELETE',
                    path: {
                        patient_id
                    }
                })
                this.patients = this.patients.filter(p => p.patient_id !== patient_id)
                this.isPending = false  
                return true
            }catch(error){
                this.isPending = false
                backendError(error)
                return false
            }
        }
    }
})

