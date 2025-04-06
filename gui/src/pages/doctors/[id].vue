<script setup lang="ts">
import type { components } from '#nuxt-api-party/backend'
import type { TableColumn, TableRow } from '@nuxt/ui'

definePageMeta({
    layout: 'doctors'
})

useBackButton().value = true
const route = useRoute()
const authStore = useAuthStore()

const {data, status, refresh} = await useBackendData(`/api/v1/doctors/{doctor_id}`,{
    path: {
        doctor_id: route.params.id as string
    },
    lazy: true,
    cache: false
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
    header: 'Ім\'я',
    cell({row}) {
        return row.original.last_name + ' ' + row.original.first_name + ' ' + row.original.middle_name
    }
},{
    header: 'Телефон',
    accessorKey: 'phone_number'
},{
    header: 'Email',
    accessorKey: 'email'
},{
    header: 'Дата народження',
    cell({row}) {
        return row.original.birth_data + ' (' + getAge(row.original.birth_data) + ')'
    }
}]

const patientTableSelect = (row: TableRow<components["schemas"]["PatientRead"]>, event: any) => {
    navigateTo(`/patients/${row.original.patient_id}`)
}

const transformDoctor = (doctor: components["schemas"]["DoctorDetailRead"]) => {
    const { patients, department, role, ...rest} = doctor
    rest["role_id"] = role.role_id
    rest["department_id"] = department.department_id
    return rest as components["schemas"]["DoctorRead"]
}


</script>


<template>
    <UTabs :items="tabs" class="w-full" variant="link">
        <template #info>
        <div class="flex flex-col gap-2" v-if="status === 'success'">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
                <UCard :ui="{body: 'flex flex-col gap-2 relative'}">
                    <div class="flex flex-row gap-2 items-center absolute bottom-2 right-2">
                        <DoctorUpdate :doctor="transformDoctor(data)" @updated="refresh" />
                        <DoctorDelete :doctor="transformDoctor(data)"/>
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
                    <UBadge label="Мій профіль" v-if="data?.doctor_id === authStore.user.doctor_id" class="w-fit" variant="subtle"/>
                </UCard>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
                <UCard :ui="{body: 'flex flex-col gap-2'}">
                    <UILabel label="Відділення">
                        <ULink class="hover:bg-gray-700/20 rounded-lg py-2 pr-2 cursor-pointer w-fit" :to="`/departments/${data?.department.department_id}`">{{ data?.department.name }}</ULink></UILabel>
                    <UILabel label="Спеціальність">{{ data?.specialization }}</UILabel>
                </UCard>
                <UCard :ui="{body: 'flex flex-col gap-2'}">
                    <UILabel label="Роль">{{ data?.role.name }}</UILabel>
                    <UILabel label="Дозволи">
                        <div class="grid grid-cols-6 gap-2 py-2">
                            <UBadge v-for="permission in data?.role.permissions" :key="permission.permission_id" variant="subtle" color="secondary">{{ permission.resource + ':' + permission.action }}</UBadge>
                        </div>
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
    <template #patients>
        <UTable :data="data?.patients" :columns="patientColumns" @select="patientTableSelect"/>
    </template>
    <template #medical_records>
        <MedRecordsTable :query="{doctor_id: data?.doctor_id}" :showPatient="true" :showDoctor="false" />
    </template>

    </UTabs>
</template>
