<template>
  <UTabs :items="tabs" variant="link" class="w-full">
    <template #my>
      <MedRecordTable :query="{doctor_id: authStore.user.doctor_id}" :show-doctor="false"/>
    </template>
    <template #all>
      <MedRecordTable/>
    </template>
  </UTabs>
</template>

<script lang="ts" setup>
const tabs = [{
  label: 'Мої записи',
  slot: 'my' as const
},{
  label: 'Усі записи',
  slot: 'all' as const
}]
useBackButton().value = false
const authStore = useAuthStore()


</script>

<style>

</style>