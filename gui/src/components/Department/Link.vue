<template>
  <ULink class="hover:bg-gray-700/20 rounded-lg py-2 pr-2 cursor-pointer w-fit " :to="`/departments/${$props.department.department_id}`">{{ $props.department.name }}</ULink>
</template>

<script lang="ts" setup>
import type { components } from '#open-fetch-schemas/backend';
import type { PropType } from 'vue';

defineProps({
  department: {
    type: {} as PropType<components["schemas"]["DepartmentRead"]>,
    required: true
  }
})
</script>

<style>

</style>