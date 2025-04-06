<script setup lang="ts">
import type { components } from '#nuxt-api-party/backend';
import type { PropType } from 'vue';


defineProps({
    doctor: {
        type: Object as PropType<components["schemas"]["DoctorRead"]>,
        required: true
    }
})

</script>

<template>
    <ULink class="rounded-md p-3 hover:bg-primary-700/60" :to="`/doctors/${ doctor.doctor_id }`" active-class="border-r-2 bg-primary-900/20 border-primary-600">
        <div class="flex items-center gap-2">
            <UAvatar :alt="`${doctor.last_name} ${doctor.first_name}`" />
            <div class="flex flex-col">
                <span class="text-sm font-medium">{{ doctor.last_name }} {{ doctor.first_name }}</span>
                <span class="text-xs text-gray-500">{{ doctor.phone_number }}</span>
                <span class="text-xs text-gray-500">{{ doctor.department.name }}</span>
            </div>
        </div>
    </ULink>

</template>