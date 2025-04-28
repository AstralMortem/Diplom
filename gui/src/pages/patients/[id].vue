<template>
  <UTabs class="w-full" variant="link" :items="tabs">
    <template #info>
      <div v-if="status === 'success'" class="flex flex-col gap-2">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
                <UCard :ui="{body: 'flex flex-col gap-2 relative'}">
                    <div class="flex flex-row gap-2 items-center absolute bottom-2 right-2">
                        <PatientUpdate :patient="removeFields(data, ['medical_records'])" @updated="refresh"/>
                        <PatientDelete :patient="data"/> 
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
        <div v-else-if="status === 'pending'" class="flex flex-col gap-2">
            <div v-for="j in 2" :key="j" class="grid grid-cols-2 gap-2">
                <USkeleton v-for="i in 2" :key="i" class="w-full h-20"/>
            </div>
        </div>
        <div v-else class="flex flex-col gap-2">
            <p>Empty</p>
        </div>
    </template>
    <template #medical_records>
        <MedRecordTable :query="{patient_id: data?.patient_id}" :show-patient="false"/>
    </template>
  </UTabs>
</template>

<script lang="ts" setup>
const tabs = ref([{
    label: "Інформація",
    slot: 'info' as const
},{
    label: "Мед. записи",
    slot: 'medical_records' as const
}])

const route = useRoute()

const {data, error, status, refresh} = await useBackend('/api/v1/patients/{patient_id}',{
  path: {
    patient_id: route.params.id as string
  },
  
  cache: 'no-cache',
  lazy: true
})

watch(error, () => {
  if(error.value){
    backendError(error.value)
  }
})

definePageMeta({
  layout: 'patientlist',
  resource: 'patients'
})
useBackButton().value = true
</script>

<style>

</style>