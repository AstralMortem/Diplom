<script setup lang="ts">
const route = useRoute()
useBackButton().value = true

const {data, status, refresh} = await useBackendData(`/api/v1/departments/{department_id}`, {
    path: {
        department_id: Number(route.params.id as string)
    },
    lazy: true,
    cache: false
})

const select = (row: any, event: any) => {
    navigateTo(`/doctors/${row.original.doctor_id}`)
}

const columns = ref([{
    header: 'Прізвище',
    accessorKey: 'last_name'
},{
    header: 'Ім\'я',
    accessorKey: 'first_name'
}, {
    header: 'По-батькові',
    accessorKey: 'middle_name'
}, {   
    header: 'Телефон',
    accessorKey: 'phone_number'
}, {
    header: 'Email',
    accessorKey: 'email'        
},])

</script>

<template>
    <div class="flex flex-col gap-4">
        <UCard v-if="status === 'success'">
            <div class="flex flex-col gap-2">
                <UILabel label="Назва">{{ data?.name }}</UILabel>
                <UILabel label="Телефон">{{ data?.contact_phone }}</UILabel>
                <UILabel label="Опис">{{ data?.description }}</UILabel>
            </div>
        </UCard>
        <UCard v-else>
            <USkeleton class="w-full h-44 rounded-lg" />
        </UCard>
        <UCard>
            <UTable :data="data?.doctors || []" :columns="columns" :loading="status === 'pending'" @select="select" />
        </UCard>
        
    </div>
    
</template>