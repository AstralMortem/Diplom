<script setup lang="ts">
import type { components } from '#nuxt-api-party/backend';


const props = defineProps({
    department: {
        type: Object as PropType<components["schemas"]["DepartmentRead"]>,
        required: true
    }
})

</script>

<template>
    <ULink class="flex items-center justify-center gap-2 hover:bg-gray-700/20 rounded-lg p-2 cursor-pointer w-fit" :to="`/departments/${department.department_id}`">
        <span class="text-sm font-medium">{{ department.name }}</span>
        <span class="text-xs text-gray-500" v-if="department.contact_phone">{{ department.contact_phone }}</span>
    </ULink>
</template>
