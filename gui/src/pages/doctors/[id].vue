<template>
  <UTabs :items="tabs" class="w-full" variant="link">
    <template #info>
      <div v-if="status === 'success'" class="flex flex-col gap-2">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
                <UCard :ui="{body: 'flex flex-col gap-2 relative'}">
                    <div class="flex flex-row gap-2 items-center absolute bottom-2 right-2">
                        <DoctorUpdate :doctor="removeFields(data, ['department', 'role','patients'])" @updated="refresh" />
                        <DoctorDelete :doctor="data" @deleted="router.go(-1)"/> 
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
                    <UBadge v-if="data?.doctor_id === authStore.user.doctor_id" label="Мій профіль" class="w-fit" variant="subtle"/>
                </UCard>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
                <UCard :ui="{body: 'flex flex-col gap-2'}">
                    <UILabel v-if="data?.department" label="Відділення">
                        <DepartmentLink :department="data.department"/>
                    </UILabel>
                    <UILabel label="Спеціальність">{{ data?.specialization }}</UILabel>
                </UCard>
                <UCard :ui="{body: 'flex flex-col gap-2'}">
                    <UILabel label="Роль">{{ data?.role.name }}</UILabel>
                    <UILabel label="Дозволи">
                        <div class="grid grid-cols-3 gap-2 py-2">
                            <UBadge v-for="permission in data?.role.permissions" :key="permission.permission_id" variant="subtle" color="secondary">{{ permission.resource + ':' + permission.action }}</UBadge>
                        </div>
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
    <template #patients>
        <UCard class="w-full" :ui="{body: 'overflow-y-scroll max-h-[70vh]'}">
            <template #header>
                <div class="flex flex-row justify-between items-center">
                    <p>Пацієнти ({{data?.patients.length || 0 }})</p>
                    <PatientAdd/>
                </div>
            </template>
            <UTable :loading="status === 'pending'" :data="data?.patients || []" :columns="patientColumns" @select="patientSelected"/>
        </UCard>
    </template>
    <template #medical_records>
        <MedRecordTable :query="{doctor_id: data?.doctor_id}" :show-doctor="false"/>
    </template>
  </UTabs>
</template>

<script lang="ts" setup>
import type { components } from '#open-fetch-schemas/backend'
import type { TableColumn, TableRow } from '@nuxt/ui'

useBackButton().value = true
const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const {data, status, refresh, error} = await useBackend('/api/v1/doctors/{doctor_id}', {
  path: {
    doctor_id: route.params.id as string
  },
  cache: 'no-cache',
  lazy: true
})

watch(error, () => {
  if(error.value){
    backendError(error.value)
  }
})

const tabs = ref([{
    label: 'Інформація',
    slot: 'info'
},{
    label: 'Пацієнти',
    slot: 'patients'
},{
    label: 'Мед. записи',
    slot: 'medical_records'
}])

const patientColumns: TableColumn<components["schemas"]["PatientRead"]>[] = [{
    header: 'ПІБ',
    accessorKey: 'full_name',
    cell: ({row}) => {
        return `${row.original.last_name } ${row.original.first_name} ${row.original.middle_name}`
    }
},{
    header: 'Email',
    accessorKey: 'email'
}, {
    header: 'Телефон',
    accessorKey: 'phone_number'
}]

const patientSelected = (row: TableRow<components["schemas"]["PatientRead"]>, e:any) => {
    navigateTo('/patients/' + row.original.patient_id)
}

definePageMeta({
    layout: 'doctorlist',
    resource: 'doctors'
})


</script>

<style>

</style>