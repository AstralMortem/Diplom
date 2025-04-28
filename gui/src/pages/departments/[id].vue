<script setup lang="ts">
import type { components } from '#open-fetch-schemas/backend'
import type { TableColumn } from '@nuxt/ui'


const route = useRoute()
const router = useRouter()

const {data, status, error, refresh} = await useBackend('/api/v1/departments/{department_id}',{
    method: 'GET',
    path: {
        department_id: Number(route.params.id as string)
    },
})

watch(error, ()=> {
    if(error.value){
        backendError(error)
    }
})

const columns: TableColumn<components["schemas"]["DoctorRead"]>[] = [{
    header: 'ПІБ',
    accessorKey: 'full_name',
    cell: ({row}) => {
        return `${row.original.last_name } ${row.original.first_name} ${row.original.last_name}`
    }
},{
    header: 'Email',
    accessorKey: 'email'
}, {
    header: 'Телефон',
    accessorKey: 'phone_number'
}]
definePageMeta({
  resourece: "departments"
})

useBackButton().value = true

</script>

<template>
    <div  class="w-full h-full flex flex-col gap-2">
        <UCard v-if="status === 'success'">
            <div class="flex flex-col gap-2 relative">
                <UILabel label="Назва">
                    {{ data?.name }}
                </UILabel>
                <UILabel label="Контактний телефон">
                    {{ data?.contact_phone || '-' }}
                </UILabel>
                <UILabel label="Опис">
                    <p class="text-base font-normal">{{ data?.description }}</p>
                </UILabel>

                <div class="flex flex-row justify-end items-center gap-2">
                    <DepartmentDelete :department="removeFields(data, ['doctors'])" @deleted="router.go(-1)"/>
                    <DepartmentUpdate :department="removeFields(data, ['doctors'])" @updated="refresh"/>
                </div>
            </div>
        </UCard>
        <UCard v-else>
            <div class="flex flex-col gap-2">
                <USkeleton v-for="i in 3" :key="i" class="w-full h-10"/>
            </div>
        </UCard>
        <UCard :ui="{body: 'overflow-y-scroll max-h-[50vh]'}">
            <UILabel label="Лікарі" >
                <UTable :data="data?.doctors || []" :loading="status === 'pending'" :columns="columns" class="w-full" />
            </UILabel>
        </UCard>
        
    </div>
</template>