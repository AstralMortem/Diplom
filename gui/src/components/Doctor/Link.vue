<template>
  <ULink class="flex items-center justify-start gap-2 hover:bg-gray-700/20 rounded-lg p-2 cursor-pointer w-fit" :to="`/doctors/${doctor.doctor_id}`">
    <UAvatar :alt="`${doctor.last_name} ${doctor.first_name}`" />
    <div class="flex flex-col items-start">
        <span class="text-sm font-medium">{{doctor.last_name }} {{ doctor.first_name }} {{ doctor.middle_name }}</span>
        <span class="text-xs text-gray-500">{{ doctor.phone_number }}</span>
    </div>
  </ULink>
</template>

<script lang="ts" setup>
import type { components } from '#open-fetch-schemas/backend';
import type { PropType } from 'vue';

defineProps({
  doctor:{
    type: {} as PropType<components["schemas"]["DoctorRead"]>,
    required: true
  }
})
</script>

<style>

</style>