<template>
  <div class="w-full h-full flex gap-4 flex-col-reverse md:flex-row">
    <TranscriptionDocument/>
    <TranscriptionConfig/>
  </div>
</template>

<script lang="ts" setup>
useBackButton().value = true
const authStore = useAuthStore()

onBeforeMount(()=> {
    if (!authStore.hasAccess("create", "transcriptions")){
        abortNavigation()
    }
})
</script>

<style>

</style>