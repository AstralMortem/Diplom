import type { components } from "#nuxt-api-party/backend";



export const useDepartmentStore = defineStore("departmentStore", {
    state: () => ({
        departments: [] as components["schemas"]["DepartmentRead"][],
        isPending: false,
        total: 0,
        page: 0,
        size: 10,
        pages: 0
        }),
    actions: {
        async fetchDepartments(){
            try{
                this.isPending = true
                const response = await $backend('/api/v1/departments/', {
                    query: {
                        page: this.page + 1,
                        size: this.size
                    }
                })
                this.isPending = false
                this.departments = [...this.departments, ...response.items]
                this.total = response.total as number
                this.pages = response.pages as number
                this.page = response.page as number
                this.size = response.size as number
            }catch(error){
                this.isPending = false
                backendError(error)
            }
        }
    }
})
