<template>
<div class="flex justify-center items-center h-full w-full">
        <div class="flex flex-col gap-3 items-center justify-center p-2  border-neutral-700 rounded-lg">
            <UIcon name="i-heroicons-user-circle" size="5rem"/>
            <p class="text-2xl">Виберіть лікаря або додайте нового</p>
            <DoctorAdd/>
        </div>
    </div>
</template>

<script lang="ts" setup>

definePageMeta({
  layout: 'doctorlist',
  resource: 'doctors'
})

useBackButton().value = false


</script>

<style>

</style>