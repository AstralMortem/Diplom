<script setup lang="ts">
import { UBadge } from '#components'
import type { components } from '#nuxt-api-party/backend'
import type { TableColumn, TableRow } from '@nuxt/ui'


const props = defineProps({
    query: {
        type: Object as PropType<object>,
    },
    showPatient: {
        type: Boolean,
        default: false
    },
    showDoctor: {
        type: Boolean,
        default: false
    },
})

const page = ref(1)
const size = ref(10)
const query = ref(props.query)

const {data, status, refresh} = await useBackendData('/api/v1/med-records/',{
    query: {
        page: page.value,
        size: size.value,
        ...query.value
    },
    cache: false,
    lazy: true,
    watch: [page, size, query]
})

const total = ref(data.value?.total || 0)




const medRecordsColumns = ref<TableColumn<components["schemas"]["MedRecordRead"]>[]>([{
    header: 'Статус',
    accessorKey: 'status',
    cell: ({ row }) => {
        return getStatus(row.getValue('examination_date'))
    }
},{
    header: "Дата",
    accessorKey: 'examination_date',
    cell: ({ row }) => {
      return new Date(row.getValue('examination_date')).toLocaleString('uk-UA', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
      })
    }
},{
    header: "Відділення",
    accessorKey: 'department'
}])

if(props.showDoctor){
    medRecordsColumns.value.push({
        header: "Лікар",
        accessorKey: 'doctor'
    })
}

if(props.showPatient){
    medRecordsColumns.value.push({
        header: "Пацієнт",
        accessorKey: 'patient'
    })
}


const emit = defineEmits(['select'])

const onSelect = (row: TableRow<components["schemas"]["MedRecordRead"]>, event: any) =>{
    navigateTo('/medical-records/' + row.original.record_id)
    emit('select', row)
}




</script>

<template>

    <UCard>
        <template #header>
            <div class="flex justify-between items-center">
                <p>Мед. записи ({{ total }})</p>
                <MedRecordsAdd @add="refresh"/>
            </div>

        </template>
        <UTable :data="data?.items || []" :columns="medRecordsColumns" @select="onSelect" :ui="{root: 'hover:cursor-pointer'}" :loading="status === 'pending'">
            <template #doctor-cell="{row}" v-if="props.showDoctor">
                <DoctorLabel :doctor="row.original.doctor" />
            </template>
            <template #patient-cell="{row}" v-if="props.showPatient">
                <PatientLabel :patient="row.original.patient" />
            </template>
            <template #department-cell="{row}">
                <DepartmentLabel :department="row.original.department" />
            </template>
        </UTable>
        <template #footer>
            <div class="flex justify-between items-center">
                <div class="flex items-center gap-2">
                    <UButton variant="subtle" @click="refresh" color="neutral" leading-icon="i-heroicons-arrow-path" :loading="status === 'pending'" />
                    <USelectMenu v-model="size" :items="[5,10,25,50]"/>
                </div>
                
                <UPagination v-model:page="page" :total="total" :page-size="size" />
            </div>
            
        </template>
    </UCard>

    
</template>
