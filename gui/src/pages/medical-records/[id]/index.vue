<script setup lang="ts">
import type { components } from '#nuxt-api-party/backend'

const route = useRoute()

useBackButton().value = true

const {data, status, refresh} = await useBackendData('/api/v1/med-records/{record_id}',{
    path:{
        record_id: route.params.id as string
    },
    lazy: true,
    cache: false
})

const tabs = ref([
    {
        label: 'Інформація',
        slot: 'info' as const
    },{
        label: 'Транскрипції',
        slot: 'transcriptions' as const
    }
])

const transformMedRecord = (medRecord: components["schemas"]["MedRecordRead"])=>{
    const {
        department,
        doctor,
        patient,
        transcriptions, 
        ...rest
    } = medRecord
    return rest
}

const transcriptionColumns = [{
    header: '#',
    accessorKey: "transcription_id",
}, {
    header: 'Запис',
    accessorKey: "audio_url"
}, {
    header: 'Тривалість, c.',
    accessorKey: "audio_duration"
}, {
    accessorKey: "delete"
}]


</script>


<template>
    <UTabs :items="tabs" variant="link">
        <template #info>
            <div class="flex flex-col gap-2" v-if="status === 'success' && data">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
                <UCard :ui="{body: 'flex flex-col gap-2 relative'}">
                    <UILabel label="Пацієнт">
                        <PatientLabel :patient="data.patient" />
                    </UILabel>
                    <UILabel label="Лікар">
                        <DoctorLabel :doctor="data.doctor" />
                    </UILabel>
                    <UILabel label="Відділення">
                        <DepartmentLabel :department="data.department" />
                    </UILabel>
                    <div class="absolute bottom-2 right-2 flex flex-row gap-2 items-center">
                        <MedRecordsUpdate :medRecord="transformMedRecord(data)" @updated="refresh"/>
                        <MedRecordsDelete :medRecord="transformMedRecord(data)" />
                    </div>
                </UCard>
                <UCard :ui="{body: 'flex flex-col gap-2 relative'}">
                    <UILabel label="Дата">
                        {{ new Date(data.examination_date).toLocaleString() }}
                    </UILabel>
                    <UILabel label="Статус">
                        <component :is="getStatus(data.examination_date)" class="w-fit"/>
                    </UILabel>
                    <UILabel label="Почати прийом">
                        <UButton :to="`/medical-records/${route.params.id}/add-transcription`" size="xl" class="w-fit">Додати транскрипцію</UButton>
                    </UILabel>
                    
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
        <template #transcriptions>
            <UCard>
                <UTable :data="data?.transcriptions || []" :columns="transcriptionColumns" @select="$event.toggleExpanded()">
                    <template #expanded="{row}">
                        <TranscriptionDetail :id="row.original.transcription_id" :record_id="route.params.id as string" />
                    </template>
                    <template #audio_url-cell="{row}">
                        <audio :src="'http://localhost:8000' + row.original.audio_url" controls />
                    </template>
                    <template #delete-cell="{row}">
                        <TranscriptionDelete :transcription="row.original" @deleted="refresh" />
                    </template>
                </UTable>
            </UCard>
        </template>
    </UTabs>
</template>
