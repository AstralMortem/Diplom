<script setup lang="ts">
import { UBadge } from '#components'
import type { components } from '#nuxt-api-party/backend'
import type { TableColumn, TableRow } from '@nuxt/ui'


useBackButton().value = true

definePageMeta({
    layout: 'patients'
})
const route = useRoute()
const router = useRouter()

const {data, status, refresh} = await useBackendData('/api/v1/patients/{patient_id}', {
    path: {
        patient_id: route.params.id as string
    },
    lazy: true,
    cache: false
})

const items = ref([{
    label: "Інформація",
    slot: 'info' as const
},{
    label: "Мед. записи",
    slot: 'med-records' as const
}])




const transformPatient = (patient: components["schemas"]["PatientDetailRead"]) => {
    const { medical_records, ...rest } = patient
    return rest
}

</script>

<template>
<UTabs :items="items" class="w-full" variant="link">
    <template #info>
        <div class="flex flex-col gap-2" v-if="status === 'success'">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
                <UCard :ui="{body: 'flex flex-col gap-2 relative'}">
                    <div class="flex flex-row gap-2 items-center absolute bottom-2 right-2">
                        <PatientUpdate :patient="transformPatient(data)" @updated="refresh"/>
                        <PatientDelete :patient="transformPatient(data)"/>
                    </div>
                    
                    <div class="flex flex-row gap-4 flex-wrap">
                        <UILabel label="Прізвище">{{ data?.last_name }}</UILabel>
                        <UILabel label="Ім'я">{{ data?.first_name }}</UILabel>
                        <UILabel label="По-батькові">{{ data?.middle_name }}</UILabel>
                    </div>
                    <UILabel label="Дата народження">{{ data?.birth_data }} ({{ getAge(data?.birth_data) }})</UILabel>
                    <UIGenderLabel :gender="data?.gender" />
                </UCard>
                <UCard :ui="{body: 'flex flex-col gap-2'}">
                    <UILabel label="Номер телефону">{{ data?.phone_number }}</UILabel>
                    <UILabel label="Електронна пошта">{{ data?.email }}</UILabel>
                    <UILabel label="Адреса">{{ data?.address }}</UILabel>
                </UCard>
            </div>
        </div>
        <div class="flex flex-col gap-2" v-else-if="status === 'pending'">
            <div class="grid grid-cols-2 gap-2" v-for="j in 2" :key="j">
                <USkeleton class="w-full h-20" v-for="i in 2" :key="i"/>
            </div>
        </div>
        <div class="flex flex-col gap-2" v-else>
            <p>Empty</p>
        </div>
    </template>
    <template #med-records>
        <MedRecordsTable :query="{patient_id: data?.patient_id}" :showPatient="false" :showDoctor="true" />
    </template>
</UTabs>
</template>