<script setup lang="ts">
const authStore = useAuthStore()

const model = defineModel<number>()

if(!model.value){
    model.value = authStore.user?.department.department_id
}


const departmentStore = useDepartmentStore()
const {departments, size, isPending} = storeToRefs(departmentStore)

onMounted(async () => {
    if(departments.value.length == 0){
        size.value = 50
        await departmentStore.fetchDepartments()
    }
})

</script>


<template>
    <USelectMenu v-model="model" :items="departments" :loading="isPending" value-key="department_id" label-key="name" placeholder="Відділ" />

</template>