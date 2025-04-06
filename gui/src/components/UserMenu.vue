<script setup lang="ts">

const authStore = useAuthStore()
const {user} = storeToRefs(authStore)

const items = [[{
    slot: 'title',
    disabled: true,
}], [
    {
        label: 'Profile',
        to: '/auth/profile'
    },
    {
        label: 'Settings',
        to: '/settings'
    }
],[{
    label: 'Logout',
    click: async () => await authStore.logout()
}]]

</script>


<template>

    <UDropdownMenu  :items="items" >
        <UAvatar :alt="`${ user.last_name } ${user.first_name}`" />
        <template #title>
            <span>Welcome, {{ user.email || user.phone_number }}</span>
        </template>
    </UDropdownMenu >
</template>
