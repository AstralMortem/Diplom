<script setup lang="ts">
import type { components } from '#open-fetch-schemas/backend';



defineProps({
    patient: {
        type: Object as PropType<components["schemas"]["PatientRead"]>,
        required: true
    }
})

</script>

<template>
    <ULink class="flex items-center justify-start gap-2 hover:bg-gray-700/20 rounded-lg p-2 cursor-pointer w-fit" :to="`/patients/${patient.patient_id}`">
        <UAvatar :alt="`${patient.last_name} ${patient.first_name}`" />
        <div class="flex flex-col items-start">
            <span class="text-sm font-medium">{{patient.last_name }} {{ patient.first_name }} {{ patient.middle_name }}</span>
            <span class="text-xs text-gray-500">{{ patient.phone_number }}</span>
        </div>
    </ULink>
</template>
