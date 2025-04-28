<script setup lang="ts">
import type { components } from '#open-fetch-schemas/backend';
import type { PropType } from 'vue';


defineProps({
    item: {
        type: Object as PropType<components["schemas"]["DoctorRead"]>,
        required: true
    }
})

</script>

<template>
    <ULink class="rounded-md p-3 hover:bg-primary-700/60" :to="`/doctors/${ item.doctor_id }`" active-class="border-r-2 bg-primary-900/20 border-primary-600">
        <div class="flex items-center gap-2">
            <UAvatar :alt="`${item.last_name} ${item.first_name}`" />
            <div class="flex flex-col">
                <span class="text-sm font-medium">{{ item.last_name }} {{ item.first_name }}</span>
                <span class="text-xs text-gray-500">{{ item.phone_number }}</span>
                <span v-if="item.department" class="text-xs text-gray-500">{{ item.specialization }}</span>
            </div>
        </div>
    </ULink>

</template>