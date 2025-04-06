<script setup lang="ts">



const columns = [{
    header: "#",
    accessorKey: "department_id"
}, {
    header: "Назва",
    accessorKey: "name"
}, {
    header: "Телефон",
    accessorKey: "contact_phone"
}, {
    header: "Опис",
    accessorKey: "description"
}]


const departmentStore = useDepartmentStore()
const {departments, size, isPending, page, total} = storeToRefs(departmentStore)





const onSelect = (row: TableRow, e: any) => {
    navigateTo(`/departments/${row.original.department_id}`)
}

useBackButton().value = false

onMounted(async () => {
    if(departments.value.length == 0){
        await departmentStore.fetchDepartments()
    }
})



</script>


<template>
    <UCard>
        <UTable :data="departments" :loading="isPending" :columns="columns" @select="onSelect"/>
        <template #footer>
            <div class="flex justify-between items-center">
                <USelect :items="[5,10,20,50]" v-model="size" />
                <UPagination v-model="page" :total="total" :page-size="size" />
            </div>
        </template>
    </UCard>
</template>