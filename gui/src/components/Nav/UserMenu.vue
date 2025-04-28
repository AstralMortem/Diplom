<script setup lang="ts">

const authStore = useAuthStore()
const {user} = storeToRefs(authStore)

const items = [[{
    slot: 'title',
    disabled: true,
}], [
    {
        label: 'Профіль',
        to: '/doctors/' + authStore.user.doctor_id
    }
],[{
    label: 'Вихід',
    async onSelect(e: any) {
        await authStore.logout()
    }
}]]

</script>


<template>

    <UDropdownMenu  :items="items" >
        <UAvatar :alt="`${ user.last_name } ${user.first_name}`" />
        <template #title>
            <span>Привіт, {{ user.email || user.phone_number }}</span>
        </template>
    </UDropdownMenu >
</template>
