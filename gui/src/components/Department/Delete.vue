<template>
  <ItemDeleteModal url="/api/v1/departments/{department_id}" :path="{department_id:$props.department.department_id}" :title="'Видалити відділення ' + $props.department.name" resource="departments" @deleted="$emit('deleted')">
    <template #body>
      <p class="font-semibold text-2xl">Ви впевнені що хочете видалити відділення <span class="text-error-500">{{ $props.department.name }}</span>?</p>
    </template>
  </ItemDeleteModal>
</template>

<script lang="ts" setup>
import type { components } from '#open-fetch-schemas/backend';
import type { PropType } from 'vue';

defineEmits(['deleted'])

defineProps({
  department: {
    type: {} as PropType<components["schemas"]["DepartmentRead"]>,
    required:true
  }
})


</script>

<style>

</style>