<script setup lang="ts">
useBackButton().value = false

const authStore = useAuthStore()
const {user} = storeToRefs(authStore)

const tabs = [{
    label: 'Мої записи',
    slot: 'my-records' as const
},{
    label: 'Всі записи',
    slot: 'all-records' as const
}]

</script>

<template>
    <UTabs :items="tabs" variant="link" :unmount-on-hide="false">
        <template #my-records>
            <MedRecordsTable :query="{doctor_id: user.doctor_id}" :showPatient="true" :showDoctor="true" />
        </template>
        <template #all-records>
            <MedRecordsTable :showPatient="true" :showDoctor="true" />
        </template>
    </UTabs>

</template>
