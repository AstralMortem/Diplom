import type { components } from "#nuxt-api-party/backend";


export const useMedRecordStore = defineStore('medRecord', {
    state: () => ({
        medRecords: [] as components["schemas"]["MedRecordRead"][],
        isPending: false,
        total: 0,
        page: 1,
        size: 10,
        pages: 0
    }),
    actions: {
        async fetchMedRecords(query: object | undefined = undefined){
            try{
                this.isPending = true
                const response = await $backend('/api/v1/med-records/', {
                    method: 'GET',
                    query: {
                        page: this.page,
                        size: this.size,
                        ...query
                    }}
                )
                this.isPending = false
                this.medRecords = [...this.medRecords, ...response.items]
                this.total = response.total as number
                this.pages = response.pages as number
                this.page = response.page as number
                this.size = response.size as number
            }catch(error){
                this.isPending = false
                backendError(error)
            }
        },
        reset(){
            this.medRecords = []
            this.total = 0
            this.page = 1
            this.size = 10
            this.pages = 0
        }
    }
})
