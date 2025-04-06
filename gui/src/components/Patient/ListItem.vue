<script setup lang="ts">
import type { components } from '#nuxt-api-party/backend';
import type { PropType } from 'vue';


defineProps({
    patient: {
        type: Object as PropType<components["schemas"]["PatientRead"]>,
        required: true
    }
})

</script>

<template>
    <ULink class="rounded-md p-3 hover:bg-primary-700/60" :to="`/patients/${ patient.patient_id }`" active-class="border-r-2 bg-primary-900/20 border-primary-600">
        <div class="flex items-center gap-2">
            <UAvatar :alt="`${patient.last_name} ${patient.first_name}`" />
            <div class="flex flex-col">
                <span class="text-sm font-medium">{{ patient.last_name }} {{ patient.first_name }}</span>
                <span class="text-xs text-gray-500">{{ patient.phone_number }}</span>
            </div>
        </div>
    </ULink>

</template>