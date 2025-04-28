<template>
  <UTabs class="w-full" :items="tabs" variant="link">
    <template #info>
      <div v-if="status === 'success' && data" class="flex flex-col gap-2">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
          <UCard :ui="{body: 'flex flex-col gap-2 relative'}">
              <UILabel label="Пацієнт">
                  <PatientLink :patient="data.patient" />
              </UILabel>
              <UILabel label="Лікар">
                  <DoctorLink :doctor="data.doctor" />
              </UILabel>
              <UILabel label="Відділення">
                  <DepartmentLink :department="data.department" />
              </UILabel>
              <div class="absolute bottom-2 right-2 flex flex-row gap-2 items-center">
                <MedRecordUpdate :record="removeFields(data, ['department', 'doctor', 'patient', 'transcriptions'])" @updated="refresh"/>
                <MedRecordDelete :record="removeFields(data, ['department', 'doctor', 'patient', 'transcriptions'])" @updated="router.go(-1)"/>
              </div>
          </UCard>
          <UCard :ui="{body: 'flex flex-col gap-2 relative'}">
              <UILabel label="Дата">
                  {{ new Date(data.examination_date).toLocaleString() }}
              </UILabel>
              <UILabel label="Статус">
                  <component :is="getRecordStatus(data.examination_date)" class="w-fit"/>
              </UILabel>
                  <UILabel v-if="authStore.hasAccess('retrieve', 'transcriptions')" label="Почати прийом">
                      <UButton :to="`/records/${route.params.id}/add-transcription`" size="xl" class="w-fit">Додати транскрипцію</UButton>
                  </UILabel>
                  <UILabel label="Звіт">
                    <MedRecordReportButton :record="data"/>
                  </UILabel>
          </UCard>
        </div>
      </div>
      <div v-else-if="status === 'pending'" class="flex flex-col gap-2">
          <div v-for="j in 2" :key="j" class="grid grid-cols-2 gap-2">
              <USkeleton v-for="i in 2" :key="i" class="w-full h-20"/>
          </div>
      </div>
      <div v-else class="flex flex-col gap-2">
          <p>Empty</p>
      </div>


    </template>
    <template #transcriptions>
      <UCard class="w-full" :ui="{body: 'overflow-y-scroll max-h-[70vh]'}">
            <template #header>
                <div class="flex flex-row justify-between items-center" >
                    <p>Транскрипції ({{data?.transcriptions.length || 0 }})</p>
                    <UButton label="Додати транскрипцію" @click="navigateTo(`/records/${$route.params.id}/add-transcription`)"/>
                </div>
            </template>
            <UTable :loading="status === 'pending'" :data="data?.transcriptions || []" :columns="transcriptionColumns">
              <template #audio-cell="{row}">
                <audio :src="mdns + row.original.audio_url" controls/>
              </template>
              <template #actions-cell="{row}">
                <TranscriptionDelete :transcription="row.original"/>
              </template>
              <template #expanded="{row}">
                <div class=" w-full flex flex-row items-center">
                  <UCard>
                    <p class="whitespace-pre-line">{{ row.original.transcription_text }}</p>
                  </UCard>
                </div>
              </template>
            </UTable>
        </UCard>
    </template>
  </UTabs>
  
</template>

<script lang="ts" setup>
import { UButton } from '#components'
import type { components } from '#open-fetch-schemas/backend'
import type { TableColumn } from '@nuxt/ui'

const mdns = await useMDNS()

const router = useRouter()
const route = useRoute()
useBackButton().value = true
const authStore = useAuthStore()
const tabs = [{
  label: 'Інформація',
  slot: 'info',
},{
  label: 'Транскрипції',
  slot: 'transcriptions'
}]

const {data, error, status,refresh} = await useBackend('/api/v1/med-records/{record_id}', {
  path:{
    record_id: route.params.id as string
  },
  cache: 'no-cache',
})

watch(error, ()=>{
  if(error.value){
    backendError(error.value)
  }
})

const transcriptionColumns: TableColumn<components["schemas"]["TranscriptionRead"]>[] = [{
  id: 'expand',
    cell: ({ row }) =>
      h(UButton, {
        color: 'neutral',
        variant: 'ghost',
        icon: 'i-lucide-chevron-down',
        square: true,
        'aria-label': 'Expand',
        ui: {
          leadingIcon: [
            'transition-transform',
            row.getIsExpanded() ? 'duration-200 rotate-180' : ''
          ]
        },
        onClick: () => row.toggleExpanded()
      })
},{
  header: '#',
  accessorKey: 'transcription_id'
}, {
  header: 'Запис',
  accessorKey: 'audio'
},{
  header: 'Дата',
  accessorKey: 'created_at'
}, {
  header: '',
  accessorKey: 'actions'
}]



</script>

<style>

</style>